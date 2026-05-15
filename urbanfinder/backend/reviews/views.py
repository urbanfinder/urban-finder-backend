"""
Review views — CRUD and aggregate stats.
"""

from django.db.models import Avg, Count
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from common.permissions import IsObjectOwner
from common.responses import success_response
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/reviews/?property=<uuid>  → list reviews for a property
    POST /api/v1/reviews/                  → create a review (authenticated)
    """

    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = Review.objects.select_related("user", "property")
        property_id = self.request.query_params.get("property")
        if property_id:
            qs = qs.filter(property_id=property_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(
            data=serializer.data,
            message="Review submitted successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class ReviewUpdateView(generics.UpdateAPIView):
    """PATCH /api/v1/reviews/<uuid>/"""

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = "pk"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(
            data=serializer.data,
            message="Review updated.",
        )


class ReviewDeleteView(generics.DestroyAPIView):
    """DELETE /api/v1/reviews/<uuid>/"""

    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = "pk"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message="Review deleted.")


class ReviewStatsView(APIView):
    """GET /api/v1/reviews/stats/<uuid:property_id>/"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, property_id):
        reviews = Review.objects.filter(property_id=property_id)
        aggregate = reviews.aggregate(
            average_rating=Avg("rating"),
            total_reviews=Count("id"),
        )

        # Rating distribution  {1: 3, 2: 0, 3: 5, ...}
        distribution = dict(
            reviews.values_list("rating")
            .annotate(count=Count("id"))
            .values_list("rating", "count")
        )
        rating_distribution = {i: distribution.get(i, 0) for i in range(1, 6)}

        data = {
            "average_rating": round(aggregate["average_rating"] or 0, 2),
            "total_reviews": aggregate["total_reviews"],
            "rating_distribution": rating_distribution,
        }
        return success_response(data=data)
