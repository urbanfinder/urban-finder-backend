"""
Chat serializers.
"""

from rest_framework import serializers

from users.serializers import UserListSerializer
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = UserListSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "content", "is_read", "created_at"]
        read_only_fields = ["id", "sender", "is_read", "created_at"]


class MessageCreateSerializer(serializers.Serializer):
    content = serializers.CharField()


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = UserListSerializer(read_only=True)
    receiver = UserListSerializer(read_only=True)
    last_message_text = serializers.SerializerMethodField()
    last_message_at = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "related_property",
            "initiator",
            "receiver",
            "last_message_text",
            "last_message_at",
            "unread_count",
            "created_at",
        ]
        read_only_fields = fields

    def get_last_message_text(self, obj):
        msg = obj.last_message
        return msg.content[:100] if msg else None

    def get_last_message_at(self, obj):
        msg = obj.last_message
        return msg.created_at if msg else None

    def get_unread_count(self, obj):
        request = self.context.get("request")
        if request:
            return obj.messages.filter(is_read=False).exclude(
                sender=request.user
            ).count()
        return 0


class ConversationStartSerializer(serializers.Serializer):
    """Payload to start a new conversation."""

    receiver = serializers.UUIDField()
    related_property = serializers.UUIDField(required=False)
    message = serializers.CharField()
