from django.db import models


class Proprietarios(models.Model):
    nome_completo = models.CharField(
        verbose_name="Nome Completo",
        max_length=194,
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
    )

    telefone = models.CharField(
        verbose_name="Telefone do proprietário",
        max_length=11,
    )

    email = models.EmailField(
        verbose_name="Email do proprietário",
    )
    
    class Meta:
        verbose_name = "Proprietario"
        verbose_name_plural = "Proprietarios"
        db_table = "Proprietario"

    def __str__(self):
        return self.nome_completo
