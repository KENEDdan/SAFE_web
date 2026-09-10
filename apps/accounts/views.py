import logging
import secrets
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from apps.content.models import Activity, Partner, Project, TeamMember, Testimonial
from apps.newsfeed.models import NewsPost
from apps.submissions.models import (
    ContactInquiry,
    Donation,
    PartnershipRequest,
    ResourceRequest,
    VolunteerInterest,
)
from apps.submissions.models import NewsletterSubscriber

from .decorators import admin_required
from .forms import AdminAccountForm, StyledPasswordChangeForm
from .models import User

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    def _new(model):
        return model.objects.filter(is_handled=False).count()

    context = {
        "counts": {
            "contact": _new(ContactInquiry),
            "resource_requests": ResourceRequest.objects.filter(status="pending").count(),
            "partnerships": _new(PartnershipRequest),
            "volunteers": _new(VolunteerInterest),
            "donations": Donation.objects.filter(status="pending").count(),
            "subscribers": NewsletterSubscriber.objects.count(),
            "projects": Project.objects.count(),
            "activities": Activity.objects.count(),
            "team": TeamMember.objects.count(),
            "leadership": TeamMember.objects.filter(is_leadership=True).count(),
            "partners": Partner.objects.count(),
            "news": NewsPost.objects.count(),
            "testimonials": Testimonial.objects.filter(is_published=False).count(),
        },
    }
    return render(request, "accounts/dashboard.html", context)


class ForcedPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy("accounts:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.must_change_password = False
        self.request.user.save(update_fields=["must_change_password"])
        messages.success(self.request, "Password updated successfully.")
        return response


def _generate_temp_password():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(12))


def _send_temp_password_email(request, account, temp_password, is_reset=False):
    if not account.email:
        return False
    login_url = request.build_absolute_uri(reverse("accounts:login"))
    if is_reset:
        subject = "Your SAFE console password was reset"
        intro = "Your password on the SAFE management console has been reset."
    else:
        subject = "Your SAFE management console account"
        intro = "An account has been created for you on the SAFE management console."
    message = (
        f"Hello {account.get_full_name() or account.username},\n\n"
        f"{intro}\n\n"
        f"Username: {account.username}\n"
        f"Temporary password: {temp_password}\n\n"
        f"Log in here: {login_url}\n"
        "You'll be asked to set a new password the first time you log in.\n\n"
        "If you weren't expecting this, please contact your administrator."
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [account.email], fail_silently=False)
        return True
    except Exception:
        logger.exception("Failed to send account email to %s", account.email)
        return False


@admin_required
def admin_account_list(request):
    accounts = User.objects.all().order_by("-is_active", "username")
    return render(request, "accounts/account_list.html", {"accounts": accounts})


@admin_required
def admin_account_create(request):
    if request.method == "POST":
        form = AdminAccountForm(request.POST)
        if form.is_valid():
            temp_password = _generate_temp_password()
            account = form.save(commit=False)
            account.set_password(temp_password)
            account.must_change_password = True
            account.is_staff = True
            account.created_by = request.user
            account.save()
            email_sent = _send_temp_password_email(request, account, temp_password)
            if account.email and not email_sent:
                messages.error(
                    request,
                    "Account created, but the notification email failed to send — "
                    "share the temporary password with them directly.",
                )
            return render(
                request,
                "accounts/account_created.html",
                {"account": account, "temp_password": temp_password, "email_sent": email_sent},
            )
    else:
        form = AdminAccountForm()
    return render(request, "accounts/account_form.html", {"form": form, "mode": "Add"})


@admin_required
def admin_account_toggle_active(request, pk):
    account = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        if account == request.user:
            messages.error(request, "You can't deactivate your own account.")
            return redirect("accounts:account_list")
        account.is_active = not account.is_active
        account.save(update_fields=["is_active"])
        messages.success(
            request,
            f"{account.username} is now {'active' if account.is_active else 'inactive'}.",
        )
    return redirect("accounts:account_list")


@admin_required
def admin_account_reset_password(request, pk):
    account = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        temp_password = _generate_temp_password()
        account.set_password(temp_password)
        account.must_change_password = True
        account.save()
        email_sent = _send_temp_password_email(request, account, temp_password, is_reset=True)
        if account.email and not email_sent:
            messages.error(
                request,
                "Password reset, but the notification email failed to send — "
                "share the temporary password with them directly.",
            )
        return render(
            request,
            "accounts/account_created.html",
            {
                "account": account,
                "temp_password": temp_password,
                "is_reset": True,
                "email_sent": email_sent,
            },
        )
    return render(request, "accounts/account_confirm_reset.html", {"account": account})
