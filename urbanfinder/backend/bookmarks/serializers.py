"""
Bookmark serializers.
"""

from rest_framework import serializers

from properties.serializers import PropertyListSerializer
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    property_detail = PropertyListSerializer(source="property", read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "property", "property_detail", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"property": {"write_only": True}}
