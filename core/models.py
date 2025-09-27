# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings # ¡Importante!
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.core.files.storage import FileSystemStorage

# Define el almacenamiento local solo si estás en modo de desarrollo.
# Usa os.path para evitar problemas con las rutas en diferentes sistemas operativos.
if settings.DEBUG:
    from django.conf import settings as settings_file
    fs = FileSystemStorage(location=settings_file.MEDIA_ROOT)
else:
    # Si no estás en modo de depuración, usa Cloudinary.
    fs = MediaCloudinaryStorage()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    telefono = models.CharField(max_length=20, blank=True)
    nivel_usuario = models.CharField(choices=[("admin", "Admin"), ("usuario", "Usuario"), ("invitado", "Invitado")], blank=True)
    cargo = models.CharField(choices=[("gerente", "Gerente"), ("supervisor", "Supervisor"), ("empleado", "Empleado")], blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)
    estado = models.CharField(choices=[("activo", "Activo"), ("inactivo", "Inactivo"), ("suspendido", "Suspendido")], blank=True)
    foto_perfil =  models.ImageField(
        upload_to='profiles_pictures/',
        storage=fs,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username