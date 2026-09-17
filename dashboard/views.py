from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from appointments.models import Appointment
from patients.models import Patient
from visits.models import Visit


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        context["total_patients"] = Patient.objects.count()
        context["todays_appointments"] = Appointment.objects.filter(appointment_date=today).select_related(
            "patient", "doctor"
        )
        context["todays_appointments_count"] = context["todays_appointments"].count()
        context["missed_appointments"] = Appointment.objects.filter(
            status=Appointment.Status.MISSED
        ).select_related("patient", "doctor")[:10]
        context["missed_appointments_count"] = Appointment.objects.filter(
            status=Appointment.Status.MISSED
        ).count()
        context["recent_visits"] = Visit.objects.select_related("patient", "attended_by")[:10]
        return context
