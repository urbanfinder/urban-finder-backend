"""
Notification views — list, mark read, mark all read, unread count.
"""

from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from common.responses import success_response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """GET /api/v1/notifications/   → user's notifications (newest first)"""

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user)
        # Optional filter by read status
        is_read = self.request.query_params.get("is_read")
        if is_read is not None:
            qs = qs.filter(is_read=is_read.lower() == "true")
        return qs


class NotificationMarkReadView(APIView):
    """PATCH /api/v1/notifications/<uuid>/read/"""

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return success_response(
                data=None,
                message="Notification not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return success_response(
            data=NotificationSerializer(notification).data,
            message="Notification marked as read.",
        )


class NotificationMarkAllReadView(APIView):
    """POST /api/v1/notifications/read-all/"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).update(is_read=True)
        return success_response(
            data={"marked_read": count},
            message=f"{count} notification(s) marked as read.",
        )


class UnreadCountView(APIView):
    """GET /api/v1/notifications/unread-count/"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
        return success_response(data={"unread_count": count})
