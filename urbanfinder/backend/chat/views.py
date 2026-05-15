"""
Chat views — conversations and messaging.
"""

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from common.responses import error_response, success_response
from .models import Conversation, Message
from .serializers import (
    ConversationListSerializer,
    ConversationStartSerializer,
    MessageCreateSerializer,
    MessageSerializer,
)

User = get_user_model()


class ConversationListView(generics.ListAPIView):
    """GET /api/v1/chat/   → user's conversations"""

    serializer_class = ConversationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Conversation.objects.filter(Q(initiator=user) | Q(receiver=user))
            .select_related("initiator", "receiver", "related_property")
            .prefetch_related("messages")
        )


class ConversationStartView(APIView):
    """POST /api/v1/chat/start/"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ConversationStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver_id = serializer.validated_data["receiver"]
        property_id = serializer.validated_data.get("related_property")
        message_text = serializer.validated_data["message"]

        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return error_response(
                message="Receiver not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if receiver == request.user:
            return error_response(message="Cannot start a conversation with yourself.")

        # Check for existing conversation
        conversation = Conversation.objects.filter(
            Q(initiator=request.user, receiver=receiver)
            | Q(initiator=receiver, receiver=request.user),
            related_property_id=property_id,
        ).first()

        if not conversation:
            conversation = Conversation.objects.create(
                initiator=request.user,
                receiver=receiver,
                related_property_id=property_id,
            )

        # Create the first message
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=message_text,
        )

        return success_response(
            data=ConversationListSerializer(
                conversation, context={"request": request}
            ).data,
            message="Conversation started.",
            status_code=status.HTTP_201_CREATED,
        )


class ConversationMessagesView(generics.ListAPIView):
    """GET /api/v1/chat/<uuid:conversation_id>/messages/"""

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            conversation_id=self.kwargs["conversation_id"],
            conversation__in=Conversation.objects.filter(
                Q(initiator=user) | Q(receiver=user)
            ),
        ).select_related("sender")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Mark messages as read for the current user
        Message.objects.filter(
            conversation_id=self.kwargs["conversation_id"],
            is_read=False,
        ).exclude(sender=request.user).update(is_read=True)
        return response


class SendMessageView(APIView):
    """POST /api/v1/chat/<uuid:conversation_id>/send/"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            conversation = Conversation.objects.get(
                pk=conversation_id,
            )
        except Conversation.DoesNotExist:
            return error_response(
                message="Conversation not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Verify user is a participant
        if request.user not in (conversation.initiator, conversation.receiver):
            return error_response(
                message="You are not a participant in this conversation.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=serializer.validated_data["content"],
        )

        return success_response(
            data=MessageSerializer(message, context={"request": request}).data,
            message="Message sent.",
            status_code=status.HTTP_201_CREATED,
        )
