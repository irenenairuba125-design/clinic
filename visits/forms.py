from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Visit


class VisitForm(forms.ModelForm):
    visit_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Visit
        fields = [
            "patient",
            "appointment",
            "visit_date",
            "attended_by",
            "chief_complaint",
            "diagnosis",
            "treatment",
            "notes",
            "temperature_celsius",
            "blood_pressure",
            "pulse_rate",
            "weight_kg",
            "height_cm",
        ]
        widgets = {
            "diagnosis": forms.Textarea(attrs={"rows": 3}),
            "treatment": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Visit", css_class="btn btn-primary"))
