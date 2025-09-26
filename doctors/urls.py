from django.urls import path
from . import views

urlpatterns = [
    # Web Interface URLs
    path('', views.doctor_list_view, name='doctor_list'),
    path('create/', views.doctor_create_view, name='doctor_create'),
    
    # API URLs
    path('api/', views.DoctorListView.as_view(), name='doctor_api_list'),
    path('api/create/', views.DoctorCreateView.as_view(), name='doctor_api_create'),
    path('api/<int:pk>/', views.DoctorRetrieveView.as_view(), name='doctor_detail'),
    path('api/<int:pk>/update/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('api/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
]
