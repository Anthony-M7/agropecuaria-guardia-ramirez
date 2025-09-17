# settings/dev.py

from .base import *
import os

# --- Configuración de desarrollo ---
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
SECRET_KEY = 'django-insecure-ro$q1t^y*io*7ss_0+)8p84%*06$^%#@mvoea%ixcwt_!tn1n7'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de almacenamiento local (siempre necesaria en DEV)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')