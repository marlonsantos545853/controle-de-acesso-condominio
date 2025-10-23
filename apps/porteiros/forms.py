from django import forms
from porteiros.models import Porteiros
from usuarios.models import Usuario


class PorteirosForm(forms.ModelForm):

    class Meta:
        model = Porteiros
        fields = ["usuario", "nome_completo", "cpf", "telefone", "data_nascimento"]
        error_messages = {
            "usuario": {"required": ("Informe a conta de usuário")},
            "nome_completo": {"required": ("Por favor, informe o nome completo")},
            "cpf": {"required": ("Por favor, informe o CPF")},
            "telefone": {"required": ("Por favor, informe o telefone")},
            "data_nascimento": {
                "required": ("Por favor, informe a data de nascimento")
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["usuario"].queryset = Usuario.objects.filter(
            perfil=Usuario.Perfil.PORTEIRO
        )
