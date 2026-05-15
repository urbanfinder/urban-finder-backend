"""
Verification document serializers.
"""

from rest_framework import serializers

from users.serializers import UserListSerializer
from .models import VerificationDocument


class VerificationDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserListSerializer(read_only=True)
    reviewed_by = UserListSerializer(read_only=True)

    class Meta:
        model = VerificationDocument
        fields = [
            "id",
            "property",
            "uploaded_by",
            "document",
            "document_type",
            "description",
            "status",
            "reviewed_by",
            "review_notes",
            "reviewed_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_by",
            "status",
            "reviewed_by",
            "review_notes",
            "reviewed_at",
            "created_at",
        ]


class VerificationReviewSerializer(serializers.Serializer):
    """Used by admins to approve/reject a document."""

    status = serializers.ChoiceField(
        choices=["APPROVED", "REJECTED"],
    )
    review_notes = serializers.CharField(required=False, default="")
