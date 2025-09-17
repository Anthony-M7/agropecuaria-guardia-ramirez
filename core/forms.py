from django.contrib.auth.models import User
from core.models import Profile
from django import forms

# Crea un formulario para el modelo de Usuario
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput()
        }

# Crea un formulario para el modelo de Perfil
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telefono', 'nivel_usuario', 'cargo', 'salario', 'fecha_contratacion', 'estado', 'foto_perfil']

    fecha_contratacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    foto_perfil = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))  # Hacer que la foto de perfil sea opcional