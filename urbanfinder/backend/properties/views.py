"""
Property views — listing, detail, CRUD, and image upload.
"""

from django.db.models import Avg, F
from rest_framework import generics, parsers, permissions, status
from rest_framework.views import APIView

from common.permissions import IsObjectOwner, IsOwnerRole
from common.responses import error_response, success_response
from .filters import PropertyFilter
from .models import Property, PropertyImage
from .serializers import (
    PropertyCreateUpdateSerializer,
    PropertyDetailSerializer,
    PropertyImageSerializer,
    PropertyListSerializer,
)


# ──────────────────────────────────────────────
# Public — List & Search
# ──────────────────────────────────────────────
class PropertyListView(generics.ListAPIView):
    """
    GET /api/v1/properties/
    Public listing with filtering, search, and ordering.
    Only shows ACTIVE + verified properties to anonymous users.
    """

    serializer_class = PropertyListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = PropertyFilter
    search_fields = ["title", "description", "city", "address"]
    ordering_fields = ["price", "created_at", "views_count", "bedrooms"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Property.objects.filter(status=Property.ListingStatus.ACTIVE)
            .select_related("owner")
            .prefetch_related("images")
            .annotate(average_rating=Avg("reviews__rating"))
        )


# ──────────────────────────────────────────────
# Public — Detail
# ──────────────────────────────────────────────
class PropertyDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/properties/<uuid>/
    Retrieve full property details. Increments view counter.
    """

    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"

    def get_queryset(self):
        return (
            Property.objects.select_related("owner")
            .prefetch_related("images", "amenities")
            .annotate(average_rating=Avg("reviews__rating"))
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Atomic view-count increment (no race condition)
        Property.objects.filter(pk=instance.pk).update(views_count=F("views_count") + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data)


# ──────────────────────────────────────────────
# Owner — Create
# ──────────────────────────────────────────────
class PropertyCreateView(generics.CreateAPIView):
    """POST /api/v1/properties/create/   (OWNER only)"""

    serializer_class = PropertyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerRole]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(
            data=PropertyDetailSerializer(
                serializer.instance,
                context={"request": request},
            ).data,
            message="Property created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


# ──────────────────────────────────────────────
# Owner — Update
# ──────────────────────────────────────────────
class PropertyUpdateView(generics.UpdateAPIView):
    """PATCH /api/v1/properties/<uuid>/update/   (owner of the listing only)"""

    serializer_class = PropertyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = "pk"

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(
            data=PropertyDetailSerializer(
                instance,
                context={"request": request},
            ).data,
            message="Property updated successfully.",
        )


# ──────────────────────────────────────────────
# Owner — Delete
# ──────────────────────────────────────────────
class PropertyDeleteView(generics.DestroyAPIView):
    """DELETE /api/v1/properties/<uuid>/delete/   (owner only)"""

    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = "pk"

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(
            message="Property deleted successfully.",
            status_code=status.HTTP_200_OK,
        )


# ──────────────────────────────────────────────
# Owner — My Listings
# ──────────────────────────────────────────────
class MyPropertiesView(generics.ListAPIView):
    """GET /api/v1/properties/my/   (authenticated OWNER)"""

    serializer_class = PropertyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerRole]

    def get_queryset(self):
        return (
            Property.objects.filter(owner=self.request.user)
            .select_related("owner")
            .prefetch_related("images")
            .annotate(average_rating=Avg("reviews__rating"))
        )


# ──────────────────────────────────────────────
# Images — Upload & Delete
# ──────────────────────────────────────────────
class PropertyImageUploadView(APIView):
    """POST /api/v1/properties/<uuid>/images/"""

    permission_classes = [permissions.IsAuthenticated, IsOwnerRole]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, pk):
        try:
            prop = Property.objects.get(pk=pk, owner=request.user)
        except Property.DoesNotExist:
            return error_response(
                message="Property not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        images = request.FILES.getlist("images")
        if not images:
            return error_response(message="No images provided.")

        created = []
        for img_file in images:
            image_obj = PropertyImage.objects.create(
                property=prop,
                image=img_file,
                caption=request.data.get("caption", ""),
                is_cover=request.data.get("is_cover", False),
            )
            created.append(PropertyImageSerializer(image_obj, context={"request": request}).data)

        return success_response(
            data=created,
            message=f"{len(created)} image(s) uploaded.",
            status_code=status.HTTP_201_CREATED,
        )


class PropertyImageDeleteView(generics.DestroyAPIView):
    """DELETE /api/v1/properties/images/<uuid>/"""

    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return PropertyImage.objects.filter(property__owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message="Image deleted.")
