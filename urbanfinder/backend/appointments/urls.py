"""
Apointments URL routes.
"""


from django.urls import path
from . import views

urlpatterns = [
    path("", views.AppointmentListView.as_view(), name="appointment-list"),
    path("create/", views.AppointmentCreateView.as_view(), name="appointment-create"),
    path("delete/<uuid:apointment_id>/", views.AppointmentDeleteView.as_view(), name="appointment-delete"),
]