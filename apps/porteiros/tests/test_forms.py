from django.test import TestCase
from model_mommy import mommy
from apps.porteiros.forms import PorteirosForm


class PorteirosFormTests(TestCase):

    def setUp(self):
        # Usuários de teste
        self.porteiro = mommy.make("Usuario", perfil="PORTEIRO")
        self.sindico = mommy.make("Usuario", perfil="SINDICO")
        self.porteiro.save()
        self.sindico.save()

    def test_init_filtra_usuarios_com_perfil_porteiro(self):
        form = PorteirosForm()
        usuarios_qs = form.fields["usuario"].queryset
        self.assertIn(self.porteiro, usuarios_qs)
        self.assertNotIn(self.sindico, usuarios_qs)

    def test_valida_campos_obrigatorios(self):
        form = PorteirosForm(data={})
        self.assertFalse(form.is_valid())
        # Checa cada campo obrigatório
        for field in PorteirosForm.Meta.error_messages:
            self.assertIn(field, form.errors)
            self.assertEqual(
                form.errors[field][0], 
                PorteirosForm.Meta.error_messages.get(field)["required"]
            )

    def test_form_valido_com_dados_corretos(self):
        data = {
            "usuario": self.porteiro.pk,
            "nome_completo": "José da Silva",
            "cpf": "11122233344",
            "telefone": "21999999999",
            "data_nascimento": "1990-01-01"
        }

        form = PorteirosForm(data=data)
        self.assertTrue(form.is_valid())
        porteiro_obj = form.save()
        self.assertEqual(porteiro_obj.nome_completo, "José da Silva")
        self.assertEqual(porteiro_obj.usuario, self.porteiro)