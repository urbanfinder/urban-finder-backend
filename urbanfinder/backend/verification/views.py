"""
Verification views — document upload, listing, and admin review.
"""

from django.utils import timezone
from rest_framework import generics, parsers, permissions, status
from rest_framework.views import APIView

from common.permissions import IsAdminRole, IsOwnerRole
from common.responses import error_response, success_response
from .models import VerificationDocument
from .serializers import VerificationDocumentSerializer, VerificationReviewSerializer


class DocumentUploadView(generics.CreateAPIView):
    """POST /api/v1/verification/upload/   (OWNER only)"""

    serializer_class = VerificationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerRole]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(
            data=serializer.data,
            message="Document uploaded for verification.",
            status_code=status.HTTP_201_CREATED,
        )


class MyDocumentsView(generics.ListAPIView):
    """GET /api/v1/verification/my/   (OWNER — their uploaded documents)"""

    serializer_class = VerificationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerRole]

    def get_queryset(self):
        return VerificationDocument.objects.filter(
            uploaded_by=self.request.user
        ).select_related("uploaded_by", "reviewed_by")


class PendingDocumentsView(generics.ListAPIView):
    """GET /api/v1/verification/pending/   (ADMIN — pending review queue)"""

    serializer_class = VerificationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get_queryset(self):
        return VerificationDocument.objects.filter(
            status=VerificationDocument.VerificationStatus.PENDING
        ).select_related("uploaded_by", "reviewed_by", "property")


class ReviewDocumentView(APIView):
    """POST /api/v1/verification/<uuid>/review/   (ADMIN only)"""

    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        try:
            document = VerificationDocument.objects.get(pk=pk)
        except VerificationDocument.DoesNotExist:
            return error_response(
                message="Document not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = VerificationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document.status = serializer.validated_data["status"]
        document.review_notes = serializer.validated_data.get("review_notes", "")
        document.reviewed_by = request.user
        document.reviewed_at = timezone.now()
        document.save()

        # If ALL documents for this property are approved, mark property as verified
        if document.status == VerificationDocument.VerificationStatus.APPROVED:
            prop = document.property
            all_approved = not prop.verification_documents.exclude(
                status=VerificationDocument.VerificationStatus.APPROVED
            ).exists()
            if all_approved:
                prop.is_verified = True
                prop.save(update_fields=["is_verified"])

        return success_response(
            data=VerificationDocumentSerializer(document).data,
            message=f"Document {document.status.lower()}.",
        )
