#!/usr/bin/env bash
# Salir inmediatamente si un comando falla
set -o errexit

# Instalar las dependencias de Python
pip install -r requirements.txt

# Recopilar los archivos estáticos
python manage.py collectstatic --no-input

# Aplicar las migraciones de la base de datos
python manage.py migrate