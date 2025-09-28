from django.urls import path
from . import views

# API-only URLs for patients
urlpatterns = [
    path('', views.PatientListCreateView.as_view(), name='patient_list_create'),
    path('<int:pk>/', views.PatientRetrieveUpdateDestroyView.as_view(), name='patient_detail'),
]
