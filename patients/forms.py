from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Patient


class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "national_id",
            "phone_number",
            "email",
            "address",
            "district",
            "blood_group",
            "next_of_kin_name",
            "next_of_kin_phone",
            "notes",
        ]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Patient", css_class="btn btn-primary"))


class PatientSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name, patient number, or phone...", "class": "form-control"}
        ),
    )
