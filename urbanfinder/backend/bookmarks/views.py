"""
Bookmark views — list, toggle (add/remove), and check.
"""

from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from common.responses import error_response, success_response
from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkListView(generics.ListAPIView):
    """GET /api/v1/bookmarks/   → user's saved properties"""

    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Bookmark.objects.filter(user=self.request.user)
            .select_related("property__owner")
            .prefetch_related("property__images")
        )


class BookmarkToggleView(APIView):
    """
    POST /api/v1/bookmarks/toggle/
    Body: { "property": "<uuid>" }
    Adds bookmark if not exists, removes if it does — returns current state.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        property_id = request.data.get("property")
        if not property_id:
            return error_response(message="'property' field is required.")

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user, property_id=property_id
        )

        if not created:
            bookmark.delete()
            return success_response(
                data={"bookmarked": False},
                message="Bookmark removed.",
            )

        return success_response(
            data={"bookmarked": True, "id": str(bookmark.id)},
            message="Property bookmarked.",
            status_code=status.HTTP_201_CREATED,
        )


class BookmarkCheckView(APIView):
    """GET /api/v1/bookmarks/check/<uuid:property_id>/"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, property_id):
        exists = Bookmark.objects.filter(
            user=request.user, property_id=property_id
        ).exists()
        return success_response(data={"bookmarked": exists})
