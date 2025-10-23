from django.urls import path
from . import views


app_name = "porteiros"

urlpatterns = [
    path("", views.visualizar_porteiros, name="visualizar_porteiros"),
    path("cadastrar/", views.cadastrar_porteiro, name="cadastrar_porteiro"),
    path("editar/<int:porteiro_id>/", views.editar_porteiro, name="editar_porteiro"),
]
