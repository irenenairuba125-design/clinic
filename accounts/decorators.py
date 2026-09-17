from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*roles):
    """Restrict a view to users whose role is in `roles` (superusers always pass)."""

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            if request.user.is_superuser or request.user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access that page.")
            return redirect("dashboard:home")

        return wrapped

    return decorator


class RoleRequiredMixin:
    """Restrict a class-based view to users whose role is in `allowed_roles`."""

    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.role in self.allowed_roles
        ):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, "You do not have permission to access that page.")
        return redirect("dashboard:home")
