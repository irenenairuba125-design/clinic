from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_number", "full_name", "gender", "age", "phone_number", "is_active", "created_at")
    list_filter = ("is_active", "gender", "blood_group")
    search_fields = ("patient_number", "first_name", "last_name", "phone_number", "national_id")

    def get_queryset(self, request):
        return Patient.all_objects.all()
