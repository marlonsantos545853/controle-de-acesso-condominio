from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from usuarios.forms import UsuarioForm, TrocarSenhaUsuarioForm
from usuarios.models import Usuario
from .utils import log_model_update, log_model_creation


@login_required
def cadastrar_usuario(request):
    if not request.user.perfil in [
        Usuario.Perfil.SINDICO,
        Usuario.Perfil.ADMINISTRADOR,
    ]:
        messages.warning(request, "Somente o síndico pode cadastrar o usuários")
        return redirect("usuarios:visualizar_usuarios")

    form = UsuarioForm(request.POST or None)
    context = {
        "nome_pagina": "Cadastrar Usuário",
        "link_cancela": reverse("usuarios:visualizar_usuarios"),
        "form_titulo": "Formulário para cadastrar usuários",
        "nome_botao_submit": "Registrar usuário",
        "form": form,
    }

    if form.is_valid():
        form.save()
        log_model_creation(request, form)
        messages.success(request, "Usuario cadastrado com sucesso")

        return redirect("usuarios:visualizar_usuarios")  

    return render(request, "includes/form/form_geral.html", context)


@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    form = UsuarioForm(request.POST or None, instance=usuario)
    context = {
        "nome_pagina": "Edita Usuário",
        "link_cancela": reverse("usuarios:visualizar_usuarios"),
        "form_titulo": "Formulário para editar usuários",
        "nome_botao_submit": "Editar usuário",
        "form": form,
    }

    if form.is_valid():
        if (
            form.perfil() == Usuario.Perfil.ADMINISTRADOR
            and request.user.perfil != Usuario.Perfil.ADMINISTRADOR
        ):
            messages.warning(request, "Perfil de Administrador não pode ser editado.")

            return redirect("usuarios:visualizar_usuarios")

        if not request.user.perfil in [
            Usuario.Perfil.SINDICO,
            Usuario.Perfil.ADMINISTRADOR,
        ]:
            messages.warning(request, "Somente o síndico pode editar o usuários")

            return redirect("usuarios:visualizar_usuarios")

        form.save()
        log_model_update(request, form)
        messages.success(request, "Usuario editado com sucesso")

        return redirect("usuarios:visualizar_usuarios")

    return render(request, "includes/form/form_geral.html", context)


@login_required
def visualizar_usuarios(request):
    perfil = request.user.perfil
    colunas = ["Email", "Perfil", "Ativo", "Detalhes"]
    todos_usuarios = [
        {
            "Email": prop.email,
            "Perfil": prop.perfil,
            "Ativo": str(prop.is_active),
            "Detalhes": reverse(
                "usuarios:editar_usuario", kwargs={"usuario_id": prop.id}
            ),
        }
        for prop in Usuario.objects.all()
    ]

    context = {
        "nome_pagina": "Usuários",
        "link_novo": reverse("usuarios:cadastrar_usuario"),
        "nome_botao_add": "Novo usuário",
        "perfil": perfil,
        "colunas": colunas,
        "dados": todos_usuarios,
    }

    return render(request, "includes/tabela/tabela_geral.html", context)


@login_required
def atualiza_senha_usuario(request):
    usuario = get_object_or_404(
        Usuario,
        id=request.user.id,
    )

    form = TrocarSenhaUsuarioForm()
    if request.method == "POST":
        form = TrocarSenhaUsuarioForm(request.POST, instance=usuario)
        if form.is_valid() and usuario.password != "123456":
            usuario = form.save(commit=False)
            usuario.save()
            messages.success(request, "Senha do usuario atualizada com sucesso")

            return redirect("index")
        else:
            messages.warning(request, "A senha deve conter no mínimo 6 caracteres")

            return redirect("index")

    context = {
        "nome_pagina": "Pagina inicial",
        "usuario": usuario,
        "form": form,
    }

    return render(request, "index.html", context)
