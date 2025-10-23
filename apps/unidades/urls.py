from django.urls import path
from . import views


app_name = "unidades"

urlpatterns = [
    path("", views.visualizar_unidades, name="visualizar_unidades"),
    path("cadastrar/", views.cadastrar_unidade, name="cadastrar_unidade"),
    path("editar/<int:unidade_id>/", views.editar_unidade, name="editar_unidade"),
]
