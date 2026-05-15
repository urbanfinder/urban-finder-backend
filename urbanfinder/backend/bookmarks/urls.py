"""
Bookmark URL routes.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookmarkListView.as_view(), name="bookmark-list"),
    path("toggle/", views.BookmarkToggleView.as_view(), name="bookmark-toggle"),
    path("check/<uuid:property_id>/", views.BookmarkCheckView.as_view(), name="bookmark-check"),
]
