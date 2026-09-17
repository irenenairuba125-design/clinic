from django.urls import path

from . import views

app_name = "laboratory"

urlpatterns = [
    path("", views.LabTestListView.as_view(), name="list"),
    path("new/", views.LabTestCreateView.as_view(), name="create"),
    path("<int:pk>/", views.LabTestDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.LabTestUpdateView.as_view(), name="update"),
    path("<int:pk>/result/", views.LabResultCreateView.as_view(), name="add_result"),
    path("patient/<int:patient_id>/history/", views.PatientLabHistoryView.as_view(), name="patient_history"),
]
