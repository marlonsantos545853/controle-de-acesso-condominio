from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from porteiros.forms import PorteirosForm
from porteiros.models import Porteiros
from usuarios.models import Usuario
from .utils import log_model_update, log_model_creation


@login_required
def cadastrar_porteiro(request):
    if request.user.perfil != Usuario.Perfil.SINDICO:
        messages.warning(request, "Somente o síndico pode editar o porteiro")
        return redirect("porteiros:visualizar_porteiros")

    form = PorteirosForm(request.POST or None)
    context = {
        "nome_pagina": "Cadastrar Porteiros",
        "link_cancela": reverse("porteiros:visualizar_porteiros"),
        "form_titulo": "Formulário para cadastrar porteiros",
        "nome_botao_submit": "Registrar porteiros",
        "form": form,
    }

    if form.is_valid():
        form.save()
        log_model_creation(request, form)
        messages.success(request, "Porteiros cadastrada com sucesso")

        return redirect("porteiros:visualizar_porteiros")  

    return render(request, "includes/form/form_geral.html", context)


@login_required
def editar_porteiro(request, porteiro_id):
    unidade = get_object_or_404(Porteiros, pk=porteiro_id)
    form = PorteirosForm(request.POST or None, instance=unidade)
    context = {
        "nome_pagina": "Edita Porteiros",
        "link_cancela": reverse("porteiros:visualizar_porteiros"),
        "form_titulo": "Formulário para editar porteiros",
        "nome_botao_submit": "Editar porteiros",
        "form": form,
    }

    if form.is_valid():
        if request.user.perfil != Usuario.Perfil.SINDICO:
            messages.warning(request, "Somente o síndico pode editar o porteiro")
            return redirect("porteiros:visualizar_porteiros")

        log_model_update(request, form)
        form.save()
        messages.success(request, "Porteiros editada com sucesso")

        return redirect("porteiros:visualizar_porteiros")

    return render(request, "includes/form/form_geral.html", context)


@login_required
def visualizar_porteiros(request):
    perfil = request.user.perfil
    colunas = [
        "Usuário",
        "Nome Completo",
        "CPF",
        "Telefone",
        "Data de Nascimento",
        "Detalhes",
    ]

    todos_porteiros = [
        {
            "Usuário": unid.usuario,
            "Nome Completo": unid.nome_completo,
            "CPF": unid.cpf,
            "Telefone": unid.telefone,
            "Data de Nascimento": unid.data_nascimento,
            "Detalhes": reverse(
                "porteiros:editar_porteiro", kwargs={"porteiro_id": unid.id}
            ),
        }
        for unid in Porteiros.objects.all()
    ]

    context = {
        "nome_pagina": "Porteiros",
        "link_novo": reverse("porteiros:cadastrar_porteiro"),
        "nome_botao_add": "Novo porteiro",
        "perfil": perfil,
        "colunas": colunas,
        "dados": todos_porteiros,
    }

    return render(request, "includes/tabela/tabela_geral.html", context)
