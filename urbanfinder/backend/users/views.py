"""
Authentication & profile views.
"""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from common.responses import error_response, success_response
from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)

User = get_user_model()


# ──────────────────────────────────────────────
# Registration
# ──────────────────────────────────────────────
class RegisterView(generics.CreateAPIView):
    """POST /api/v1/auth/register/"""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success_response(
            data=UserProfileSerializer(user).data,
            message="Registration successful.",
            status_code=status.HTTP_201_CREATED,
        )


# ──────────────────────────────────────────────
# JWT Login (with custom claims)
# ──────────────────────────────────────────────
class LoginView(TokenObtainPairView):
    """POST /api/v1/auth/login/"""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    """POST /api/v1/auth/token/refresh/"""

    permission_classes = [permissions.AllowAny]


# ──────────────────────────────────────────────
# Profile
# ──────────────────────────────────────────────
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/v1/auth/profile/   → current user's profile
    PATCH /api/v1/auth/profile/  → update profile
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ──────────────────────────────────────────────
# Change Password
# ──────────────────────────────────────────────
class ChangePasswordView(APIView):
    """POST /api/v1/auth/change-password/"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return success_response(message="Password changed successfully.")
