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


def inject_app_serializers_imports(views_file):
    with open(views_file, 'w') as file:
        file.write(f"from rest_framework import serializers\n")


def inject_serializer_class_name(serializers_file, class_name):
    print("inject_serializer_class_name", class_name)
    with open(serializers_file, 'a') as file:
        file.write(f"from .models import {class_name}\n")
        file.write(f"\n\nclass {class_name}Serializer(serializers.ModelSerializer):\n")
        file.write("    class Meta:\n")
        file.write(f"        model = {class_name}\n")
        file.write("        fields = '__all__'\n")

def  inject_view_class_name_imports(views_file, class_name):
    with open(views_file, 'a') as file:
        file.write(f"from .models import {class_name}\n")
        file.write(f"from .serializers import {class_name}Serializer\n")

def inject_app_views_imports(views_file):
    with open(views_file, 'r+') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('from django.shortcuts import render'):
                file.write("from rest_framework import viewsets\n\n")
                file.write("from drf_spectacular.utils import extend_schema, extend_schema_view\n\n")
                file.write("@extend_schema_view(\n")
                file.write('    list=extend_schema(description="list"),\n')
                file.write('    retrieve=extend_schema(description="retrieve"),\n')
                file.write('    create=extend_schema(description="create"),\n')
                file.write('    update=extend_schema(description="list"),\n')
                file.write('    destroy=extend_schema(description="destroy"),\n')
                file.write(')\n')


def inject_view_class_viewsets(views_file, class_name):
    with open(views_file, 'a') as file:
        file.write(f"\n\nclass {class_name}ViewSet(viewsets.ModelViewSet):\n")
        file.write("    queryset = ")
        file.write(f"{class_name}.objects.all()\n")
        file.write(f"    serializer_class = {class_name}Serializer\n\n")


def inject_project_url_imports(urls_file, app_name):
    with open(urls_file, 'w') as file:
        file.write("from django.contrib import admin\n")      
        file.write("from django.urls import path, include\n\n")

        code_to_inject = '''urlpatterns = [
    ### ADMIN URLS ###
    path('admin/', admin.site.urls),
    path('api/', include(('{appname}.urls','{appname}'), namespace='api-{appname}')),
]'''.format(appname=app_name)
                        
        file.write(code_to_inject)


def inject_app_clases_urls_imports(urls_file):
    with open(urls_file, 'r+') as file:
        file.write("from django.urls import path, include\n")
        file.write("from rest_framework import permissions\n")
        file.write("from rest_framework_extensions.routers import ExtendedSimpleRouter\n")
        file.write("from drf_yasg.views import get_schema_view\n")
        file.write("from drf_yasg import openapi\n")
        file.write("from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView\n")
        file.write("from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView\n\n")


def inject_app_clases_urls(urls_file, class_names):
    with open(urls_file, 'a') as file:
        
        try:
            for class_name in class_names:
                file.write(f"from .views import {str(class_name)}ViewSet\n")
        
            file.write("\nrouter: ExtendedSimpleRouter = ExtendedSimpleRouter()\n")
            
            for class_name in class_names:
                file.write(f"router.register(r'{str(class_name).lower()}', {str(class_name)}ViewSet)\n\n")

        except Exception as e:
            print("Exception")
            print(e)


def inject_app_api_urls(urls_file, app_name):

    with open(urls_file, 'a') as file:
        code_to_inject = '''schema_view = get_schema_view(
        openapi.Info(
            title="API Documentation",
            default_version='v1',
            description="API documentation for your project",
            terms_of_service="https://www.example.com/terms/",
            contact=openapi.Contact(email="contact@example.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

urlpatterns = [    
    ### Schema/Docs URLS ###
    path('schema/',SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/',SpectacularSwaggerView.as_view(url_name='{appname}:schema'), name='swagger'),
    path('schema/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    ### Login JWT URLS ###
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    ### APP URLS ###
    path('{appname}/', include(router.urls)),
        
    ]'''.format(appname=app_name)
                        
        file.write(code_to_inject)

