from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label=_("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_(
            'Sua senha deve atender aos seguintes critérios:<ul>'
            '<li>- Conter pelo menos 8 caracteres;</li>'
            '<li>- Não ser similar a informações pessoais;</li>'
            '<li>- Não ser uma senha comum;</li>'
            '<li>- Não ser totalmente numérica.</li>'
            '</ul>'
        ),
    )
    password2 = forms.CharField(
        label=_("Confirme a senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_("Digite a mesma senha novamente para confirmação."),
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'phone', 'country', 'profile_photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "E-mail"
        self.fields['role'].label = "Perfil"
        self.fields['profile_photo'].label = "Foto"
        self.fields['phone'].label = "Telefone"
        self.fields['country'].label = "País de origem"

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Senha", strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "E-mail"
        self.fields['password'].label = "Senha"

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'phone', 'country', 'profile_photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "E-mail"
        self.fields['role'].label = "Perfil"
        self.fields['profile_photo'].label = "Foto"
        self.fields['phone'].label = "Telefone"
        self.fields['country'].label = "País de origem"


