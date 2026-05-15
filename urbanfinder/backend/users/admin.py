"""
Admin registration for the custom User model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "full_name", "role", "is_verified", "is_active", "created_at")
    list_filter = ("role", "is_active", "is_verified", "is_staff")
    search_fields = ("email", "full_name", "phone_number")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone_number", "avatar", "bio", "address", "city")}),
        ("Roles & Status", {"fields": ("role", "is_verified", "is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login", "created_at", "updated_at")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "role", "password1", "password2"),
            },
        ),
    )
