from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


# API URLs
api_urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='api_user_register'),
    path('login/', views.login_view, name='api_user_login'),
    path('logout/', views.logout_view, name='api_user_logout'),
    path('profile/', views.user_profile_view, name='api_user_profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]

urlpatterns =  api_urlpatterns
