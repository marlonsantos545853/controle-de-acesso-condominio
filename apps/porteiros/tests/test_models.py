from django.test import TestCase
from model_mommy import mommy

class PorteirosModelsTests(TestCase):

    def setUp(self):
        self.porteiro = mommy.make('Porteiros')
        self.porteiro.cpf = "11122233344"
    
    def test_get_cpf_quando_existe(self):
        self.porteiro.cpf = '11122233344'
        self.assertEqual(self.porteiro.get_cpf(), "111.222.333-44")

    def test_get_cpf_quando_vazio(self):
        self.porteiro.cpf = ""
        self.assertEqual(self.porteiro.get_cpf(), "CPF não informado.")

    def test_str(self):
        self.assertEqual(str(self.porteiro), self.porteiro.nome_completo)