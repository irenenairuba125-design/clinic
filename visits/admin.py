from django.contrib import admin

from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("patient", "visit_date", "attended_by", "chief_complaint")
    list_filter = ("visit_date",)
    search_fields = ("patient__first_name", "patient__last_name", "patient__patient_number")
