from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import PatientForm, PatientSearchForm
from .models import Patient


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"
    paginate_by = 15

    def get_queryset(self):
        queryset = Patient.objects.all()
        self.search_form = PatientSearchForm(self.request.GET or None)
        if self.search_form.is_valid():
            query = self.search_form.cleaned_data.get("query")
            if query:
                queryset = queryset.filter(
                    Q(first_name__icontains=query)
                    | Q(last_name__icontains=query)
                    | Q(patient_number__icontains=query)
                    | Q(phone_number__icontains=query)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        return context


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = "patients/patient_detail.html"
    context_object_name = "patient"

    def get_queryset(self):
        return Patient.all_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object
        context["appointments"] = patient.appointments.order_by("-appointment_date", "-appointment_time")[:10]
        context["visits"] = patient.visits.order_by("-visit_date")[:10]
        context["lab_tests"] = patient.lab_tests.order_by("-requested_date")[:10]
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"

    def form_valid(self, form):
        form.instance.registered_by = self.request.user
        messages.success(self.request, "Patient registered successfully.")
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Patient information updated successfully.")
        return super().form_valid(form)


class PatientDeleteView(LoginRequiredMixin, DetailView):
    """Confirms and performs a soft delete."""

    model = Patient
    template_name = "patients/patient_confirm_delete.html"
    context_object_name = "patient"

    def post(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.soft_delete()
        messages.success(request, f"{patient.full_name} was deactivated (soft deleted).")
        return redirect("patients:list")


def patient_restore(request, pk):
    patient = get_object_or_404(Patient.all_objects, pk=pk)
    if request.method == "POST":
        patient.restore()
        messages.success(request, f"{patient.full_name} was restored.")
    return redirect("patients:detail", pk=pk)
