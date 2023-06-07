from django.db import models

class Alumno(models.Model):
    dni = models.IntegerField(primary_key=True)
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

