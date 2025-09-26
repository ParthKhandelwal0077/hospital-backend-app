from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Web Interface URLs
    path('', views.home_view, name='home'),
    path('login/', views.web_login_view, name='login'),
    path('register/', views.web_register_view, name='register'),
    path('logout/', views.web_logout_view, name='web_logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Include patient and doctor web URLs
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    
    # API URLs (keep existing)
    path('api_register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('api_login/', views.login_view, name='user_login'),
    path('api_profile/', views.user_profile_view, name='user_profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
