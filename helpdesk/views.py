from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm


def home(request):
    return render(request, 'home.html')

def auth_view(request):
    signup_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm(request=request)
    signup_submitted = False

    if request.method == 'POST':
        if 'signup_submit' in request.POST:
            signup_form = CustomUserCreationForm(request.POST, request.FILES)
            signup_submitted = True
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.role = 'cliente'
                user.save()
                login(request, user)
                messages.success(request, "Conta criada com sucesso.")
                return redirect('home')

        elif 'login_submit' in request.POST:
            login_form = CustomAuthenticationForm(request=request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, "Login realizado com sucesso.")
                return redirect('home')
            else:
                messages.error(request, "E-mail ou senha inválidos. Insira os dados novamente.")

    return render(request, 'login.html', {
        'signup_form': signup_form,
        'login_form': login_form,
        'signup_submitted': signup_submitted
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da conta.")
    return redirect('home')

@login_required(login_url='home')
def profile_view(request):
    if request.method == 'POST':
        edit_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user, request_user=request.user)
        if edit_form.is_valid():
            if request.user.role != 'superadm':
                edit_form.instance.role = edit_form.instance.role
            edit_form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('profile')
    else:
        edit_form = CustomUserChangeForm(instance=request.user, request_user=request.user)

    return render(request, 'profile.html', {'edit_form': edit_form})

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'suporte':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@staff_required
def staff_user_create(request):
    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST, request.FILES, request_user=request.user)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, "Usuário Staff criado com sucesso.")
            return redirect('staff_user_create')
        else:
            messages.error(request, "Erro ao criar usuário. Verifique os campos.")
    else:
        signup_form = CustomUserCreationForm(request_user=request.user)

    return render(request, 'staff_user_create.html', {'signup_form': signup_form})




