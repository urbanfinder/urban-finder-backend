"""
Property verification documents model.
Owners upload documents; admins approve or reject them.
"""

from django.conf import settings
from django.db import models

from common.models import BaseModel
from properties.models import Property


class VerificationDocument(BaseModel):
    """
    A document submitted by a property owner for admin verification.
    """

    class DocumentType(models.TextChoices):
        OWNERSHIP_PROOF = "OWNERSHIP_PROOF", "Ownership Proof"
        UTILITY_BILL = "UTILITY_BILL", "Utility Bill"
        IDENTITY = "IDENTITY", "Identity Document"
        TAX_RECEIPT = "TAX_RECEIPT", "Tax Receipt"
        OTHER = "OTHER", "Other"

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="verification_documents",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_documents",
    )
    document = models.FileField(upload_to="verification/documents/%Y/%m/")
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )
    description = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(
        max_length=10,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_documents",
    )
    review_notes = models.TextField(blank=True, default="")
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Verification Document"
        verbose_name_plural = "Verification Documents"

    def __str__(self):
        return f"[{self.document_type}] {self.property.title} — {self.status}"
