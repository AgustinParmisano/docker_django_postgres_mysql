#!/bin/bash

# Lee el nombre del proyecto desde el archivo YAML
PROJECT_NAME=$(head -1 config.yml | cut -d: -f2)

# Crea un proyecto Django con el nombre leído
django-admin startproject $PROJECT_NAME .

# Ejecuta las migraciones iniciales del proyecto
python manage.py migrate

# Ejecuta el demonio para crear la app y las clases de la misma según lo configurado en config.yml
python app_config_daemon.py

export DJANGO_SUPERUSER_EMAIL=admin@admin.com
export DJANGO_SUPERUSER_PASSWORD=password
python manage.py createsuperuser --username admin --noinput

python manage.py makemigrations
python manage.py migrate

# Inicia el servidor de desarrollo de Django
python manage.py runserver 0.0.0.0:8000
