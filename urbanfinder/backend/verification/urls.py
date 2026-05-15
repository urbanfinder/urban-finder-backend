"""
Verification URL routes.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.DocumentUploadView.as_view(), name="verification-upload"),
    path("my/", views.MyDocumentsView.as_view(), name="verification-my-documents"),
    path("pending/", views.PendingDocumentsView.as_view(), name="verification-pending"),
    path("<uuid:pk>/review/", views.ReviewDocumentView.as_view(), name="verification-review"),
]
