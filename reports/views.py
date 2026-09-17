import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView

from appointments.models import Appointment
from laboratory.models import LabTest
from patients.models import Patient
from visits.models import Visit


class ReportsHomeView(LoginRequiredMixin, TemplateView):
    template_name = "reports/home.html"


class DateRangeMixin:
    def get_date_range(self):
        start_date = self.request.GET.get("start_date") or ""
        end_date = self.request.GET.get("end_date") or ""
        return start_date, end_date


class CsvExportMixin:
    csv_filename = "report.csv"
    csv_headers = []

    def get_csv_rows(self, queryset):
        raise NotImplementedError

    def export_csv(self, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{self.csv_filename}"'
        writer = csv.writer(response)
        writer.writerow(self.csv_headers)
        for row in self.get_csv_rows(queryset):
            writer.writerow(row)
        return response


class PatientRegisterReportView(LoginRequiredMixin, DateRangeMixin, CsvExportMixin, TemplateView):
    template_name = "reports/patient_register.html"
    csv_filename = "patient_register.csv"
    csv_headers = ["Patient Number", "Full Name", "Gender", "Age", "Phone", "District", "Registered On"]

    def get_queryset(self):
        queryset = Patient.all_objects.all()
        start_date, end_date = self.get_date_range()
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        return queryset

    def get_csv_rows(self, queryset):
        for patient in queryset:
            yield [
                patient.patient_number,
                patient.full_name,
                patient.get_gender_display(),
                patient.age,
                patient.phone_number,
                patient.district,
                patient.created_at.strftime("%Y-%m-%d"),
            ]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get("export") == "csv":
            return self.export_csv(queryset)
        context = self.get_context_data(patients=queryset, start_date=request.GET.get("start_date", ""),
                                         end_date=request.GET.get("end_date", ""))
        return self.render_to_response(context)


class AppointmentReportView(LoginRequiredMixin, DateRangeMixin, CsvExportMixin, TemplateView):
    template_name = "reports/appointment_report.html"
    csv_filename = "appointment_report.csv"
    csv_headers = ["Patient", "Doctor", "Date", "Time", "Status", "Reason"]

    def get_queryset(self):
        queryset = Appointment.objects.select_related("patient", "doctor")
        start_date, end_date = self.get_date_range()
        if start_date:
            queryset = queryset.filter(appointment_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(appointment_date__lte=end_date)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_csv_rows(self, queryset):
        for appt in queryset:
            yield [
                appt.patient.full_name,
                appt.doctor.get_full_name() if appt.doctor else "",
                appt.appointment_date,
                appt.appointment_time,
                appt.get_status_display(),
                appt.reason,
            ]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get("export") == "csv":
            return self.export_csv(queryset)
        context = self.get_context_data(
            appointments=queryset,
            start_date=request.GET.get("start_date", ""),
            end_date=request.GET.get("end_date", ""),
            selected_status=request.GET.get("status", ""),
            status_choices=Appointment.Status.choices,
        )
        return self.render_to_response(context)


class VisitReportView(LoginRequiredMixin, DateRangeMixin, CsvExportMixin, TemplateView):
    template_name = "reports/visit_report.html"
    csv_filename = "visit_report.csv"
    csv_headers = ["Patient", "Visit Date", "Attended By", "Chief Complaint", "Diagnosis"]

    def get_queryset(self):
        queryset = Visit.objects.select_related("patient", "attended_by")
        start_date, end_date = self.get_date_range()
        if start_date:
            queryset = queryset.filter(visit_date__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(visit_date__date__lte=end_date)
        return queryset

    def get_csv_rows(self, queryset):
        for visit in queryset:
            yield [
                visit.patient.full_name,
                visit.visit_date.strftime("%Y-%m-%d %H:%M"),
                visit.attended_by.get_full_name() if visit.attended_by else "",
                visit.chief_complaint,
                visit.diagnosis,
            ]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get("export") == "csv":
            return self.export_csv(queryset)
        context = self.get_context_data(visits=queryset, start_date=request.GET.get("start_date", ""),
                                         end_date=request.GET.get("end_date", ""))
        return self.render_to_response(context)


class LaboratoryReportView(LoginRequiredMixin, DateRangeMixin, CsvExportMixin, TemplateView):
    template_name = "reports/laboratory_report.html"
    csv_filename = "laboratory_report.csv"
    csv_headers = ["Patient", "Test Name", "Test Type", "Status", "Requested Date"]

    def get_queryset(self):
        queryset = LabTest.objects.select_related("patient")
        start_date, end_date = self.get_date_range()
        if start_date:
            queryset = queryset.filter(requested_date__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(requested_date__date__lte=end_date)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_csv_rows(self, queryset):
        for test in queryset:
            yield [
                test.patient.full_name,
                test.test_name,
                test.get_test_type_display(),
                test.get_status_display(),
                test.requested_date.strftime("%Y-%m-%d %H:%M"),
            ]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get("export") == "csv":
            return self.export_csv(queryset)
        context = self.get_context_data(
            lab_tests=queryset,
            start_date=request.GET.get("start_date", ""),
            end_date=request.GET.get("end_date", ""),
            selected_status=request.GET.get("status", ""),
            status_choices=LabTest.Status.choices,
        )
        return self.render_to_response(context)
