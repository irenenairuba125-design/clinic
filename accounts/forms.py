from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.safestring import mark_safe
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username", "autofocus": True})
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            PrependedText("username", mark_safe('<i class="bi bi-person-fill"></i>')),
            PrependedText("password", mark_safe('<i class="bi bi-lock-fill"></i>')),
        )
        self.helper.add_input(Submit("submit", "Sign In", css_class="btn btn-primary w-100"))


class StaffCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Create Account", css_class="btn btn-primary"))
