from django import forms
from proprietarios.models import Proprietarios


class ProprietariosForm(forms.ModelForm):

    class Meta:
        model = Proprietarios
        fields = ["nome_completo", "cpf", "telefone", "email"]

        error_messages = {
            "nome_completo": {"required": ("Por favor, informe o nome completo")},
            "cpf": {"required": ("Por favor, informe o CPF")},
            "telefone": {"required": ("Por favor, informe o telefone")},
            "email": {"required": ("Por favor, informe o email")},
        }