def inject_settings(project_name,app_name):
    # Ruta al archivo settings.py
    settings_path = project_name + '/settings.py'
    
    code_to_inject = [
        "import datetime\n",
        "from django.conf import settings\n",
    ]

    # Inyectar las líneas de código
    with open(settings_path, 'r+') as f:
        lines = f.readlines()
        updated_lines = []

        for line in lines:
            updated_lines.append(line)
            if line.startswith("from pathlib import Path"):
                updated_lines.extend(code_to_inject)

        f.seek(0)
        f.writelines(updated_lines)

    # Agregar la nueva app a INSTALLED_APPS
    with open(settings_path, 'r') as f:
        lines = f.readlines()

    with open(settings_path, 'w') as f:
        app_settings_name = "{}.apps.{}Config".format(app_name,str(app_name).capitalize()) 
        for line in lines:
            f.write(line)
            if line.startswith('INSTALLED_APPS = ['):
                f.write(f"    '{app_settings_name}',\n")
                f.write(f"    '{'rest_framework'}',\n")
                f.write(f"    '{'drf_yasg'}',\n")
                f.write(f"    '{'rest_framework_extensions'}',\n")
                f.write(f"    '{'drf_spectacular'}',\n")

        code_to_inject = '''\nREST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
 
    "AUTH_HEADER_TYPES": ("Bearer",),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "Description API",
    "VERSION": "2.0.0",
    "CONTACT": {
      "name": "Contacto",
      "email": "contacto@mail.com",
      "url": "https://contacto.com",  
    },
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    #"SWAGGER_UI_FAVICON_HREF": settings.STATIC_URL + "your_company_favicon.png", # default is swagger favicon
}'''
                            
        f.write(code_to_inject)

def inject_code(project_name,app_name,classes):

    inject_settings(project_name,app_name)

    models_path = f'{app_name}/models.py'

    project_urls_file = f'{project_name}/urls.py'  # Ruta al archivo urls.py del projecto
    inject_project_url_imports(project_urls_file, app_name)
    
    #views_file = f'{app_name}/views.py'  # Ruta al archivo views.py
    #inject_app_views_imports(views_file)

    serializers_file = f'{app_name}/serializers.py'  # Ruta al archivo serializers.py
    inject_app_serializers_imports(serializers_file)

    urls_file = f'{app_name}/urls.py'  # Ruta al archivo urls.py
    with open(urls_file, 'a') as file:
        file.write("from django.urls import path\n")
        file.write(f"\nurlpatterns = []\n")

    with open(models_path, 'w') as f:
        f.write('from django.db import models\n\n')
        class_names = []
        i = 0
        for class_name, attributes in classes.items():
            i+=1
            class_names.append(class_name)
            
            # Inyectar en models.py
            model_code = generate_model_code(class_name, attributes)
            f.write(model_code)
            f.write('\n')

            # Inyectar en serializers.py
            serializers_file = f'{app_name}/serializers.py'  # Ruta al archivo serializers.py
            inject_serializer_class_name(serializers_file, class_name)

            # Inyectar en views.py
            views_file = f'{app_name}/views.py'  # Ruta al archivo views.py
            inject_view_class_name_imports(views_file, class_name)
            
            urls_file = f'{app_name}/urls.py'  # Ruta al archivo urls.py
            # Solo una vez
            if i == 1:
                inject_app_views_imports(views_file)
                inject_app_clases_urls_imports(urls_file)
            
            inject_view_class_viewsets(views_file, class_name)

            if i == len(classes.items()):
                inject_app_clases_urls(urls_file, class_names)
                inject_app_api_urls(urls_file, app_name)

        # Inyectar en urls.py
        

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

    # Obtiene el nombre del projecto y el nombre de la app
    project_name = datos['project_name']
    app_name = datos['app_name']

    # Obtiene las clases y crea las estructuras de control correspondientes
    clases = datos['clases']

    print("[SUCCESS] Nombre del projecto:", project_name)

    result = {"project_name":project_name, "app_name":app_name, "clases":clases}
    
    return result

def only_migrations():
    subprocess.run(['python', 'manage.py', 'makemigrations'])
    subprocess.run(['python', 'manage.py', 'migrate'])


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
            print("[SUCCESS] Nombre de la app creada:", app_name)
            print("[SUCCESS] Clases Creadas")
            for clase in classes:
                pprint.pprint(clase)
            # Ejecutar las migraciones
    only_migrations()

except Exception as e:
    print(e)
