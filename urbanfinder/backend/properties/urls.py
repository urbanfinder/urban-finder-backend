"""
Property URL routes.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Public
    path("", views.PropertyListView.as_view(), name="property-list"),
    path("<uuid:pk>/", views.PropertyDetailView.as_view(), name="property-detail"),

    # Owner CRUD
    path("create/", views.PropertyCreateView.as_view(), name="property-create"),
    path("<uuid:pk>/update/", views.PropertyUpdateView.as_view(), name="property-update"),
    path("<uuid:pk>/delete/", views.PropertyDeleteView.as_view(), name="property-delete"),
    path("my/", views.MyPropertiesView.as_view(), name="property-my-listings"),

    # Images
    path("<uuid:pk>/images/", views.PropertyImageUploadView.as_view(), name="property-image-upload"),
    path("images/<uuid:pk>/", views.PropertyImageDeleteView.as_view(), name="property-image-delete"),
]
