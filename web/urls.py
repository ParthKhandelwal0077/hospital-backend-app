from django.urls import path
from . import views

urlpatterns = [
    # Home and Dashboard
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Patients
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/create/', views.PatientListView.as_view(), name='patient_create'),  # Placeholder
    path('patients/<int:pk>/edit/', views.PatientDetailView.as_view(), name='patient_edit'),  # Placeholder
    path('patients/<int:pk>/delete/', views.PatientDetailView.as_view(), name='patient_delete'),  # Placeholder
    
    # Doctors
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctors/create/', views.DoctorListView.as_view(), name='doctor_create'),  # Placeholder
    path('doctors/<int:pk>/edit/', views.DoctorDetailView.as_view(), name='doctor_edit'),  # Placeholder
    path('doctors/<int:pk>/delete/', views.DoctorDetailView.as_view(), name='doctor_delete'),  # Placeholder
    
    # Mappings
    path('assignments/', views.MappingListView.as_view(), name='mapping_list'),
    path('assignments/create/', views.MappingListView.as_view(), name='mapping_create'),  # Placeholder
    path('assignments/<int:pk>/edit/', views.MappingListView.as_view(), name='mapping_edit'),  # Placeholder
    path('assignments/<int:pk>/delete/', views.MappingListView.as_view(), name='mapping_delete'),  # Placeholder
    
    # API Test
    path('api-test/', views.api_test_view, name='api_test'),
]
