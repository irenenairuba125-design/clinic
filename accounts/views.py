from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .decorators import RoleRequiredMixin
from .forms import LoginForm, StaffCreationForm
from .models import User


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    next_page = "accounts:login"


class StaffListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = User
    template_name = "accounts/staff_list.html"
    context_object_name = "staff_members"
    paginate_by = 20
    allowed_roles = (User.Role.ADMIN,)

    def get_queryset(self):
        return User.objects.all().order_by("first_name", "last_name")


class StaffCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = User
    form_class = StaffCreationForm
    template_name = "accounts/staff_form.html"
    success_url = reverse_lazy("accounts:staff_list")
    allowed_roles = (User.Role.ADMIN,)

    def form_valid(self, form):
        messages.success(self.request, "Staff account created successfully.")
        return super().form_valid(form)
