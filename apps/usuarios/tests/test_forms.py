from django.test import TestCase
from model_mommy import mommy
from apps.usuarios.forms import UsuarioForm
from apps.usuarios.forms import TrocarSenhaUsuarioForm


class UsuarioFormTests(TestCase):
    def setUp(self):
        self.usuario = mommy.make("Usuario", email="teste1@example.com", perfil="ADMINISTRADOR")
        self.usuario.set_password("senha_antiga")
        self.usuario.save()

    def test_init_com_usuario_existente(self):
        form = UsuarioForm(instance=self.usuario)
        self.assertEqual(form._senha_antiga, self.usuario.password)
        self.assertEqual(form._perfil, self.usuario.perfil)

    def test_init_sem_usuario(self):
        form = UsuarioForm()
        self.assertIsNone(form._senha_antiga)
        self.assertIsNone(form._perfil)

    def test_perfil_retorna_valor_do_init(self):
        form = UsuarioForm(instance=self.usuario)
        self.assertEqual(form.perfil(), self.usuario.perfil)

    def test_save_com_nova_senha(self):
        data = {"email": "novo@example.com", "perfil": "SINDICO", "password": "nova_senha"}
        form = UsuarioForm(data, instance=self.usuario)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password("nova_senha"))

    def test_save_sem_senha_mantem_antiga(self):
        data = {"email": "novo@example.com", "perfil": "SINDICO", "password": ""}
        form = UsuarioForm(data, instance=self.usuario)
        self.assertTrue(form.is_valid())
        user = form.save()
        # Continua com a senha antiga
        self.assertTrue(user.check_password("senha_antiga"))


class TrocarSenhaUsuarioFormTests(TestCase):
    def setUp(self):
        self.usuario = mommy.make("Usuario", email="teste2@example.com")
        self.usuario.set_password("senha_antiga")
        self.usuario.save()

    def test_init_com_usuario_existente(self):
        form = TrocarSenhaUsuarioForm(instance=self.usuario)
        self.assertEqual(form._senha_antiga, self.usuario.password)

    def test_save_com_nova_senha_valida(self):
        data = {"password": "nova_senha123"}
        form = TrocarSenhaUsuarioForm(data, instance=self.usuario)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password("nova_senha123"))

    def test_init_sem_instance_define_perfil_none(self):
        form = TrocarSenhaUsuarioForm()  # sem instance
        self.assertIsNone(form._perfil)

    def test_campo_password_obrigatorio(self):
        form = TrocarSenhaUsuarioForm(data={}, instance=self.usuario)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)
        self.assertEqual(
            form.errors["password"][0],
            "Por favor, informe uma senha"
        )