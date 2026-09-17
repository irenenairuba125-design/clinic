from django.conf import settings
from django.db import models
from django.urls import reverse

from patients.models import Patient
from visits.models import Visit


class LabTest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    class TestType(models.TextChoices):
        BLOOD = "BLOOD", "Blood Test"
        URINE = "URINE", "Urine Test"
        HIV = "HIV", "HIV Test"
        MALARIA = "MALARIA", "Malaria Test"
        TB = "TB", "TB Test"
        STOOL = "STOOL", "Stool Test"
        OTHER = "OTHER", "Other"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="lab_tests")
    visit = models.ForeignKey(
        Visit, on_delete=models.SET_NULL, null=True, blank=True, related_name="lab_tests"
    )
    test_type = models.CharField(max_length=20, choices=TestType.choices)
    test_name = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requested_lab_tests",
    )
    requested_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_date"]

    def __str__(self):
        return f"{self.test_name} - {self.patient.full_name}"

    def get_absolute_url(self):
        return reverse("laboratory:detail", kwargs={"pk": self.pk})


class LabResult(models.Model):
    lab_test = models.OneToOneField(LabTest, on_delete=models.CASCADE, related_name="result")
    result_value = models.TextField()
    unit = models.CharField(max_length=50, blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    is_abnormal = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="lab_results"
    )
    recorded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.lab_test}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.lab_test.status != LabTest.Status.COMPLETED:
            self.lab_test.status = LabTest.Status.COMPLETED
            self.lab_test.save(update_fields=["status"])
