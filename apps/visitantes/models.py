from django.db import models
from unidades.models import Unidade


class Visitantes(models.Model):
    STATUS_VISITANTE = [
        ("AGUARDANDO", "Aguardando autorização"),
        ("EM_VISITA", "Em visita"),
        ("FINALIZADO", "Visita finalizada"),
    ]

    TIPO_VISITANTE = [
        ("INDEFINIDA", "Visita não identificada"),
        ("ENTREGA", "Visita para entregas"),
        ("TECNICA", "Visita para prestação de serviços"),
        ("FAMILIAR", "Visita de amigos ou familiares"),
    ]

    status = models.CharField(
        verbose_name="Status",
        max_length=10,
        choices=STATUS_VISITANTE,
        default="AGUARDANDO",
    )

    tipo = models.CharField(
        verbose_name="Tipo", max_length=15, choices=TIPO_VISITANTE, default="INDEFINIDA"
    )

    nome_completo = models.CharField(
        verbose_name="Nome completo",
        max_length=194,
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
    )

    data_nascimento = models.DateField(
        verbose_name="Data de nascimento",
        auto_now_add=False,
        auto_now=False,
    )

    numero_casa = models.ForeignKey(
        Unidade,
        verbose_name="Numero da unidade a ser visitada",
        on_delete=models.PROTECT,
    )

    placa_veiculo = models.CharField(
        verbose_name="Placa de veiculo",
        max_length=7,
        blank=True,
        null=True,
    )

    horario_chegada = models.DateTimeField(
        verbose_name="Horario de chegada na portaria",
        auto_now_add=True,
    )

    horario_saida = models.DateTimeField(
        verbose_name="Horario de saida",
        auto_now=False,
        blank=True,
        null=True,
    )

    horario_autorizacao = models.DateTimeField(
        verbose_name="Horario de autorizacao de entrada",
        auto_now=False,
        blank=True,
        null=True,
    )

    morador_responsavel = models.CharField(
        verbose_name="Nome do morador responsavel por autorizador a entrada do visitante",
        max_length=194,
        blank=True,
    )

    registrado_por = models.ForeignKey(
        "porteiros.Porteiros",
        verbose_name="Porteiro responsavel pelo registro",
        on_delete=models.PROTECT,
    )
    
    def get_morador_responsavel(self):
        if self.morador_responsavel:
            return self.morador_responsavel
        else:
            return "Aguardando autorização."

    def get_horario_autorizacao(self):
        if self.horario_autorizacao:
            return self.horario_autorizacao
        else:
            return "Aguardando autorização."

    def get_horario_saida(self):
        if self.horario_saida:
            return self.horario_saida
        else:
            return "Saida não informada."

    def get_placa_veiculo(self):
        if self.placa_veiculo:
            return self.placa_veiculo
        else:
            return "Veículo não informado."

    def get_cpf(self):
        if self.cpf:
            cpf_str = self.cpf
            return f"{cpf_str[0:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
        else:
            return "CPF não informado."

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"
        db_table = "visitante"

    def __str__(self):
        return self.nome_completo
