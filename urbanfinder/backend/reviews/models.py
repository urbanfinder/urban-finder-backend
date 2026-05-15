"""
Review & Rating model.
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import BaseModel
from properties.models import Property


class Review(BaseModel):
    """
    A user's review of a property. One review per user per property.
    Rating is 1–5.
    """

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, default="")

    class Meta(BaseModel.Meta):
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ("property", "user")

    def __str__(self):
        return f"{self.user.full_name} → {self.property.title} ({self.rating}★)"
