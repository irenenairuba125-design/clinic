from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import VisitForm
from .models import Visit


class VisitListView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = "visits/visit_list.html"
    context_object_name = "visits"
    paginate_by = 15

    def get_queryset(self):
        return Visit.objects.select_related("patient", "attended_by")


class PatientVisitHistoryView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = "visits/visit_history.html"
    context_object_name = "visits"

    def get_queryset(self):
        return Visit.objects.filter(patient_id=self.kwargs["patient_id"]).select_related("attended_by")

    def get_context_data(self, **kwargs):
        from patients.models import Patient

        context = super().get_context_data(**kwargs)
        context["patient"] = Patient.all_objects.get(pk=self.kwargs["patient_id"])
        return context


class VisitDetailView(LoginRequiredMixin, DetailView):
    model = Visit
    template_name = "visits/visit_detail.html"
    context_object_name = "visit"


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    form_class = VisitForm
    template_name = "visits/visit_form.html"

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get("patient")
        if patient_id:
            initial["patient"] = patient_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Visit recorded successfully.")
        return super().form_valid(form)


class VisitUpdateView(LoginRequiredMixin, UpdateView):
    model = Visit
    form_class = VisitForm
    template_name = "visits/visit_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Visit updated successfully.")
        return super().form_valid(form)
