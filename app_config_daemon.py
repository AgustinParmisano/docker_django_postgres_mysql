import os
import subprocess
import time

def create_app(app_name):
    # Ejecutar el comando 'startapp' para crear la nueva app
    subprocess.run(['python', 'manage.py', 'startapp', app_name])

def generate_model_code(class_name, attributes):
    code = f'class {class_name}(models.Model):\n'
    for attr, attr_type in attributes.items():
        code += f'    {attr} = models.{attr_type}\n'
    return code

def inject_code(proyect_name,app_name,classes):
    # Ruta al archivo settings.py
    settings_path = proyect_name + '/settings.py'

    # Agregar la nueva app a INSTALLED_APPS
    with open(settings_path, 'r') as f:
        lines = f.readlines()

    with open(settings_path, 'w') as f:
        app_settings_name = "{}.apps.{}Config".format(app_name,app_name.capitalize()) 
        for line in lines:
            f.write(line)
            if line.startswith('INSTALLED_APPS = ['):
                f.write(f"    '{app_settings_name}',\n")

    models_path = f'{app_name}/models.py'

    with open(models_path, 'w') as f:
        f.write('from django.db import models\n\n')
        for class_name, attributes in classes.items():
            model_code = generate_model_code(class_name, attributes)
            f.write(model_code)
            f.write('\n')


    # Crear los modelos del admin site
    admin_path = f'{app_name}/admin.py'

    with open(admin_path, 'w') as f:
        f.write('from django.contrib import admin\n')
        for class_name in classes.keys():
            f.write(f'from .models import {class_name}\n')
        f.write('\n')
        for class_name, attributes in classes.items():
            f.write(f'class {class_name}Admin(admin.ModelAdmin):\n')
            f.write(f'    list_display = {list(attributes.keys())}\n\n')
            f.write(f'admin.site.register({class_name}, {class_name}Admin)\n')

# Ejemplo de uso
app_name = 'academico'
proyect_name = "instituto"
class1 = {'Alumno': {
    'dni':'CharField(primary_key=True, max_length=30)',
    'nombre':'CharField(max_length=30)',
    'apellido':'CharField(max_length=30)',
    'telefono':'CharField(max_length=30)',
    'email':'EmailField()'
}}

class2 = {'Materia': {
    'id_materia':'IntegerField(primary_key=True)',
    'nombre':'CharField(max_length=30)',
    'descripcion':'CharField(max_length=255)',
    'anio':'IntegerField()',
    'alumno':'ForeignKey(Alumno, on_delete=models.CASCADE, default=None)'
}}

classes = {**class1, **class2}

try:
    create_app(app_name)
    time.sleep(2)
    inject_code(proyect_name, app_name, classes)
    time.sleep(2)
    # Ejecutar las migraciones
    subprocess.run(['python', 'manage.py', 'makemigrations', app_name])
    subprocess.run(['python', 'manage.py', 'migrate'])
except Exception as e:
    raise(e)