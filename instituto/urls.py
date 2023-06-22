from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    ### ADMIN URLS ###
    path('admin/', admin.site.urls),
    path('api/', include(('academico.urls','academico'), namespace='api-academico')),
]