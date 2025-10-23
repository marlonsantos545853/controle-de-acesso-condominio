# apps/porteiros/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from model_mommy import mommy
from porteiros.models import Porteiros
from usuarios.models import Usuario


Usuario = get_user_model()

class PorteirosViewsCoverageTests(TestCase):
    def setUp(self):
        # cria usuários com perfis diferentes
        self.sindico = mommy.make(Usuario, perfil=Usuario.Perfil.SINDICO)
        self.porteiro_user = mommy.make(Usuario, perfil=Usuario.Perfil.PORTEIRO)
        self.client.force_login(self.sindico)
        # cria um porteiro para edição
        self.porteiro = mommy.make(Porteiros, usuario=self.porteiro_user)

    # ---- cadastrar_porteiro ----
    def test_cadastrar_porteiro_get(self):
        url = reverse("porteiros:cadastrar_porteiro")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_cadastrar_porteiro_post_valido(self):
        novo_usuario = mommy.make(Usuario, perfil=Usuario.Perfil.PORTEIRO)
        url = reverse("porteiros:cadastrar_porteiro")
        data = {
            "usuario": novo_usuario.id,
            "nome_completo": "Fulano Teste",
            "cpf": "11122233344",
            "telefone": "21999999999",
            "data_nascimento": "1990-01-01"
        }

        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Porteiros.objects.count(), 2)

    def test_cadastrar_porteiro_usuario_nao_sindico(self):
        self.client.force_login(self.porteiro_user)
        url = reverse("porteiros:cadastrar_porteiro")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    # ---- editar_porteiro ----
    def test_editar_porteiro_post_valido(self):
        url = reverse("porteiros:editar_porteiro", kwargs={"porteiro_id": self.porteiro.id})
        data = {
            "usuario": self.porteiro.usuario.id,
            "nome_completo": "Nome Editado",
            "cpf": self.porteiro.cpf,
            "telefone": self.porteiro.telefone,
            "data_nascimento": self.porteiro.data_nascimento,
        }

        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)

    def test_editar_porteiro_usuario_nao_sindico_dispara_warning(self):
        self.client.force_login(self.porteiro_user)
        url = reverse("porteiros:editar_porteiro", kwargs={"porteiro_id": self.porteiro.id})
        data = {
            "usuario": self.porteiro.usuario.id,
            "nome_completo": "Nome Editado",
            "cpf": self.porteiro.cpf,
            "telefone": self.porteiro.telefone,
            "data_nascimento": self.porteiro.data_nascimento,
        }

        resp = self.client.post(url, data, follow=True)
        mensagens = [m.message for m in resp.context["messages"]]
        self.assertIn("Somente o síndico pode editar o porteiro", mensagens)

    def test_editar_porteiro_post_invalido_render_form(self):
        url = reverse("porteiros:editar_porteiro", kwargs={"porteiro_id": self.porteiro.id})
        data = {
            "usuario": "",  # inválido
            "nome_completo": "",
            "cpf": "",
            "telefone": "",
            "data_nascimento": "",
        }
        
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "includes/form/form_geral.html")

    # ---- visualizar_porteiros ----
    def test_visualizar_porteiros(self):
        url = reverse("porteiros:visualizar_porteiros")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "includes/tabela/tabela_geral.html")
