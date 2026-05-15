"""
Notification serializers.
"""

from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "is_read",
            "action_url",
            "created_at",
        ]
        read_only_fields = ["id", "notification_type", "title", "message", "action_url", "created_at"]
