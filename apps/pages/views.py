from django.contrib import messages
from django.shortcuts import redirect, render

from apps.accounts.decorators import admin_required
from apps.core.forms import OrganizationProfileForm, SiteSettingsForm
from apps.core.models import OrganizationProfile, SiteSettings
from apps.content.models import (
    CoreValue,
    CrossCuttingTheme,
    GalleryImage,
    ImpactStat,
    Milestone,
    Partner,
    Program,
    Project,
    Resource,
    TargetBeneficiary,
    TeamMember,
    Testimonial,
)
from apps.submissions.forms import (
    ContactInquiryForm,
    DonationForm,
    PartnershipRequestForm,
    ResourceRequestForm,
    VolunteerInterestForm,
)
from apps.newsfeed.models import NewsPost
from apps.submissions.models import DonationSettings

from . import forms
from .models import (
    AboutPage,
    GetInvolvedPage,
    HomePage,
    ImpactPage,
    ResourcesPage,
    WhatWeDoPage,
)

# --- Public pages ----------------------------------------------------------


def home(request):
    ctx = {
        "page": HomePage.get_solo(),
        "programs": Program.objects.published()[:6],
        "stats": ImpactStat.objects.published(),
        "featured_projects": Project.objects.published().filter(is_featured=True)[:3],
        "gallery": GalleryImage.objects.published()[:8],
        "testimonials": Testimonial.objects.published().filter(is_featured=True)[:3],
        "news": NewsPost.objects.live()[:3],
    }
    return render(request, "public/home.html", ctx)


def about(request):
    ctx = {
        "page": AboutPage.get_solo(),
        "values": CoreValue.objects.published(),
        "team": TeamMember.objects.published()[:8],
        "leadership": TeamMember.objects.published().filter(is_leadership=True),
        "org": OrganizationProfile.get_solo(),
        "partners": Partner.objects.published(),
    }
    return render(request, "public/about.html", ctx)


def what_we_do(request):
    ctx = {
        "page": WhatWeDoPage.get_solo(),
        "programs": Program.objects.published(),
        "themes": CrossCuttingTheme.objects.published(),
    }
    return render(request, "public/what_we_do.html", ctx)


def impact(request):
    ctx = {
        "page": ImpactPage.get_solo(),
        "stats": ImpactStat.objects.published(),
        "beneficiaries": TargetBeneficiary.objects.published(),
        "milestones": Milestone.objects.published(),
        "testimonials": Testimonial.objects.published(),
        "gallery": GalleryImage.objects.published()[:9],
    }
    return render(request, "public/impact.html", ctx)


def resources(request):
    ctx = {
        "page": ResourcesPage.get_solo(),
        "resources": Resource.objects.published(),
        "form": ResourceRequestForm(),
    }
    return render(request, "public/resources.html", ctx)


def get_involved(request):
    ctx = {
        "page": GetInvolvedPage.get_solo(),
        "volunteer_form": VolunteerInterestForm(),
        "partnership_form": PartnershipRequestForm(),
        "donation_form": DonationForm(),
        "donation_settings": DonationSettings.get_solo(),
    }
    return render(request, "public/get_involved.html", ctx)


def contact(request):
    ctx = {"form": ContactInquiryForm()}
    return render(request, "public/contact.html", ctx)


def newsletter(request):
    return render(request, "public/newsletter.html", {})


# --- Console: page content editing --------------------------------------

_PAGE_EDITORS = {
    "home": (HomePage, forms.HomePageForm, "Home page"),
    "about": (AboutPage, forms.AboutPageForm, "About page"),
    "what-we-do": (WhatWeDoPage, forms.WhatWeDoPageForm, "What We Do page"),
    "impact": (ImpactPage, forms.ImpactPageForm, "Impact page"),
    "resources": (ResourcesPage, forms.ResourcesPageForm, "Resources page"),
    "get-involved": (GetInvolvedPage, forms.GetInvolvedPageForm, "Get Involved page"),
}


@admin_required
def manage_site(request):
    obj = SiteSettings.get_solo()
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings updated.")
            return redirect("pages:manage_site")
    else:
        form = SiteSettingsForm(instance=obj)
    return render(request, "manage/site_settings.html", {"form": form})


@admin_required
def manage_org(request):
    obj = OrganizationProfile.get_solo()
    if request.method == "POST":
        form = OrganizationProfileForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization profile updated.")
            return redirect("pages:manage_org")
    else:
        form = OrganizationProfileForm(instance=obj)
    return render(request, "manage/org_form.html", {"form": form})


@admin_required
def manage_page(request, key):
    model_cls, form_cls, label = _PAGE_EDITORS[key]
    obj = model_cls.get_solo()
    if request.method == "POST":
        form = form_cls(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{label} content updated.")
            return redirect("pages:manage_page", key=key)
    else:
        form = form_cls(instance=obj)
    return render(
        request,
        "manage/page_form.html",
        {"form": form, "label": label, "key": key},
    )
