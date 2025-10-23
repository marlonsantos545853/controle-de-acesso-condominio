from django.test import TestCase
from model_mommy import mommy
from datetime import datetime


class VisitantesModelTests(TestCase):
    def setUp(self):
        self.visitante = mommy.make('Visitantes')

    def test_str(self):
        self.assertEqual(str(self.visitante), self.visitante.nome_completo)

    # --- CPF ---
    def test_get_cpf_quando_existe(self):
        self.visitante.cpf = '11122233344'
        self.assertEqual(self.visitante.get_cpf(), "111.222.333-44")

    def test_get_cpf_quando_vazio(self):
        self.visitante.cpf = ""
        self.assertEqual(self.visitante.get_cpf(), "CPF não informado.")

    # --- Morador responsável ---
    def test_get_morador_responsavel_quando_existe(self):
        self.visitante.morador_responsavel = "João da Silva"
        self.assertEqual(self.visitante.get_morador_responsavel(), "João da Silva")

    def test_get_morador_responsavel_quando_vazio(self):
        self.visitante.morador_responsavel = ""
        self.assertEqual(self.visitante.get_morador_responsavel(), "Aguardando autorização.")

    # --- Horário de autorização ---
    def test_get_horario_autorizacao_quando_existe(self):
        self.visitante.horario_autorizacao = datetime(2025, 9, 24, 10, 0)
        self.assertEqual(
            self.visitante.get_horario_autorizacao(),
            datetime(2025, 9, 24, 10, 0)
        )

    def test_get_horario_autorizacao_quando_vazio(self):
        self.visitante.horario_autorizacao = None
        self.assertEqual(self.visitante.get_horario_autorizacao(), "Aguardando autorização.")

    # --- Horário de saída ---
    def test_get_horario_saida_quando_existe(self):
        self.visitante.horario_saida = datetime(2025, 9, 24, 18, 0)
        self.assertEqual(
            self.visitante.get_horario_saida(),
            datetime(2025, 9, 24, 18, 0)
        )

    def test_get_horario_saida_quando_vazio(self):
        self.visitante.horario_saida = None
        self.assertEqual(self.visitante.get_horario_saida(), "Saida não informada.")

    # --- Placa veículo ---
    def test_get_placa_veiculo_quando_existe(self):
        self.visitante.placa_veiculo = "ABC1234"
        self.assertEqual(self.visitante.get_placa_veiculo(), "ABC1234")

    def test_get_placa_veiculo_quando_vazio(self):
        self.visitante.placa_veiculo = None
        self.assertEqual(self.visitante.get_placa_veiculo(), "Veículo não informado.")
