# apps/visitantes/tests/test_views.py
from django.test import TestCase
from django.urls import reverse_lazy
from model_mommy import mommy
from django.utils import timezone
from usuarios.models import Usuario
from porteiros.models import Porteiros
from visitantes.models import Visitantes
import csv
from io import StringIO
from django.contrib.messages import get_messages


class VisitantesViewsCoverageTests(TestCase):
    def setUp(self):
        # Usuários com diferentes perfis
        self.porteiro = mommy.make(Usuario, perfil=Usuario.Perfil.PORTEIRO)
        self.sindico = mommy.make(Usuario, perfil=Usuario.Perfil.SINDICO)
        self.conselho = mommy.make(Usuario, perfil=Usuario.Perfil.CONSELHO)

        # Cria o objeto Porteiro relacionado ao usuário
        self.porteiro_obj = mommy.make(Porteiros, usuario=self.porteiro)

        # Cliente logado como porteiro por padrão
        self.client.force_login(self.porteiro)

        # Visitante de exemplo registrado pelo porteiro
        self.visitante = mommy.make(
            Visitantes,
            nome_completo="Fulano Teste",
            cpf="12345678901",
            status="AGUARDANDO",
            registrado_por=self.porteiro_obj,
            horario_chegada=timezone.now()
        )

    # ---- registrar_visitantes ----
    def test_registrar_visitantes_get(self):
        url = reverse_lazy("visitantes:registrar_visitantes")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "registrar_visitante.html")

    def test_registrar_visitantes_post_valido(self):
        data = {
            "nome_completo": "Beltrano",
            "cpf": "98765432100",
            "data_nascimento": "01/06/1991",
            "numero_casa": self.visitante.numero_casa.id,
            "tipo": "INDEFINIDA",
        }

        resp = self.client.post(reverse_lazy("visitantes:registrar_visitantes"), data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Visitantes.objects.filter(nome_completo="Beltrano").exists())

    def test_registrar_visitantes_usuario_nao_porteiro(self):
        self.client.force_login(self.sindico)
        url = reverse_lazy("visitantes:registrar_visitantes")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    # ---- informacoes_visitantes ----
    def test_informacoes_visitantes_get(self):
        self.client.force_login(self.sindico)
        url = reverse_lazy("visitantes:informacoes_visitantes", args=[self.visitante.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_informacoes_visitantes_post_autoriza_invalido(self):
        self.client.force_login(self.sindico)
        url = reverse_lazy("visitantes:informacoes_visitantes", args=[self.visitante.id])
        data = {"morador_responsavel": "Nome Morador"}
        self.client.post(url, data)
        self.assertEqual(self.visitante.status, "AGUARDANDO")
        self.assertIsNone(self.visitante.horario_autorizacao)

    def test_informacoes_visitantes_post_autoriza(self):
        url = reverse_lazy("visitantes:informacoes_visitantes", args=[self.visitante.id])
        data = {"morador_responsavel": "Nome Morador"}
        self.client.post(url, data)
        self.visitante.refresh_from_db()
        self.assertEqual(self.visitante.status, "EM_VISITA")
        self.assertIsNotNone(self.visitante.horario_autorizacao)

    # ---- finalizar_visita ----
    def test_finalizar_visita_post_nao_autorizado(self):
        self.client.force_login(self.sindico)
        url = reverse_lazy("visitantes:finalizar_visita", args=[self.visitante.id])
        resp = self.client.post(url)
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Somente porteiros podem finalizar visitas")
        self.assertEqual(messages[0].level_tag, "warning")

    def test_finalizar_visita_post(self):
        url = reverse_lazy("visitantes:finalizar_visita", args=[self.visitante.id])
        self.client.post(url)
        self.visitante.refresh_from_db()
        self.assertEqual(self.visitante.status, "FINALIZADO")
        self.assertIsNotNone(self.visitante.horario_saida)

    def test_finalizar_visita_get_nao_permitido(self):
        url = reverse_lazy("visitantes:finalizar_visita", args=[self.visitante.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 405)  # HttpResponseNotAllowed

    # ---- exportar_visitas_csv ----
    def test_exportar_visitas_csv_com_permissao(self):
        self.client.force_login(self.sindico)
        url = reverse_lazy("visitantes:exportar_csv")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/csv")
 
        # Lê CSV
        content = StringIO(resp.content.decode())
        reader = csv.reader(content)
        header = next(reader)
        self.assertIn("Nome completo", header)

    def test_exportar_visitas_csv_com_permissao_e_filtros(self):
        self.client.force_login(self.sindico)
        data = {
            "inicio":"1990-01-1",
            "fim":"2029-01-1",
            "status":"EM_VISITA"
        }

        resp = self.client.get(reverse_lazy("visitantes:exportar_csv"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/csv")
  
        # Lê CSV
        content = StringIO(resp.content.decode())
        reader = csv.reader(content)
        header = next(reader)
        self.assertIn("Nome completo", header)

    def test_exportar_visitas_csv_sem_permissao(self):
        self.client.force_login(self.porteiro)
        url = reverse_lazy("visitantes:exportar_csv")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)