# apps/usuarios/tests/test_views.py
from django.test import TestCase
from django.urls import reverse_lazy
from model_mommy import mommy
from usuarios.models import Usuario
from django.contrib import messages

class UsuarioViewsCoverageTests(TestCase):
    def setUp(self):
        # Usuários com diferentes perfis
        self.sindico = mommy.make(Usuario, perfil=Usuario.Perfil.SINDICO)
        self.admin = mommy.make(Usuario, perfil=Usuario.Perfil.ADMINISTRADOR)
        self.porteiro = mommy.make(Usuario, perfil=Usuario.Perfil.PORTEIRO)
        self.conselho = mommy.make(Usuario, perfil=Usuario.Perfil.CONSELHO)
        self.usuario_editado = mommy.make(Usuario, perfil=Usuario.Perfil.CONSELHO)
        self.client.force_login(self.sindico)

    # ---- cadastrar_usuario ----
    def test_cadastrar_usuario_get(self):
        url = reverse_lazy("usuarios:cadastrar_usuario")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_cadastrar_usuario_post_valido(self):
        url = reverse_lazy("usuarios:cadastrar_usuario")
        data = {"email": "teste@example.com", "perfil": Usuario.Perfil.CONSELHO, "password": "12sasdsk23"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)

    def test_cadastrar_usuario_nao_permitido(self):
        self.client.force_login(self.porteiro)
        url = reverse_lazy("usuarios:cadastrar_usuario")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    # # ---- editar_usuario ----
    def test_editar_usuario_get(self):
        url = reverse_lazy("usuarios:editar_usuario", kwargs={"usuario_id": self.admin.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_editar_usuario_perfil_admin_warning(self):
        self.client.force_login(self.sindico)
        url = reverse_lazy("usuarios:editar_usuario", kwargs={"usuario_id": self.admin.id})
        data = {"email": self.admin.email, "perfil": Usuario.Perfil.PORTEIRO}
        resp = self.client.post(url, data, follow=True)
        mensagens = [m.message for m in resp.context["messages"]]
        self.assertIn("Perfil de Administrador não pode ser editado.", mensagens)

    def test_editar_usuario_nao_permitido_warning(self):
        self.client.force_login(self.conselho)
        url = reverse_lazy("usuarios:editar_usuario", kwargs={"usuario_id": self.porteiro.id})
        data = {"email": self.porteiro.email, "perfil": Usuario.Perfil.CONSELHO}
        resp = self.client.post(url, data, follow=True)
        mensagens = [m.message for m in resp.context["messages"]]
        self.assertIn("Somente o síndico pode editar o usuários", mensagens)

    def test_editar_usuario_post_valido(self):
        url = reverse_lazy("usuarios:editar_usuario", kwargs={"usuario_id": self.usuario_editado.id})
        data = {
            "email": "novoemail@example.com",
            "perfil": self.usuario_editado.perfil,
            "password": "",  # vazio para manter a senha antiga
        }

        resp = self.client.post(url, data)
        
        # Verifica redirecionamento
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse_lazy("usuarios:visualizar_usuarios"))

        # Recarrega usuário do DB e verifica alteração
        self.usuario_editado.refresh_from_db()
        self.assertEqual(self.usuario_editado.email, "novoemail@example.com")

        # Verifica se a mensagem de sucesso foi adicionada
        messages_list = list(messages.get_messages(resp.wsgi_request))
        self.assertTrue(any("Usuario editado com sucesso" in str(m) for m in messages_list))

    # # ---- visualizar_usuarios ----
    def test_visualizar_usuarios(self):
        url = reverse_lazy("usuarios:visualizar_usuarios")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "includes/tabela/tabela_geral.html")

    # # ---- atualiza_senha_usuario ----
    def test_atualiza_senha_usuario_get(self):
        url = reverse_lazy("usuarios:atualiza_senha_usuario")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "index.html")

    def test_atualiza_senha_usuario_post_valido(self):
        url = reverse_lazy("usuarios:atualiza_senha_usuario")
        data = {"password": "nova_senha123"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)

    def test_atualiza_senha_usuario_post_invalido(self):
        url = reverse_lazy("usuarios:atualiza_senha_usuario")
        data = {"password": "123"}  # menor que 6 caracteres
        resp = self.client.post(url, data, follow=True)
        mensagens = [m.message for m in resp.context["messages"]]
        self.assertIn("A senha deve conter no mínimo 6 caracteres", mensagens)
