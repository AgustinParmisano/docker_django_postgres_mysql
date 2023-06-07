from django.contrib import admin
from .models import Alumno
from .models import Materia

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['dni', 'nombre', 'apellido', 'telefono', 'email']

admin.site.register(Alumno, AlumnoAdmin)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['id_materia', 'nombre', 'descripcion', 'anio', 'alumno']

admin.site.register(Materia, MateriaAdmin)
