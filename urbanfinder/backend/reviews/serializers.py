"""
Review serializers.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserListSerializer
from .models import Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "property", "user", "rating", "comment", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        property_obj = attrs.get("property")

        # Prevent owners from reviewing their own property
        if property_obj and property_obj.owner == request.user:
            raise serializers.ValidationError("You cannot review your own property.")

        # Prevent duplicate reviews (on create only)
        if not self.instance:
            if Review.objects.filter(user=request.user, property=property_obj).exists():
                raise serializers.ValidationError(
                    "You have already reviewed this property."
                )

        return attrs


class ReviewStatsSerializer(serializers.Serializer):
    """Read-only serializer for aggregate review stats."""

    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    rating_distribution = serializers.DictField()
