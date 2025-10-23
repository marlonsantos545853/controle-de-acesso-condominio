from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from unidades.forms import UnidadeForm
from unidades.models import Unidade
from usuarios.models import Usuario
from .utils import log_model_update, log_model_creation


@login_required
def cadastrar_unidade(request):
    if request.user.perfil != Usuario.Perfil.SINDICO:
        messages.warning(request, "Somente o síndico pode cadastar a unidades")
        return redirect("unidades:visualizar_unidades")

    form = UnidadeForm(request.POST or None)
    context = {
        "nome_pagina": "Cadastrar Unidade",
        "link_cancela": reverse("unidades:visualizar_unidades"),
        "form_titulo": "Formulário para cadastrar unidades",
        "nome_botao_submit": "Registrar unidades",
        "form": form,
    }

    if form.is_valid():
        form.save()
        log_model_creation(request, form)
        messages.success(request, "Unidade cadastrada com sucesso")

        return redirect("unidades:visualizar_unidades")  

    return render(request, "includes/form/form_geral.html", context)


@login_required
def editar_unidade(request, unidade_id):
    unidade = get_object_or_404(Unidade, pk=unidade_id)
    form = UnidadeForm(request.POST or None, instance=unidade)
    context = {
        "nome_pagina": "Edita Unidade",
        "link_cancela": reverse("unidades:visualizar_unidades"),
        "form_titulo": "Formulário para editar unidades",
        "nome_botao_submit": "Editar unidades",
        "form": form,
    }

    if form.is_valid():
        if request.user.perfil != Usuario.Perfil.SINDICO:
            messages.warning(request, "Somente o síndico pode editar a unidade")
            return redirect("unidades:visualizar_unidades")

        form.save()
        log_model_update(request, form)
        messages.success(request, "Unidade editada com sucesso")

        return redirect("unidades:visualizar_unidades")

    return render(request, "includes/form/form_geral.html", context)

@login_required
def visualizar_unidades(request):
    perfil = request.user.perfil
    colunas = ["Bloco", "Numero", "Proprietario", "Detalhes"]
    todas_unidades = [
        {
            "Bloco": unid.bloco,
            "Numero": unid.numero,
            "Proprietario": str(unid.proprietario),
            "Detalhes": reverse(
                "unidades:editar_unidade", kwargs={"unidade_id": unid.id}
            ),
        }
        for unid in Unidade.objects.all()
    ]

    context = {
        "nome_pagina": "Unidades",
        "link_novo": reverse("unidades:cadastrar_unidade"),
        "nome_botao_add": "Novo unidade",
        "perfil": perfil,
        "colunas": colunas,
        "dados": todas_unidades,
    }

    return render(request, "includes/tabela/tabela_geral.html", context)
