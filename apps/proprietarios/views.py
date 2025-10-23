from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from proprietarios.forms import ProprietariosForm
from proprietarios.models import Proprietarios
from usuarios.models import Usuario
from .utils import log_model_update, log_model_creation


@login_required
def cadastrar_proprietario(request):
    if request.user.perfil != Usuario.Perfil.SINDICO:
        messages.warning(request, "Somente o síndico pode editar o proprietário")
        return redirect("proprietarios:visualizar_proprietarios")

    form = ProprietariosForm(request.POST or None)
    context = {
        "nome_pagina": "Cadastrar Proprietarios",
        "link_cancela": reverse("proprietarios:visualizar_proprietarios"),
        "form_titulo": "Formulário para cadastrar proprietarios",
        "nome_botao_submit": "Registrar proprietarios",
        "form": form,
    }

    if form.is_valid():
        form.save()
        log_model_creation(request, form)
        messages.success(request, "Proprietarios cadastrada com sucesso")
        return redirect(
            "proprietarios:visualizar_proprietarios"
        )  

    return render(request, "includes/form/form_geral.html", context)


@login_required
def editar_proprietario(request, proprietario_id):
    unidade = get_object_or_404(Proprietarios, pk=proprietario_id)
    form = ProprietariosForm(request.POST or None, instance=unidade)
    context = {
        "nome_pagina": "Edita Proprietarios",
        "link_cancela": reverse("proprietarios:visualizar_proprietarios"),
        "form_titulo": "Formulário para editar proprietarios",
        "nome_botao_submit": "Editar proprietarios",
        "form": form,
    }

    if form.is_valid():
        if request.user.perfil != Usuario.Perfil.SINDICO:
            messages.warning(request, "Somente o síndico pode editar o proprietário")
            return redirect("proprietarios:visualizar_proprietarios")

        form.save()
        log_model_update(request, form)
        messages.success(request, "Proprietarios editada com sucesso")

        return redirect("proprietarios:visualizar_proprietarios")

    return render(request, "includes/form/form_geral.html", context)


@login_required
def visualizar_proprietarios(request):
    colunas = ["Nome Completo", "CPF", "Telefone", "email", "Detalhes"]
    todos_proprietarios = [
        {
            "Nome Completo": unid.nome_completo,
            "CPF": unid.cpf,
            "Telefone": unid.telefone,
            "email": unid.email,
            "Detalhes": reverse(
                "proprietarios:editar_proprietario", kwargs={"proprietario_id": unid.id}
            ),
        }
        for unid in Proprietarios.objects.all()
    ]

    context = {
        "nome_pagina": "Proprietários",
        "link_novo": reverse("proprietarios:cadastrar_proprietario"),
        "nome_botao_add": "Novo proprietário",
        "perfil": "",
        "colunas": colunas,
        "dados": todos_proprietarios,
    }

    return render(request, "includes/tabela/tabela_geral.html", context)
