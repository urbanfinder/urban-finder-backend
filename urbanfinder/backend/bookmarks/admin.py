"""
Admin configuration for Bookmarks.
"""

from django.contrib import admin

from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "property", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email", "property__title"]
