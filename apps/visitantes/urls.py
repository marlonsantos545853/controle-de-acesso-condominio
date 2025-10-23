from django.urls import path
from . import views


app_name = "visitantes"

urlpatterns = [
    path("cadastrar/", views.registrar_visitantes, name="registrar_visitantes"),
    path("<int:id>/", views.informacoes_visitantes, name="informacoes_visitantes"),
    path("<int:id>/finalizar-visita/", views.finalizar_visita, name="finalizar_visita"),
    path("exportar/", views.exportar_visitas_csv, name="exportar_csv"),
]
