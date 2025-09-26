"""
URL configuration for healthcare_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API Root endpoint with available endpoints"""
    return Response({
        'message': 'Healthcare Backend API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'profile': '/api/auth/profile/',
                'token_refresh': '/api/auth/token/refresh/',
            },
            'patients': {
                'list_create': '/api/patients/',
                'detail': '/api/patients/<id>/',
            },
            'doctors': {
                'list': '/api/doctors/',
                'create': '/api/doctors/create/',
                'detail': '/api/doctors/<id>/',
                'update': '/api/doctors/<id>/update/',
                'delete': '/api/doctors/<id>/delete/',
            },
            'mappings': {
                'list_create': '/api/mappings/',
                'delete': '/api/mappings/<id>/',
                'update': '/api/mappings/<id>/update/',
                'patient_doctors': '/api/mappings/patient/<patient_id>/',
            }
        }
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Web Interface (Frontend)
    path('', include('authentication.urls')),  # Web views now in authentication app
    
    # API Routes
    path('api/', api_root, name='api_root'),
    path('api/auth/', include('authentication.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/mappings/', include('mappings.urls')),
]
