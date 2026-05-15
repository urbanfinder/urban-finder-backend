"""
Notification model for in-app notifications.
"""

from django.conf import settings
from django.db import models

from common.models import BaseModel


class Notification(BaseModel):
    """
    An in-app notification sent to a user.
    Supports different notification types and read/unread state.
    """

    class NotificationType(models.TextChoices):
        REVIEW = "REVIEW", "New Review"
        BOOKMARK = "BOOKMARK", "New Bookmark"
        VERIFICATION = "VERIFICATION", "Verification Update"
        PROPERTY = "PROPERTY", "Property Update"
        SYSTEM = "SYSTEM", "System"
        MESSAGE = "MESSAGE", "New Message"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM,
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    action_url = models.CharField(max_length=500, blank=True, default="")

    class Meta(BaseModel.Meta):
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"[{self.notification_type}] {self.title} → {self.recipient.email}"
