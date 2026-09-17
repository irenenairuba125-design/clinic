from django.conf import settings
from django.db import models
from django.urls import reverse

from appointments.models import Appointment
from patients.models import Patient


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="visits")
    appointment = models.ForeignKey(
        Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name="visits"
    )
    visit_date = models.DateTimeField()
    attended_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="visits"
    )

    chief_complaint = models.CharField(max_length=255)
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    temperature_celsius = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, blank=True, help_text="e.g. 120/80")
    pulse_rate = models.PositiveIntegerField(null=True, blank=True, help_text="beats per minute")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-visit_date"]

    def __str__(self):
        return f"{self.patient.full_name} visit on {self.visit_date:%Y-%m-%d}"

    def get_absolute_url(self):
        return reverse("visits:detail", kwargs={"pk": self.pk})
