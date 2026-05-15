"""
UrbanFinder URL Configuration.
Root router that includes all app-level URL patterns.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API v1 namespaced routes
    path("api/v1/auth/", include("users.urls")),
    path("api/v1/properties/", include("properties.urls")),
    path("api/v1/bookmarks/", include("bookmarks.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/verification/", include("verification.urls")),
    path("api/v1/chat/", include("chat.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
