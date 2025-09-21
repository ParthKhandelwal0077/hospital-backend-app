from django.urls import path
from . import views

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('<int:pk>/', views.DoctorRetrieveView.as_view(), name='doctor_detail'),
    path('<int:pk>/update/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
]
