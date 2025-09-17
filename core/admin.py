from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define un Inline para el modelo Profile
class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    # Puedes añadir los campos que quieres mostrar, excluyendo el 'user' ya que se manejará automáticamente
    fields = ['telefono', 'nivel_usuario', 'cargo', 'salario', 'fecha_contratacion', 'estado', 'foto_perfil']


# Define una clase UserAdmin para controlar la vista de usuario
class MyUserAdmin(BaseUserAdmin):
    # Sobrescribe el 'fieldsets' para mostrar solo los campos deseados
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
        # Puedes añadir más fieldsets si lo deseas, por ejemplo, para permisos
    )
    inlines = (ProfileInline,)

# Desregistra el UserAdmin por defecto
admin.site.unregister(User)

# Registra el nuevo MyUserAdmin
admin.site.register(User, MyUserAdmin)