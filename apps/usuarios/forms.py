from django import forms
from usuarios.models import Usuario


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha", widget=forms.PasswordInput, required=False
    )

    class Meta:
        model = Usuario
        fields = ["email", "perfil", "password"]
        error_messages = {
            "email": {"required": ("O email é obrigatório")},
            "perfil": {"required": ("Informe o perfil que deve do usuário")},
            "password": {"required": ("Por favor, informe uma senha")},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Armazena a senha original (hashed) se for uma edição
        if self.instance and self.instance.pk:
            self._senha_antiga = self.instance.password
            self._perfil = self.instance.perfil
        else:
            self._senha_antiga = None
            self._perfil = None
        
        self.fields["perfil"].choices = [
            (value, label)
            for value, label in self.fields["perfil"].choices
            if value != Usuario.Perfil.ADMINISTRADOR
        ]

    def perfil(self):
        return self._perfil

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get("password")
        if pwd and pwd.strip():
            user.set_password(pwd)
        else:
            # Mantém a senha antiga se o campo estiver vazio
            user.password = self._senha_antiga

        if commit:
            user.save()

        return user


class TrocarSenhaUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput, 
        min_length=6, 
        required=True,
        error_messages={"required": "Por favor, informe uma senha"}
    )

    class Meta:
        model = Usuario
        fields = ["password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Armazena a senha original (hashed) se for uma edição
        if self.instance and self.instance.pk:
            self._senha_antiga = self.instance.password
        else:
            self._perfil = None

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get("password")
        if pwd and len(pwd.strip()) > 6:
            user.set_password(pwd)
        else:
            # Mantém a senha antiga se o campo estiver vazio
            user.password = self._senha_antiga # pragma: no cover

        if commit:
            user.save()

        return user
