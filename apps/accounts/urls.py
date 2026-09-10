from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import StyledAuthenticationForm

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=StyledAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password-change/", views.ForcedPasswordChangeView.as_view(), name="password_change"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("staff/", views.admin_account_list, name="account_list"),
    path("staff/add/", views.admin_account_create, name="account_create"),
    path("staff/<int:pk>/toggle-active/", views.admin_account_toggle_active, name="account_toggle_active"),
    path("staff/<int:pk>/reset-password/", views.admin_account_reset_password, name="account_reset_password"),
]
