from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password

class UsuarioManage(BaseUserManager):
    def create_user(self, email, password=None):
        usuario = self.model(email=self.normalize_email(email))
        usuario.is_active = True
        usuario.is_staff = False
        usuario.is_superuser = False
        if password:
            usuario.set_password(password)

        usuario.save()

        return usuario

    def create_superuser(self, email, password):
        usuario = self.create_user(email=self.normalize_email(email), password=password)
        usuario.is_active = True
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.set_password(password)
        usuario.save()

        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Perfil(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        PORTEIRO = "PORTEIRO", "Porteiro"
        CONSELHO = "CONSELHO", "Conselho"
        SINDICO = "SINDICO", "Síndico"

    email = models.EmailField(
        verbose_name="E-mail do usuário",
        max_length=194,
        unique=True,
    )

    is_active = models.BooleanField(
        verbose_name="Usuário está ativo",
        default=True,
    )

    is_staff = models.BooleanField(
        verbose_name="Usuário é da equipe de desenvolvimento",
        default=False,
    )

    is_superuser = models.BooleanField(
        verbose_name="Usuário é um superusuário",
        default=False,
    )

    perfil = models.CharField(
        verbose_name="Perfil do usuário",
        max_length=20,
        choices=Perfil.choices,
        default=Perfil.ADMINISTRADOR,
    )

    def get_perfil_login(self):
        return str(f"{self.email} [ {self.get_perfil_display()} ]")

    USERNAME_FIELD = "email"
    objects = UsuarioManage()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = "usuario"

    def save(self, *args, **kwargs):
        # Se a senha não estiver criptografada, aplica o hash
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
