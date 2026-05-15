"""
Admin configuration for Reviews.
"""

from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "property", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["user__email", "property__title", "comment"]
    readonly_fields = ["id", "created_at", "updated_at"]
