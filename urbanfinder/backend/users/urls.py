"""
User & auth URL routes.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="auth-register"),
    path("login/", views.LoginView.as_view(), name="auth-login"),
    path("token/refresh/", views.CustomTokenRefreshView.as_view(), name="auth-token-refresh"),
    path("profile/", views.ProfileView.as_view(), name="auth-profile"),
    path("change-password/", views.ChangePasswordView.as_view(), name="auth-change-password"),
]
