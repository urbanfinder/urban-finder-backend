"""
Bookmark model — users can save properties to their wishlist.
"""

from django.conf import settings
from django.db import models

from common.models import BaseModel
from properties.models import Property


class Bookmark(BaseModel):
    """
    A user's saved property. Enforces uniqueness per user-property pair.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookmarked_by",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
        unique_together = ("user", "property")

    def __str__(self):
        return f"{self.user.full_name} → {self.property.title}"
