from django.test import SimpleTestCase
from dashboard.templatetags import core_tags  # ajuste para o nome do seu arquivo

class CoreTemplatetagsTests(SimpleTestCase):
    def test_get_existing_key(self):
        d = {"nome": "Maria"}
        self.assertEqual(core_tags.get_item(d, "nome"), "Maria")

    def test_get_missing_key(self):
        d = {"idade": 30}
        self.assertEqual(core_tags.get_item(d, "nome"), "")