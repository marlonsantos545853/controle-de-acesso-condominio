from django import forms
from visitantes.models import Visitantes


class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitantes
        fields = [
            "nome_completo",
            "cpf",
            "data_nascimento",
            "numero_casa",
            "tipo",
            "placa_veiculo",
        ]

        error_messages = {
            "nome_completo": {
                "required": (
                    "O nome completo do visitante é obrigatorio" " para o registro"
                )
            },
            "cpf": {
                "required": ("O nome cpf do visitante e obrigatorio " "para o registro")
            },
            "data_nascimento": {
                "required": (
                    "A data de nascimento do visitante e " "obrigatoria para o registro"
                ),
                "invalid": (
                    "Por favor, informe um formato valido "
                    "para a data de nascimento (DD/MM/AAAA)"
                ),
            },
            "tipo": {"required": ("Por favor, informe o tipo de visita")},
            "numero_casa": {
                "required": ("Por favor, Informe o número da casa a ser " "visitada")
            },
        }


class AutorizaVisitanteForm(forms.ModelForm):
    morador_responsavel = forms.CharField(required=True)

    class Meta:
        model = Visitantes
        fields = ["morador_responsavel"]
        error_messages = {
            "morador_responsavel": {
                "required": (
                    "Por favor, informe o nome do morador responsavel "
                    "por autorizar a entrada do visitante."
                )
            },
        }
