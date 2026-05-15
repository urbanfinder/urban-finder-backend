"""
Property listing models — the core of the UrbanFinder platform.
Includes Property, PropertyImage, and PropertyAmenity.
"""

import uuid

from django.conf import settings
from django.db import models

from common.models import BaseModel


class Property(BaseModel):
    """
    A rental property listing created by an OWNER.
    Contains location, pricing, specs, and status metadata.
    """

    class PropertyType(models.TextChoices):
        APARTMENT = "APARTMENT", "Apartment"
        HOUSE = "HOUSE", "House"
        ROOM = "ROOM", "Room"
        STUDIO = "STUDIO", "Studio"
        VILLA = "VILLA", "Villa"
        OFFICE = "OFFICE", "Office Space"
        SHOP = "SHOP", "Shop"

    class FurnishingStatus(models.TextChoices):
        FURNISHED = "FURNISHED", "Furnished"
        SEMI_FURNISHED = "SEMI_FURNISHED", "Semi-Furnished"
        UNFURNISHED = "UNFURNISHED", "Unfurnished"

    class ListingStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active"
        RENTED = "RENTED", "Rented"
        INACTIVE = "INACTIVE", "Inactive"

    # ── Ownership ───────────────────────────
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties",
    )

    # ── Basic Details ───────────────────────
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
    )
    furnishing = models.CharField(
        max_length=20,
        choices=FurnishingStatus.choices,
        default=FurnishingStatus.UNFURNISHED,
    )

    # ── Pricing ─────────────────────────────
    price = models.DecimalField(max_digits=12, decimal_places=2)
    negotiable = models.BooleanField(default=False)

    # ── Specifications ──────────────────────
    bedrooms = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    area_sq_ft = models.PositiveIntegerField(help_text="Area in square feet")
    floor_number = models.SmallIntegerField(blank=True, null=True)
    total_floors = models.PositiveSmallIntegerField(blank=True, null=True)

    # ── Location ────────────────────────────
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, blank=True, default="")
    zip_code = models.CharField(max_length=20, blank=True, default="")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    # ── Status & Flags ──────────────────────
    status = models.CharField(
        max_length=10,
        choices=ListingStatus.choices,
        default=ListingStatus.DRAFT,
        db_index=True,
    )
    is_verified = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        indexes = [
            models.Index(fields=["city", "property_type"]),
            models.Index(fields=["price"]),
            models.Index(fields=["status", "is_verified"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.city}"

    @property
    def average_rating(self):
        """Compute average review rating for this property."""
        from reviews.models import Review

        avg = Review.objects.filter(property=self).aggregate(
            avg=models.Avg("rating")
        )["avg"]
        return round(avg, 2) if avg else 0.0


class PropertyImage(BaseModel):
    """
    Image associated with a property listing.
    Supports an 'is_cover' flag for the primary display image.
    """

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="properties/images/%Y/%m/")
    caption = models.CharField(max_length=200, blank=True, default="")
    is_cover = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyAmenity(BaseModel):
    """
    An amenity tag linked to a property (e.g. WiFi, Parking, Gym).
    """

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="amenities"
    )
    name = models.CharField(max_length=100)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Property Amenities"
        unique_together = ("property", "name")

    def __str__(self):
        return f"{self.name} — {self.property.title}"
