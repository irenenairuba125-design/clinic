from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import LabResult, LabTest


class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ["patient", "visit", "test_type", "test_name", "status", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Test Request", css_class="btn btn-primary"))


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ["result_value", "unit", "reference_range", "is_abnormal", "remarks"]
        widgets = {
            "result_value": forms.Textarea(attrs={"rows": 3}),
            "remarks": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Result", css_class="btn btn-primary"))
