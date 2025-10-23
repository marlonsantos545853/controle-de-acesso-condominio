from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Usuario
from visitantes.models import Visitantes
from visitantes.forms import VisitanteForm, AutorizaVisitanteForm
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from .utils import log_model_update, log_model_creation
import csv


@login_required
def registrar_visitantes(request):
    if request.user.perfil != Usuario.Perfil.PORTEIRO:
        messages.warning(request, "Somente porteiros podem cadastrar visitas")
        return redirect("index")

    form = VisitanteForm()
    if request.method == "POST":
        form = VisitanteForm(request.POST)
        if form.is_valid():
            visitante = form.save(commit=False)
            visitante.registrado_por = request.user.porteiros
            visitante.save()
            log_model_creation(request, form)
            messages.success(request, "Visitante registrado com sucesso")

            return redirect("index")

    context = {
        "nome_pagina": "Registrar isitante",
        "form": form,
    }

    return render(request, "registrar_visitante.html", context)


@login_required
def informacoes_visitantes(request, id):
    visitante = get_object_or_404(
        Visitantes,
        id=id,
    )

    form = AutorizaVisitanteForm()
    if request.method == "POST":
        form = AutorizaVisitanteForm(request.POST, instance=visitante)
        if form.is_valid():
            visitante = form.save(commit=False)
            visitante.status = "EM_VISITA"
            visitante.horario_autorizacao = timezone.now()
            if request.user.perfil != Usuario.Perfil.PORTEIRO:
                messages.warning(request, "Somente porteiros podem autorizar visitas")
                return redirect("index")

            visitante.save()
            log_model_update(request, form)
            messages.success(request, "Entrada de visitante autorizada com sucesso")

            return redirect("index")

    context = {
        "nome_pagina": "Informacoes de visitantes",
        "visitante": visitante,
        "form": form,
    }

    return render(request, "informacoes_visitante.html", context)


@login_required
def finalizar_visita(request, id):
    if request.user.perfil != Usuario.Perfil.PORTEIRO:
        messages.warning(request, "Somente porteiros podem finalizar visitas")
        return redirect("index")

    if request.method == "POST":
        visitante = get_object_or_404(Visitantes, id=id)
        visitante.status = "FINALIZADO"
        visitante.horario_saida = timezone.now()
        visitante.save()
        messages.success(request, "Visita finalizada com sucesso")

        return redirect("index")
    else:
        return HttpResponseNotAllowed(["POST"], "Método não permitido")


@login_required
def exportar_visitas_csv(request):
    if not request.user.perfil in [
        Usuario.Perfil.SINDICO,
        Usuario.Perfil.ADMINISTRADOR,
        Usuario.Perfil.CONSELHO,
    ]:
        messages.warning(request, "Vocẽ não tem autorização para gerar os relatórios.")
        return redirect("index")

    # Filtros recebidos via GET
    data_inicio = request.GET.get("inicio")
    data_fim = request.GET.get("fim")
    status = request.GET.get("status")
    visitas = Visitantes.objects.all()

    # Filtro por intervalo de datas (baseado em horario_chegada)
    if data_inicio:
        visitas = visitas.filter(horario_chegada__date__gte=parse_date(data_inicio))
    if data_fim:
        visitas = visitas.filter(horario_chegada__date__lte=parse_date(data_fim))

    # Filtro por status
    if status and status != "TODOS":
        visitas = visitas.filter(status=status)

    # Cria resposta HTTP como CSV
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="relatorio_visitas.csv"'
    writer = csv.writer(response)

    # Cabeçalho
    writer.writerow(
        [
            "Nome completo",
            "CPF",
            "Tipo",
            "Status",
            "Unidade",
            "Horário chegada",
            "Horário saída",
            "Morador responsável",
            "Registrado por",
        ]
    )

    # Linhas
    for v in visitas:
        writer.writerow(
            [
                v.nome_completo,
                v.get_cpf(),
                v.get_tipo_display(),
                v.get_status_display(),
                v.numero_casa,
                v.horario_chegada.strftime("%d/%m/%Y %H:%M"),
                v.get_horario_saida(),
                v.get_morador_responsavel(),
                v.registrado_por,
            ]
        )

    return response
