from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.ReportsHomeView.as_view(), name="home"),
    path("patients/", views.PatientRegisterReportView.as_view(), name="patient_register"),
    path("appointments/", views.AppointmentReportView.as_view(), name="appointments"),
    path("visits/", views.VisitReportView.as_view(), name="visits"),
    path("laboratory/", views.LaboratoryReportView.as_view(), name="laboratory"),
]
