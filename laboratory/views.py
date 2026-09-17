from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import LabResultForm, LabTestForm
from .models import LabTest


class LabTestListView(LoginRequiredMixin, ListView):
    model = LabTest
    template_name = "laboratory/labtest_list.html"
    context_object_name = "lab_tests"
    paginate_by = 15

    def get_queryset(self):
        queryset = LabTest.objects.select_related("patient", "requested_by")
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = LabTest.Status.choices
        context["selected_status"] = self.request.GET.get("status", "")
        return context


class PatientLabHistoryView(LoginRequiredMixin, ListView):
    model = LabTest
    template_name = "laboratory/labtest_history.html"
    context_object_name = "lab_tests"

    def get_queryset(self):
        return LabTest.objects.filter(patient_id=self.kwargs["patient_id"]).select_related("result")

    def get_context_data(self, **kwargs):
        from patients.models import Patient

        context = super().get_context_data(**kwargs)
        context["patient"] = Patient.all_objects.get(pk=self.kwargs["patient_id"])
        return context


class LabTestDetailView(LoginRequiredMixin, DetailView):
    model = LabTest
    template_name = "laboratory/labtest_detail.html"
    context_object_name = "lab_test"


class LabTestCreateView(LoginRequiredMixin, CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = "laboratory/labtest_form.html"

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get("patient")
        if patient_id:
            initial["patient"] = patient_id
        return initial

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        messages.success(self.request, "Laboratory test requested successfully.")
        return super().form_valid(form)


class LabTestUpdateView(LoginRequiredMixin, UpdateView):
    model = LabTest
    form_class = LabTestForm
    template_name = "laboratory/labtest_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Laboratory test updated successfully.")
        return super().form_valid(form)


class LabResultCreateView(LoginRequiredMixin, CreateView):
    form_class = LabResultForm
    template_name = "laboratory/labresult_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.lab_test = get_object_or_404(LabTest, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lab_test"] = self.lab_test
        return context

    def form_valid(self, form):
        form.instance.lab_test = self.lab_test
        form.instance.recorded_by = self.request.user
        messages.success(self.request, "Laboratory result captured successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.lab_test.get_absolute_url()
