from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Alumno
from .models import Materia
from .serializers import AlumnoSerializer
from .serializers import MateriaSerializer

@extend_schema_view(
    list=extend_schema(description="list"),
    retrieve=extend_schema(description="retrieve"),
    create=extend_schema(description="create"),
    update=extend_schema(description="list"),
    destroy=extend_schema(description="destroy"),
)

class AlumnoViewSet(viewsets.ModelViewSet):
    serializer_class = AlumnoSerializer
    queryset = Alumno.objects.all()

class MateriaViewSet(viewsets.ModelViewSet):
    serializer_class = MateriaSerializer
    queryset = Materia.objects.all()
