# Creación de Sistema Web Django con base de datos Postgre con Docker Compose

### 1. Crear las imagenes
```sh
$ docker-compose build
```

## Autocreacion BETA:
Configure las clases que desee crear en config.yml como muestra el ejemplo y ejecute:
```sh
$ docker-compose up
```
---

## Configurar Django manualmente

### 1. Crear el sistema en el contenedor Web
```sh
docker-compose run web django-admin startproject <nombre_sistema> .  
```
#### Si estamos usando Linux debemos cambiar los usuarios de los archivos creados desde el contenedor 
```sh
sudo chown -R $USER:$USER <nombre_sistema> manage.py 
```

### 2. Conectar la base de datos
En el archivo <nombre_sistema>/settings.py cambiar el siguiente código:

Agregar:
```sh
import os
```
Arriba de:
```sh
from pathlib import Path
```

Y modificar:

```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
Por lo siguiente:
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
 }
```

### 3. Correr los contenedores  
```sh
$ docker-compose up
```
Si en la consola nos dice algo como:
```sh
web_1  | You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
web_1  | Run 'python manage.py migrate' to apply them.
web_1  | November 24, 2022 - 00:07:42
web_1  | Django version 4.1.2, using settings 'sistema_web.settings'
web_1  | Starting development server at http://0.0.0.0:8000/
web_1  | Quit the server with CONTROL-C.
```
Entonces está funcionando


### 4. Correr las migraciones de Django
```sh
docker exec -it <id contenedor web> python manage.py migrate
```

### 5. Crear un superusuario (admin) Django
```sh
docker exec -it <id contenedor web> python manage.py createsuperuser
```
Y completas los campos que nos pide adecuadamente

### 6. Navegar al admin de Django
http://localhost:8000/admin/
Ingresar con las credenciales del superusuario creado

### Probar el sistema

1. Crear un usuario nuevo en el panel de Admin de Django
2. Detener los contenedores
3. Volver a correr los contenedores
4. Verificar que el usuario crado siga existiando (esté persistido en la base de datos)

-----

## Con Mysql en lugar de Postgres:


### Requerimientos

#### En requirements.txt reemplazar:
```sh
psycopg2
```
#### por
```sh
mysqlclient
django-mysql
```

### ORM en Django

```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'PORT': os.environ.get('MYSQL_PORT'),
    }
}
```

### Modificar el docker-compose:

#### En Services DB 

```sh
image: mysql
volumes:
    - dbdata:/var/lib/mysql
environment:
    - MYSQL_ROOT_PASSWORD=root
    - MYSQL_DATABASE=django
    - MYSQL_USER=user
    - MYSQL_PASSWORD=password
ports:
    - "6033:3306"
```

#### En Services WEB

```sh
environment:
    - MYSQL_DATABASE=django
    - MYSQL_USER=user
    - MYSQL_PASSWORD=password
    - MYSQL_PORT=3306
    - MYSQL_HOST=db
```


# Django Ejemplo

## Iniciar una app de ejemplo: cursos
```sh
python manage.py startapp cursos
```

## Agregar a INSTALLED_APPS

```sh
'cursos.apps.CursosConfig',
```

## Crear clases Django de ejemplo

```sh
from django.db import models

class Alumno(models.Model):
    dni = models.CharField(primary_key=True, max_length=30)  
    nombre = models.CharField(max_length=30)  
    apellido = models.CharField(max_length=30)  
    telefono = models.CharField(max_length=30)
    email = models.EmailField()

class Materia(models.Model):
    id_materia = models.IntegerField(primary_key=True)  
    nombre = models.CharField(max_length=30)  
    descripcion = models.CharField(max_length=255)  
    anio = models.IntegerField()
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, default=None)
```

## Admin site
```sh
from django.contrib import admin
from cursos.models import Alumno, Materia

# Register your models here.
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ["dni","nombre","apellido","telefono","email"]

class MateriaAdmin(admin.ModelAdmin):
    list_display = ["id_materia","nombre","descripcion","anio"]

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Materia, MateriaAdmin)
```

### Crear y Correr las migraciones de Django para los nuevos modelos
```sh
docker exec -it <id contenedor web> python manage.py makemigrations
docker exec -it <id contenedor web> python manage.py migrate
```