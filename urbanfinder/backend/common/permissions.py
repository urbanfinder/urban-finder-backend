"""
Reusable DRF permissions used across multiple apps.
"""

from rest_framework.permissions import BasePermission


class IsOwnerRole(BasePermission):
    """Allow access only to users with OWNER role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "OWNER"
        )


class IsAdminRole(BasePermission):
    """Allow access only to users with ADMIN role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsOwnerOrAdmin(BasePermission):
    """Allow access to OWNER or ADMIN roles."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ("OWNER", "ADMIN")
        )


class IsObjectOwner(BasePermission):
    """
    Object-level permission: only allow the object's owner to modify it.
    Expects the object to have a ``user`` or ``owner`` FK.
    """

    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "owner", None) or getattr(obj, "user", None)
        return owner == request.user
