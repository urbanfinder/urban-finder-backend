"""
Chat models — Conversation threads and Messages.
Enables user-to-owner communication about specific properties.
"""

from django.conf import settings
from django.db import models

from common.models import BaseModel
from properties.models import Property


class Conversation(BaseModel):
    """
    A conversation thread between two users, optionally linked to a property.
    """

    related_property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conversations",
    )
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="initiated_conversations",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_conversations",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        unique_together = ("initiator", "receiver", "related_property")

    def __str__(self):
        return f"{self.initiator.full_name} ↔ {self.receiver.full_name}"

    @property
    def last_message(self):
        return self.messages.order_by("-created_at").first()


class Message(BaseModel):
    """A single message within a conversation."""

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.full_name}: {self.content[:50]}"
