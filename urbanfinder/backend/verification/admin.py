"""
Admin configuration for Verification Documents.
"""

from django.contrib import admin

from .models import VerificationDocument


@admin.register(VerificationDocument)
class VerificationDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "property",
        "document_type",
        "status",
        "uploaded_by",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    ]
    list_filter = ["status", "document_type", "created_at"]
    search_fields = ["property__title", "uploaded_by__email"]
    readonly_fields = ["id", "created_at", "updated_at"]
