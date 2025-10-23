from django.test import TestCase
from model_mommy import mommy

class ProprietariosModelsTests(TestCase):
    def setUp(self):
        self.proprietario = mommy.make('Proprietarios')

    def test_str(self):
        self.assertEqual(str(self.proprietario), self.proprietario.nome_completo)