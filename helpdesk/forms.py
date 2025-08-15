from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AuthenticationForm,
    PasswordResetForm, SetPasswordForm
)
from django.forms import ClearableFileInput
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
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        self.fields['email'].label = "E-mail"
        self.fields['role'].label = "Perfil"
        self.fields['profile_photo'].label = "Foto"
        self.fields['phone'].label = "Telefone"
        self.fields['country'].label = "País de origem"

        if not self.request_user or not self.request_user.is_staff:
            self.fields['role'].choices = [('cliente', 'Cliente')]

        self.fields['phone'].widget.attrs.update({
            'placeholder': '(011) XXXXX-XXXX',
            'class': 'phone-input block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-blue-400 placeholder:text-gray-900 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-blue-600 sm:text-sm'
        })

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "E-mail"
        self.fields['password'].label = "Senha"

    def get_invalid_login_error(self):
        from django.core.exceptions import ValidationError
        return ValidationError(
            "E-mail ou senha inválidos. Insira os dados novamente.",
            code='invalid_login',
        )

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'

class CustomUserChangeForm(UserChangeForm):
    password = None

    profile_photo = forms.ImageField(
        label="Foto",
        required=False,
        widget=CustomClearableFileInput(attrs={'class': 'custom-file-input'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'phone', 'country', 'profile_photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "E-mail"
        self.fields['role'].label = "Perfil"
        self.fields['phone'].label = "Telefone"
        self.fields['country'].label = "País de origem"

        if not self.instance.is_superuser:
            self.fields['role'].choices = [('cliente', 'Cliente')]

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("E-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline outline-1 -outline-offset-1 outline-blue-400 focus:outline-2 focus:outline-blue-600 sm:text-sm',
            'placeholder': 'Digite seu e-mail'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Nova senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline outline-1 -outline-offset-1 outline-blue-400 focus:outline-2 focus:outline-blue-600 sm:text-sm',
            'placeholder': 'Digite a nova senha'
        }),
        help_text=_(
            'Sua senha deve atender aos seguintes critérios:<ul>'
            '<li>- Conter pelo menos 8 caracteres;</li>'
            '<li>- Não ser similar a informações pessoais;</li>'
            '<li>- Não ser uma senha comum;</li>'
            '<li>- Não ser totalmente numérica.</li>'
            '</ul>'
        ),
    )
    new_password2 = forms.CharField(
        label=_("Confirme a senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline outline-1 -outline-offset-1 outline-blue-400 focus:outline-2 focus:outline-blue-600 sm:text-sm',
            'placeholder': 'Confirme a nova senha'
        }),
    )

