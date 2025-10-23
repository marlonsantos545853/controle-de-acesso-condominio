from django.test import TestCase
from model_mommy import mommy
from django.contrib.auth import get_user_model


class UsuarioModelsTests(TestCase):
    def setUp(self):
        self.usuario = mommy.make('Usuario')

    def test_get_perfil_emal(self):
        self.assertEqual(self.usuario.get_perfil_login(), f"{self.usuario.email} [ {self.usuario.get_perfil_display()} ]")

    def test_str(self):
        self.assertEqual(str(self.usuario), self.usuario.email)


class UsuarioManagerTests(TestCase):
    def setUp(self):
        self.Usuario = get_user_model()

    def test_create_user(self):
        # Arrange & Act
        user = self.Usuario.objects.create_user(
            email="teste@exemplo.com", password="senha123"
        )

        # Assert
        self.assertEqual(user.email, "teste@exemplo.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("senha123"))  # senha foi criptografada

    def test_create_user_without_password(self):
        user = self.Usuario.objects.create_user(email="nopass@exemplo.com")
        self.assertTrue(user.is_active)
        self.assertEqual(user.password, '')

    def test_create_superuser(self):
        superuser = self.Usuario.objects.create_superuser(
            email="admin@exemplo.com", password="admin123"
        )

        self.assertEqual(superuser.email, "admin@exemplo.com")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password("admin123"))