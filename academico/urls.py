from django.urls import path, include
from rest_framework import permissions
from rest_framework_extensions.routers import ExtendedSimpleRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from academico.views import AlumnoViewSet, MateriaViewSet

router: ExtendedSimpleRouter = ExtendedSimpleRouter()
router.register(r'alumnos', AlumnoViewSet)
router.register(r'materias', MateriaViewSet)


schema_view = get_schema_view(
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
    path('schema/swagger/',SpectacularSwaggerView.as_view(url_name='academico:schema'), name='swagger'),
    path('schema/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    ### Login JWT URLS ###
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    ### Academico URLS ###
    path('academico/', include(router.urls)),
]