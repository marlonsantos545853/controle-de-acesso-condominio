from django.urls import path
from . import views

app_name = "proprietario"

urlpatterns = [
    path("", views.visualizar_proprietarios, name="visualizar_proprietarios"),
    path("cadastrar/", views.cadastrar_proprietario, name="cadastrar_proprietario"),
    path(
        "editar/<int:proprietario_id>/",
        views.editar_proprietario,
        name="editar_proprietario",
    ),
]
