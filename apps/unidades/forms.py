from django import forms
from unidades.models import Unidade


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ["bloco", "numero", "proprietario"]
        error_messages = {
            "numero": {"required": ("Informe o número da unidade")},
            "proprietario": {"required": ("Por favor, informe o usuário proprietario")},
        }
