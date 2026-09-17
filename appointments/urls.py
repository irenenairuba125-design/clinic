from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("", views.AppointmentListView.as_view(), name="list"),
    path("upcoming/", views.UpcomingAppointmentListView.as_view(), name="upcoming"),
    path("new/", views.AppointmentCreateView.as_view(), name="create"),
    path("<int:pk>/", views.AppointmentDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.AppointmentUpdateView.as_view(), name="update"),
    path("<int:pk>/cancel/", views.AppointmentCancelView.as_view(), name="cancel"),
]
