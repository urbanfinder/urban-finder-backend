"""
Serializers for Property, PropertyImage, and PropertyAmenity.
Handles creation with nested images/amenities and read-only computed fields.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserListSerializer
from .models import Property, PropertyAmenity, PropertyImage

User = get_user_model()


# ──────────────────────────────────────────────
# Nested / child serializers
# ──────────────────────────────────────────────
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image", "caption", "is_cover", "order", "created_at"]
        read_only_fields = ["id", "created_at"]


class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = ["id", "name"]
        read_only_fields = ["id"]


# ──────────────────────────────────────────────
# Property — List (lightweight)
# ──────────────────────────────────────────────
class PropertyListSerializer(serializers.ModelSerializer):
    """Compact serializer used in list views and search results."""

    owner = UserListSerializer(read_only=True)
    cover_image = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "property_type",
            "price",
            "negotiable",
            "bedrooms",
            "bathrooms",
            "area_sq_ft",
            "city",
            "address",
            "status",
            "is_verified",
            "views_count",
            "cover_image",
            "average_rating",
            "owner",
            "created_at",
        ]
        read_only_fields = fields

    def get_cover_image(self, obj):
        cover = obj.images.filter(is_cover=True).first()
        if not cover:
            cover = obj.images.first()
        if cover:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(cover.image.url)
            return cover.image.url
        return None


# ──────────────────────────────────────────────
# Property — Detail (full)
# ──────────────────────────────────────────────
class PropertyDetailSerializer(serializers.ModelSerializer):
    """Full serializer used in retrieve views."""

    owner = UserListSerializer(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities = PropertyAmenitySerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "description",
            "property_type",
            "furnishing",
            "price",
            "negotiable",
            "bedrooms",
            "bathrooms",
            "area_sq_ft",
            "floor_number",
            "total_floors",
            "address",
            "city",
            "state",
            "zip_code",
            "latitude",
            "longitude",
            "status",
            "is_verified",
            "views_count",
            "average_rating",
            "owner",
            "images",
            "amenities",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_verified",
            "views_count",
            "owner",
            "created_at",
            "updated_at",
        ]


# ──────────────────────────────────────────────
# Property — Create / Update
# ──────────────────────────────────────────────
class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    """Used by OWNER to create or update a listing."""

    amenities = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "property_type",
            "furnishing",
            "price",
            "negotiable",
            "bedrooms",
            "bathrooms",
            "area_sq_ft",
            "floor_number",
            "total_floors",
            "address",
            "city",
            "state",
            "zip_code",
            "latitude",
            "longitude",
            "status",
            "amenities",
        ]

    def create(self, validated_data):
        amenity_names = validated_data.pop("amenities", [])
        prop = Property.objects.create(**validated_data)
        for name in amenity_names:
            PropertyAmenity.objects.create(property=prop, name=name)
        return prop

    def update(self, instance, validated_data):
        amenity_names = validated_data.pop("amenities", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if amenity_names is not None:
            instance.amenities.all().delete()
            for name in amenity_names:
                PropertyAmenity.objects.create(property=instance, name=name)

        return instance
