# apps/proprietarios/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from usuarios.models import Usuario
from proprietarios.models import Proprietarios


class ProprietariosViewsCoverageTests(TestCase):
    def setUp(self):
        # Usuários com perfis diferentes
        self.sindico = mommy.make(Usuario, perfil=Usuario.Perfil.SINDICO)
        self.conselho = mommy.make(Usuario, perfil=Usuario.Perfil.CONSELHO)
        self.client.force_login(self.sindico)

        # Proprietário para edição
        self.proprietario = mommy.make(Proprietarios)

    # ---- cadastrar_proprietario ----
    def test_cadastrar_proprietario_get(self):
        url = reverse("proprietarios:cadastrar_proprietario")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_cadastrar_proprietario_post_valido(self):
        url = reverse("proprietarios:cadastrar_proprietario")
        data = {
            "nome_completo": "Fulano Teste",
            "cpf": "11122233344",
            "telefone": "21999999999",
            "email": "teste@example.com"
        }

        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Proprietarios.objects.count(), 2)  # já existia 1

    def test_cadastrar_proprietario_usuario_nao_sindico(self):
        self.client.force_login(self.conselho)
        url = reverse("proprietarios:cadastrar_proprietario")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    # ---- editar_proprietario ----
    def test_editar_proprietario_post_valido(self):
        url = reverse(
            "proprietarios:editar_proprietario", 
            kwargs={"proprietario_id": self.proprietario.id}
        )

        data = {
            "nome_completo": "Nome Editado",
            "cpf": self.proprietario.cpf,
            "telefone": self.proprietario.telefone,
            "email": self.proprietario.email,
        }

        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)

    def test_editar_proprietario_usuario_nao_sindico_dispara_warning(self):
        self.client.force_login(self.conselho)
        url = reverse(
            "proprietarios:editar_proprietario", 
            kwargs={"proprietario_id": self.proprietario.id}
        )

        data = {
            "nome_completo": "Nome Editado",
            "cpf": self.proprietario.cpf,
            "telefone": self.proprietario.telefone,
            "email": self.proprietario.email,
        }

        resp = self.client.post(url, data, follow=True)
        mensagens = [m.message for m in resp.context["messages"]]
        self.assertIn("Somente o síndico pode editar o proprietário", mensagens)

    def test_editar_proprietario_post_invalido_render_form(self):
        url = reverse(
            "proprietarios:editar_proprietario", 
            kwargs={"proprietario_id": self.proprietario.id}
        )

        data = {
            "nome_completo": "",
            "cpf": "",
            "telefone": "",
            "email": "",
        }

        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "includes/form/form_geral.html")

    # ---- visualizar_proprietarios ----
    def test_visualizar_proprietarios(self):
        url = reverse("proprietarios:visualizar_proprietarios")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "includes/tabela/tabela_geral.html")
