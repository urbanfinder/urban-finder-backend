"""
Admin configuration for Property models.
"""

from django.contrib import admin

from .models import Property, PropertyAmenity, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0
    fields = ["image", "caption", "is_cover", "order"]


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "property_type",
        "city",
        "price",
        "status",
        "is_verified",
        "views_count",
        "created_at",
    ]
    list_filter = ["property_type", "status", "is_verified", "furnishing", "city"]
    search_fields = ["title", "description", "address", "city"]
    readonly_fields = ["id", "views_count", "created_at", "updated_at"]
    inlines = [PropertyImageInline, PropertyAmenityInline]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ["property", "caption", "is_cover", "order"]


@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = ["property", "name"]
