from django.db import models


class Porteiros(models.Model):

    usuario = models.OneToOneField(
        "usuarios.Usuario",
        verbose_name="Usuario",
        on_delete=models.PROTECT,
    )

    nome_completo = models.CharField(
        verbose_name="Nome Completo",
        max_length=194,
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
    )

    telefone = models.CharField(
        verbose_name="Telefone do contato",
        max_length=11,
    )

    data_nascimento = models.DateField(
        verbose_name="Data de nascimento",
        auto_now=False,
        auto_now_add=False,
    )

    def get_cpf(self):
        if self.cpf:
            cpf_str = self.cpf
            return f"{cpf_str[0:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
        else:
            return "CPF não informado."

    class Meta:
        verbose_name = "Porteiro"
        verbose_name_plural = "Porteiros"
        db_table = "porteiro"

    def __str__(self):
        return self.nome_completo
