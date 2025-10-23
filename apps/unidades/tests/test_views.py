# apps/unidades/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from model_mommy import mommy
from unidades.models import Unidade
from proprietarios.models import Proprietarios  # ajuste se o app for outro


Usuario = get_user_model()

class UnidadeViewsCoverageTests(TestCase):
    def setUp(self):
        self.sindico = mommy.make(Usuario, perfil=Usuario.Perfil.SINDICO)
        self.porteiro = mommy.make(Usuario, perfil=Usuario.Perfil.PORTEIRO)
        self.proprietario = mommy.make(Proprietarios)  # 👈 cria proprietário válido
        self.client.force_login(self.sindico)

    def test_cadastrar_unidade_get(self):
        url = reverse("unidades:cadastrar_unidade")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_cadastrar_unidade_post_valido(self):
        url = reverse("unidades:cadastrar_unidade")
        data = {"bloco": "A", "numero": "101", "proprietario": self.proprietario.id}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Unidade.objects.count(), 1)

    def test_cadastrar_unidade_usuario_nao_sindico(self):
        self.client.force_login(self.porteiro)
        url = reverse("unidades:cadastrar_unidade")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_editar_unidade_post_valido(self):
        unidade = mommy.make(Unidade, proprietario=self.proprietario)
        url = reverse("unidades:editar_unidade", kwargs={"unidade_id": unidade.id})
        resp = self.client.post(url, {
            "bloco": "B",
            "numero": "202",
            "proprietario": self.proprietario.id,
        })
        self.assertEqual(resp.status_code, 302)

    def test_visualizar_unidades(self):
        mommy.make(Unidade, proprietario=self.proprietario)
        url = reverse("unidades:visualizar_unidades")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_editar_unidade_usuario_nao_sindico_dispara_warning(self):
        # cria unidade
        unidade = mommy.make(Unidade, proprietario=self.proprietario)

        # loga como usuário que não é síndico
        self.client.force_login(self.porteiro)

        url = reverse("unidades:editar_unidade", kwargs={"unidade_id": unidade.id})

        # faz POST mesmo que válido, mas o perfil é diferente
        resp = self.client.post(url, {
            "bloco": "C",
            "numero": "303",
            "proprietario": self.proprietario.id,
        }, follow=True)

        # redireciona para a lista
        self.assertEqual(resp.status_code, 200)

        # verifica se a mensagem foi adicionada
        mensagens = [m.message for m in resp.context["messages"]]
        self.assertIn("Somente o síndico pode editar a unidade", mensagens)

    def test_editar_unidade_render_form_quando_invalido(self):
        # cria unidade
        unidade = mommy.make(Unidade, proprietario=self.proprietario)

        # loga como síndico (tem permissão)
        self.client.force_login(self.sindico)

        url = reverse("unidades:editar_unidade", kwargs={"unidade_id": unidade.id})

        # envia dados incompletos (form inválido)
        resp = self.client.post(url, {
            "bloco": "",  # campo obrigatório vazio
            "numero": "",
            "proprietario": "",  
        })

        # verifica que renderizou o template do form
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "includes/form/form_geral.html")