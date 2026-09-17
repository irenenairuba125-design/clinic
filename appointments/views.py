from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AppointmentForm
from .models import Appointment


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"
    paginate_by = 15

    def get_queryset(self):
        queryset = Appointment.objects.select_related("patient", "doctor")
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Appointment.Status.choices
        context["selected_status"] = self.request.GET.get("status", "")
        return context


class UpcomingAppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "appointments/appointment_upcoming.html"
    context_object_name = "appointments"
    paginate_by = 15

    def get_queryset(self):
        return Appointment.objects.select_related("patient", "doctor").filter(
            appointment_date__gte=timezone.localdate(),
            status=Appointment.Status.SCHEDULED,
        )


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = "appointments/appointment_detail.html"
    context_object_name = "appointment"


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get("patient")
        if patient_id:
            initial["patient"] = patient_id
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Appointment scheduled successfully.")
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Appointment updated successfully.")
        return super().form_valid(form)


class AppointmentCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status", "updated_at"])
        messages.success(request, "Appointment cancelled.")
        return redirect("appointments:detail", pk=pk)
