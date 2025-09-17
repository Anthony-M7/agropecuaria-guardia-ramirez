"""
Django settings for central_proyect project.
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Configuración de Correo Electrónico (Backend de Consola para desarrollo)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # Si usas Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'comercializadoraagroguardia@gmail.com'
EMAIL_HOST_USER = 'crepystories1@gmail.com'
EMAIL_HOST_PASSWORD = 'pzuw vizs zsdf bqut'# Usa una clave de aplicación, no tu contraseña
DEFAULT_FROM_EMAIL = 'crepystories1@gmail.com'

# Application definition
# --- Apps de Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# --- Tus apps
INSTALLED_APPS += [
    'system',
    'core',
]

# --- Apps de terceros
INSTALLED_APPS += [
    'cloudinary', # Ahora esta aqui
    'cloudinary_storage', # Ahora esta aqui
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'central_proyect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'central_proyect.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'es-ve'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True

# settings/base.py

LOGIN_REDIRECT_URL = '/welcome/' # <-- Cambia esta línea
LOGOUT_REDIRECT_URL = '/' # Página a la que se redirige al cerrar sesión
LOGIN_URL = '/login/' # URL de la página de inicio de sesión


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Ruta donde se recolectarán todos los archivos estáticos para producción.
# Esta carpeta debe estar vacía y no debe contener archivos fuente.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Rutas adicionales donde Django buscará archivos estáticos durante el desarrollo.
# Aquí es donde guardas tus archivos CSS, JS e imágenes del proyecto.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuración de Cloudinary, es común para ambos entornos
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET')
}

# La configuración del almacenamiento se movera a los archivos dev y prod
# dependiendo del entorno.
# DEFAULT_FILE_STORAGE = '...'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'