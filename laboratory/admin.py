from django.contrib import admin

from .models import LabResult, LabTest


class LabResultInline(admin.StackedInline):
    model = LabResult
    extra = 0


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ("test_name", "patient", "test_type", "status", "requested_date")
    list_filter = ("status", "test_type")
    search_fields = ("patient__first_name", "patient__last_name", "patient__patient_number", "test_name")
    inlines = [LabResultInline]
