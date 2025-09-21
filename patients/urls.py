from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientListCreateView.as_view(), name='patient_list_create'),
    path('<int:pk>/', views.PatientRetrieveUpdateDestroyView.as_view(), name='patient_detail'),
]
