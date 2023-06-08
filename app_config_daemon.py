import os
import sys
import subprocess
import time
import yaml
import pprint

def create_app(app_name):
    # Ejecutar el comando 'startapp' para crear la nueva app
    subprocess.run(['python', 'manage.py', 'startapp', app_name])

def generate_model_code(class_name, attributes):
    code = f'class {class_name}(models.Model):\n'
    for attr, attr_type in attributes.items():
        code += f'    {attr} = models.{attr_type}\n'
    return code


def inject_serializer_class_name(serializers_file, class_name):
    with open(serializers_file, 'a') as file:
        file.write(f"\n\nclass {class_name}Serializer(serializers.ModelSerializer):\n")
        file.write("    class Meta:\n")
        file.write(f"        model = {class_name}\n")
        file.write("        fields = '__all__'\n")


def inject_view_class_name(views_file, class_name):
    with open(views_file, 'a') as file:
        file.write(f"\n\nclass {class_name}ListCreateAPIView(generics.ListCreateAPIView):\n")
        file.write("    queryset = ")
        file.write(f"{class_name}.objects.all()\n")
        file.write(f"    serializer_class = {class_name}Serializer\n\n")
        file.write(f"class {class_name}RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):\n")
        file.write("    queryset = ")
        file.write(f"{class_name}.objects.all()\n")
        file.write(f"    serializer_class = {class_name}Serializer\n")


def inject_url_class_name(urls_file, class_name):
    with open(urls_file, 'a') as file:
        file.write(f"\nfrom .views import {class_name}ListCreateAPIView, {class_name}RetrieveUpdateDestroyAPIView\n")
        file.write(f"\nurlpatterns = [\n")
        file.write(f"    path('{class_name.lower()}s/', {class_name}ListCreateAPIView.as_view(), name='{class_name.lower()}-list'),\n")
        file.write(f"    path('{class_name.lower()}s/<str:pk>/', {class_name}RetrieveUpdateDestroyAPIView.as_view(), name='{class_name.lower()}-detail'),\n")
        file.write(f"]\n")


def inject_code(project_name,app_name,classes):
    # Ruta al archivo settings.py
    settings_path = project_name + '/settings.py'

    # Agregar la nueva app a INSTALLED_APPS
    with open(settings_path, 'r') as f:
        lines = f.readlines()

    with open(settings_path, 'w') as f:
        app_settings_name = "{}.apps.{}Config".format(app_name,app_name.capitalize()) 
        for line in lines:
            f.write(line)
            if line.startswith('INSTALLED_APPS = ['):
                f.write(f"    '{app_settings_name}',\n")
                f.write(f"    '{'rest_framework'}',\n")

    models_path = f'{app_name}/models.py'

    with open(models_path, 'w') as f:
        f.write('from django.db import models\n\n')
        for class_name, attributes in classes.items():
            # Inyectar en models.py
            model_code = generate_model_code(class_name, attributes)
            f.write(model_code)
            f.write('\n')

            # Inyectar en serializers.py
            serializers_file = f'{app_name}/serializers.py'  # Ruta al archivo serializers.py
            inject_serializer_class_name(serializers_file, class_name)

            # Inyectar en views.py
            views_file = f'{app_name}/views.py'  # Ruta al archivo views.py
            inject_view_class_name(views_file, class_name)

            # Inyectar en urls.py
            urls_file = f'{app_name}/urls.py'  # Ruta al archivo urls.py
            inject_url_class_name(urls_file, class_name)


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

def crear_estructuras_desde_yaml(archivo):
    result = {}
    
    def leer_archivo_yml(archivo):
        with open(archivo, 'r') as f:
            contenido = yaml.safe_load(f)
        return contenido

    # Lee el archivo YAML y obtén los datos como diccionario
    datos = leer_archivo_yml(archivo)

    # Obtiene el nombre del proyecto y el nombre de la app
    project_name = datos['project_name']
    app_name = datos['app_name']

    # Obtiene las clases y crea las estructuras de control correspondientes
    clases = datos['clases']

    print("[SUCCESS] Nombre del proyecto:", project_name)
    print("[SUCCESS] Nombre de la app creada:", app_name)
    print("[SUCCESS] Clases Creadas")
    for clase in clases:
        pprint.pprint(clase)

    result = {"project_name":project_name, "app_name":app_name, "clases":clases}
    
    return result

def only_migrations():
    subprocess.run(['python', 'manage.py', 'makemigrations'])
    subprocess.run(['python', 'manage.py', 'migrate'])

# Ejemplo de uso
'''
app_name = 'academico'
project_name = "instituto"
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
'''

# Llama a la función y pasa el nombre del archivo YAML como argumento
data = crear_estructuras_desde_yaml('config.yml')

project_name = data["project_name"]
app_name = data["app_name"]
classes = data["clases"]

try:
    if str(sys.argv[1]) == "1":
        if os.path.isdir(app_name):
            print("[INFO] Se ignora la creacion de la app, ya existe:", app_name)
            pass
        else:
            create_app(app_name)
            time.sleep(2)
            inject_code(project_name, app_name, classes)
            time.sleep(2)
            # Ejecutar las migraciones
    only_migrations()

except Exception as e:
    raise(e)
