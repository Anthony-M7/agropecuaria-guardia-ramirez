from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from .forms import *

# Crea una vista de inicio de sesión que usa la plantilla predeterminada de Django
class CustomLoginView(LoginView):
    template_name = 'core/login.html' # Ruta a tu plantilla de login personalizada
    redirect_authenticated_user = True

# Crea una vista de cierre de sesión que redirige a la página principal
class CustomLogoutView(LogoutView):
    next_page = '/login/' # Redirige a la página principal después de cerrar sesión

def custom_user_add(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                # 1. Guarda el usuario primero
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                # 2. Guarda el perfil y lo asocia al usuario
                profile_instance = profile_form.save(commit=False)
                profile_instance.user = user
                profile_instance.save()
                
                return redirect(reverse('login'))
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/custom_add_user.html', context)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)