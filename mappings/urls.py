from django.urls import path
from . import views

urlpatterns = [
    path('', views.MappingListCreateView.as_view(), name='mapping_list_create'),
    path('<int:pk>/', views.MappingDeleteView.as_view(), name='mapping_delete'),
    path('<int:pk>/update/', views.MappingUpdateView.as_view(), name='mapping_update'),
    path('patient/<int:patient_id>/', views.patient_doctors_view, name='patient_doctors'),
]
