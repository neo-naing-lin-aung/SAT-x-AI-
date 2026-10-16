"""URL Patterns for Accounts App."""

from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    # Login 
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    # Logout 
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    # Register 
    path('register/', views.register, name="register"),    
    # Edit Profile Page
    path('edit-profile/', views.edit_profile, name="edit_profile"),
]