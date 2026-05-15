"""
Abstract base models for consistent schema across the project.
All app models should inherit from these to get UUID PKs and timestamps.
"""

import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract model providing self-updating ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class BaseModel(TimeStampedModel):
    """
    Abstract model with UUID primary key + timestamps.
    Every concrete model in the project should extend this.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(TimeStampedModel.Meta):
        abstract = True
