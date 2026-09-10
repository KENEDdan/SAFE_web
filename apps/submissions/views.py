import csv

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.accounts.decorators import admin_required

from . import forms
from .models import (
    ContactInquiry,
    Donation,
    DonationSettings,
    DonationStatus,
    NewsletterSubscriber,
    PartnershipRequest,
    ResourceRequest,
    ResourceRequestStatus,
    VolunteerInterest,
)

# --- Public form handlers -------------------------------------------------


def _safe_next(request, fallback):
    nxt = request.POST.get("next", "")
    if nxt and url_has_allowed_host_and_scheme(
        nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return nxt
    return fallback


def _handle_public_form(request, form_class, success_msg, fallback_name):
    """Shared POST handling: honeypot, validate, save, redirect back with a message."""
    fallback = reverse(fallback_name)
    if request.method != "POST":
        return redirect(fallback)
    nxt = _safe_next(request, fallback)
    form = form_class(request.POST, request.FILES)
    if getattr(form, "is_bot", False):
        return redirect(nxt)  # drop silently
    if form.is_valid():
        form.save()
        messages.success(request, success_msg)
    else:
        messages.error(request, "Please check the form and try again.")
        request.session["form_errors"] = form.errors.get_json_data()
    return redirect(nxt)


@require_POST
def contact_submit(request):
    return _handle_public_form(
        request,
        forms.ContactInquiryForm,
        "Thank you for reaching out. We'll get back to you soon.",
        "pages:contact",
    )


@require_POST
def partnership_submit(request):
    return _handle_public_form(
        request,
        forms.PartnershipRequestForm,
        "Thank you — we've received your partnership proposal and will be in touch.",
        "pages:get_involved",
    )


@require_POST
def volunteer_submit(request):
    return _handle_public_form(
        request,
        forms.VolunteerInterestForm,
        "Thank you for your interest in volunteering. We'll contact you with opportunities.",
        "pages:get_involved",
    )


@require_POST
def resource_request_submit(request):
    return _handle_public_form(
        request,
        forms.ResourceRequestForm,
        "Your resource request has been received. We will review it and get back to you soon.",
        "pages:resources",
    )


@require_POST
def donation_submit(request):
    fallback = reverse("pages:get_involved")
    nxt = _safe_next(request, fallback)
    form = forms.DonationForm(request.POST, request.FILES)
    if getattr(form, "is_bot", False):
        return redirect(nxt)
    if form.is_valid():
        donation = form.save()
        messages.success(
            request,
            f"Thank you, {donation.donor_name}. Your reference code is "
            f"{donation.reference_code} — our team will confirm receipt.",
        )
    else:
        messages.error(request, "Please check the donation form and try again.")
    return redirect(nxt)


@require_POST
def newsletter_signup(request):
    fallback = reverse("pages:newsletter")
    nxt = _safe_next(request, fallback)
    form = forms.NewsletterSubscriberForm(request.POST)
    if getattr(form, "is_bot", False):
        return redirect(nxt)
    if form.is_valid():
        _, created = NewsletterSubscriber.objects.get_or_create(email=form.cleaned_data["email"])
        messages.success(
            request,
            "Thank you for joining our newsletter."
            if created
            else "You're already on the list — thanks for staying connected.",
        )
    else:
        messages.error(request, "Please enter a valid email address.")
    return redirect(nxt)


# --- Console inboxes -----------------------------------------------------

_INBOXES = {
    "contact": {
        "model": ContactInquiry,
        "label": "Contact inquiries",
        "columns": (("Name", "name"), ("Type", "get_inquiry_type_display"), ("Email", "email")),
    },
    "partnerships": {
        "model": PartnershipRequest,
        "label": "Partnership requests",
        "columns": (("Organization", "organization_name"), ("Contact", "contact_person"), ("Email", "email")),
    },
    "volunteers": {
        "model": VolunteerInterest,
        "label": "Volunteer interest",
        "columns": (("Name", "name"), ("Email", "email"), ("Skills", "skills")),
    },
}


@admin_required
def inbox_list(request, key):
    cfg = _INBOXES[key]
    objects = cfg["model"].objects.all()
    rows = [
        {
            "obj": o,
            "cells": [
                (getattr(o, a)() if callable(getattr(o, a)) else getattr(o, a))
                for _, a in cfg["columns"]
            ],
        }
        for o in objects
    ]
    return render(
        request,
        "manage/inbox_list.html",
        {
            "key": key,
            "label": cfg["label"],
            "headers": [h for h, _ in cfg["columns"]],
            "rows": rows,
        },
    )


@admin_required
def inbox_detail(request, key, pk):
    cfg = _INBOXES[key]
    obj = get_object_or_404(cfg["model"], pk=pk)
    if request.method == "POST":
        obj.admin_notes = request.POST.get("admin_notes", obj.admin_notes)
        if "mark_handled" in request.POST and not obj.is_handled:
            obj.is_handled = True
            obj.handled_by = request.user
            obj.handled_at = timezone.now()
        elif "mark_open" in request.POST:
            obj.is_handled = False
            obj.handled_by = None
            obj.handled_at = None
        obj.save()
        messages.success(request, "Saved.")
        return redirect("submissions:inbox_detail", key=key, pk=pk)
    return render(
        request,
        "manage/inbox_detail.html",
        {"key": key, "label": cfg["label"], "object": obj},
    )


# --- Resource requests (own status workflow) ----------------------------


@admin_required
def resource_request_list(request):
    return render(
        request,
        "manage/resource_request_list.html",
        {"requests": ResourceRequest.objects.all()},
    )


@admin_required
def resource_request_detail(request, pk):
    obj = get_object_or_404(ResourceRequest, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ResourceRequestStatus.values:
            obj.status = new_status
        obj.admin_notes = request.POST.get("admin_notes", obj.admin_notes)
        obj.is_handled = obj.status != ResourceRequestStatus.PENDING
        obj.save()
        messages.success(request, "Resource request updated.")
        return redirect("submissions:resource_request_detail", pk=pk)
    return render(
        request,
        "manage/resource_request_detail.html",
        {"object": obj, "statuses": ResourceRequestStatus.choices},
    )


# --- Donations ---------------------------------------------------------


@admin_required
def donation_list(request):
    return render(
        request,
        "manage/donation_list.html",
        {"donations": Donation.objects.all(), "settings_obj": DonationSettings.get_solo()},
    )


@admin_required
def donation_detail(request, pk):
    obj = get_object_or_404(Donation, pk=pk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "confirm":
            obj.status = DonationStatus.CONFIRMED
            obj.confirmed_by = request.user
            obj.confirmed_at = timezone.now()
        elif action == "reject":
            obj.status = DonationStatus.REJECTED
        obj.save()
        messages.success(request, "Donation updated.")
        return redirect("submissions:donation_detail", pk=pk)
    return render(request, "manage/donation_detail.html", {"object": obj})


@admin_required
def donation_settings(request):
    obj = DonationSettings.get_solo()
    from .forms_manage import DonationSettingsForm

    if request.method == "POST":
        form = DonationSettingsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Donation settings updated.")
            return redirect("submissions:donation_settings")
    else:
        form = DonationSettingsForm(instance=obj)
    return render(request, "manage/donation_settings.html", {"form": form})


# --- Newsletter -------------------------------------------------------


@admin_required
def subscriber_list(request):
    return render(
        request,
        "manage/subscriber_list.html",
        {"subscribers": NewsletterSubscriber.objects.all()},
    )


@admin_required
def subscriber_export(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="safe-newsletter-subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(["email", "subscribed_at", "is_active"])
    for sub in NewsletterSubscriber.objects.all():
        writer.writerow([sub.email, sub.subscribed_at.isoformat(), sub.is_active])
    return response
