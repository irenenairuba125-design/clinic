from django.urls import path

from . import views

app_name = "visits"

urlpatterns = [
    path("", views.VisitListView.as_view(), name="list"),
    path("new/", views.VisitCreateView.as_view(), name="create"),
    path("<int:pk>/", views.VisitDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.VisitUpdateView.as_view(), name="update"),
    path("patient/<int:patient_id>/history/", views.PatientVisitHistoryView.as_view(), name="patient_history"),
]
