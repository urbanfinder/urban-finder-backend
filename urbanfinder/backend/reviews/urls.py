"""
Review URL routes.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.ReviewListCreateView.as_view(), name="review-list-create"),
    path("<uuid:pk>/", views.ReviewUpdateView.as_view(), name="review-update"),
    path("<uuid:pk>/delete/", views.ReviewDeleteView.as_view(), name="review-delete"),
    path("stats/<uuid:property_id>/", views.ReviewStatsView.as_view(), name="review-stats"),
]
