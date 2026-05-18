"""
appointments model — users can save properties to their wishlist.
"""

from django.conf import settings
from django.db import models

from common.models import BaseModel
from properties.models import Property


class appointments(BaseModel):
    """
    A user's saved property. Enforces uniqueness per user-property pair.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments"
    )
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="appointments"
    )
    date = models.DateField
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user} → {self.property} on {self.date}"
