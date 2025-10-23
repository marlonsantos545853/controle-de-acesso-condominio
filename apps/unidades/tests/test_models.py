from django.test import TestCase
from model_mommy import mommy

class UnidadesModelsTests(TestCase):
    def setUp(self):
        self.unidade = mommy.make('Unidade')

    def test_str(self):
        bloco = self.unidade.bloco if self.unidade.bloco else "" 
        self.assertEqual(str(self.unidade), f"{bloco} {self.unidade.numero}")