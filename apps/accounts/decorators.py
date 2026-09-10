from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Restricts a view to console administrators (or Django superusers)."""

    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not getattr(request.user, "is_console_admin", False):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped
