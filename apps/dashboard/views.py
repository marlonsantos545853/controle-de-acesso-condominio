from django.shortcuts import render
from visitantes.models import Visitantes
from django.contrib.auth.decorators import login_required


@login_required
def index(request):

    perfil = request.user.perfil
    todos_visitantes = Visitantes.objects.order_by("-horario_chegada")
    visita_aguardando = todos_visitantes.filter(status="AGUARDANDO")
    visita_em_andamento = todos_visitantes.filter(status="EM_VISITA")
    visita_finalizada = todos_visitantes.filter(status="FINALIZADO")

    context = {
        "nome_pagina": "Pagina inicial",
        "todos_visitantes": todos_visitantes,
        "visita_aguardando": visita_aguardando.count(),
        "visita_em_andamento": visita_em_andamento.count(),
        "visita_finalizada": visita_finalizada.count(),
        "total_mes": todos_visitantes.count(),
        "perfil": perfil,
    }

    return render(request, "index.html", context)
