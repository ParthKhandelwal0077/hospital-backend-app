from django.urls import path
from . import views

urlpatterns = [
    # Web Interface URLs
    path('', views.patient_list_view, name='patient_list'),
    path('create/', views.patient_create_view, name='patient_create'),
    
    # API URLs
    path('api/', views.PatientListCreateView.as_view(), name='patient_list_create'),
    path('api/<int:pk>/', views.PatientRetrieveUpdateDestroyView.as_view(), name='patient_detail'),
]
