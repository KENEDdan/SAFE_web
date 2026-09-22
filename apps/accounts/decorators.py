from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import Http404


def admin_required(view_func):
    """Restricts a view to console administrators (or Django superusers).

    Anonymous visitors get a 404 rather than a redirect, so a staff URL never
    discloses where the login portal lives.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not getattr(request.user, "is_console_admin", False):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped
