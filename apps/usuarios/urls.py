from django.urls import path
from . import views


app_name = "usuarios"

urlpatterns = [
    path("", views.visualizar_usuarios, name="visualizar_usuarios"),
    path("cadastrar/", views.cadastrar_usuario, name="cadastrar_usuario"),
    path("editar/<int:usuario_id>/", views.editar_usuario, name="editar_usuario"),
    path("perfil/", views.atualiza_senha_usuario, name="atualiza_senha_usuario"),
]
