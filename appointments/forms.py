from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from accounts.models import User

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "appointment_date", "appointment_time", "reason", "status", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = User.objects.filter(role=User.Role.DOCTOR)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Appointment", css_class="btn btn-primary"))
