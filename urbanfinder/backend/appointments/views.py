"""
appointment views — list, toggle (add/remove), and check.
"""

from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from common.responses import error_response, success_response
from .models import appointment
from .serializers import appointmentSerializer


class appointmentListView(generics.ListAPIView):
    """GET /api/v1/appointments/   → user's saved properties"""

    serializer_class = appointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            appointment.objects.filter(user=self.request.user)
            .select_related("property__owner")
            .prefetch_related("property__images")
        )


class appointmentToggleView(APIView):
    """
    POST /api/v1/appointments/toggle/
    Body: { "property": "<uuid>" }
    Adds appointment if not exists, removes if it does — returns current state.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        property_id = request.data.get("property")
        if not property_id:
            return error_response(message="'property' field is required.")

        appointment, created = appointment.objects.get_or_create(
            user=request.user, property_id=property_id
        )

        if not created:
            appointment.delete()
            return success_response(
                data={"appointmented": False},
                message="appointment removed.",
            )

        return success_response(
            data={"appointmented": True, "id": str(appointment.id)},
            message="Property appointmented.",
            status_code=status.HTTP_201_CREATED,
        )


class appointmentCheckView(APIView):
    """GET /api/v1/appointments/check/<uuid:property_id>/"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, property_id):
        exists = appointment.objects.filter(
            user=request.user, property_id=property_id
        ).exists()
        return success_response(data={"appointmented": exists})
