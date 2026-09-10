from django.shortcuts import redirect
from django.urls import Resolver404, resolve

EXEMPT_URL_NAMES = {"password_change", "logout", "login"}


class ForcePasswordChangeMiddleware:
    """A logged-in user with ``must_change_password=True`` is redirected to the
    password-change form on every request except that form, logout, and
    static/media."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user and user.is_authenticated and getattr(user, "must_change_password", False):
            if not (request.path.startswith("/static/") or request.path.startswith("/media/")):
                try:
                    url_name = resolve(request.path_info).url_name
                except Resolver404:
                    url_name = None
                if url_name not in EXEMPT_URL_NAMES:
                    return redirect("accounts:password_change")

        return self.get_response(request)
