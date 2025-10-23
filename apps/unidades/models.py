from django.db import models
from proprietarios.models import Proprietarios


class Unidade(models.Model):
    bloco = models.CharField(
        verbose_name="Bloco da casa ou apartamento",
        max_length=192,
        blank=True,
        null=True,
    )

    numero = models.CharField(
        verbose_name="Numero da casa ou apartamento a ser visitado",
        max_length=192,
    )

    proprietario = models.ForeignKey(
        Proprietarios,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        bloco = self.bloco if self.bloco else ""
        return f"{bloco} {self.numero}"
