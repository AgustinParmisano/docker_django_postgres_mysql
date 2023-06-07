from .views import AlumnoListCreateAPIView, AlumnoRetrieveUpdateDestroyAPIView
from .views import MateriaListCreateAPIView, MateriaRetrieveUpdateDestroyAPIView
from django.urls import path

urlpatterns = [
    path('alumnos/', AlumnoListCreateAPIView.as_view(), name='alumno-list'),
    path('alumnos/<str:pk>/', AlumnoRetrieveUpdateDestroyAPIView.as_view(), name='alumno-detail'),
    path('materias/', MateriaListCreateAPIView.as_view(), name='materia-list'),
    path('materias/<str:pk>/', MateriaRetrieveUpdateDestroyAPIView.as_view(), name='materia-detail'),
]
