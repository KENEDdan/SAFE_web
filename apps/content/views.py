from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import admin_required
from apps.core.models import OrganizationProfile

from .collections import COLLECTIONS
from .forms import (
    ActivityForm,
    ActivityImageFormSet,
    ProjectForm,
    ProjectImageFormSet,
)
from .managecrud import make_views
from .models import Activity, ActivityCategory, Partner, Project, TeamMember

# --- Public views -----------------------------------------------------------


def project_list(request):
    projects = Project.objects.published()
    return render(request, "public/project_list.html", {"projects": projects})


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.published(), slug=slug)
    others = Project.objects.published().exclude(pk=project.pk)[:3]
    return render(request, "public/project_detail.html", {"project": project, "others": others})


def activity_list(request):
    category = request.GET.get("category", "")
    activities = Activity.objects.published()
    if category:
        activities = activities.filter(category=category)
    return render(
        request,
        "public/activity_list.html",
        {
            "activities": activities,
            "categories": ActivityCategory.choices,
            "active_category": category,
        },
    )


def activity_detail(request, slug):
    activity = get_object_or_404(Activity.objects.published(), slug=slug)
    others = Activity.objects.published().exclude(pk=activity.pk)[:3]
    return render(request, "public/activity_detail.html", {"activity": activity, "others": others})


def public_team(request):
    members = TeamMember.objects.published()
    return render(
        request,
        "public/team.html",
        {
            "leadership": members.filter(is_leadership=True),
            "staff": members.filter(is_leadership=False),
            "org": OrganizationProfile.get_solo(),
            "partners": Partner.objects.published(),
        },
    )


# --- Generic collection CRUD (programs, values, testimonials, partners, ...) ---

_generated = {}
for _coll in COLLECTIONS:
    _list, _create, _edit, _delete = make_views(_coll)
    _generated[f"{_coll.key}_list"] = _list
    _generated[f"{_coll.key}_create"] = _create
    _generated[f"{_coll.key}_edit"] = _edit
    _generated[f"{_coll.key}_delete"] = _delete

globals().update(_generated)


# --- Slug + inline-gallery CRUD (projects, activities) ---------------------


def _slug_gallery_views(model, form_cls, formset_cls, list_url, list_tmpl, form_tmpl, del_tmpl, noun):
    @admin_required
    def manage(request):
        return render(request, list_tmpl, {"objects": model.objects.all(), "noun": noun})

    @admin_required
    def create(request):
        if request.method == "POST":
            form = form_cls(request.POST, request.FILES)
            formset = formset_cls(request.POST, request.FILES, prefix="images")
            if form.is_valid() and formset.is_valid():
                obj = form.save()
                formset.instance = obj
                formset.save()
                messages.success(request, f"{noun} added.")
                return redirect(list_url)
        else:
            form, formset = form_cls(), formset_cls(prefix="images")
        return render(request, form_tmpl, {"form": form, "formset": formset, "mode": "Add", "noun": noun})

    @admin_required
    def edit(request, pk):
        obj = get_object_or_404(model, pk=pk)
        if request.method == "POST":
            form = form_cls(request.POST, request.FILES, instance=obj)
            formset = formset_cls(request.POST, request.FILES, instance=obj, prefix="images")
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, f"{noun} updated.")
                return redirect(list_url)
        else:
            form = form_cls(instance=obj)
            formset = formset_cls(instance=obj, prefix="images")
        return render(request, form_tmpl, {"form": form, "formset": formset, "mode": "Edit", "object": obj, "noun": noun})

    @admin_required
    def delete(request, pk):
        obj = get_object_or_404(model, pk=pk)
        if request.method == "POST":
            obj.delete()
            messages.success(request, f"{noun} deleted.")
            return redirect(list_url)
        return render(request, del_tmpl, {"object": obj, "noun": noun})

    return manage, create, edit, delete


manage_projects, project_create, project_edit, project_delete = _slug_gallery_views(
    Project, ProjectForm, ProjectImageFormSet,
    "content:manage_projects",
    "content/project_manage_list.html", "content/project_form.html",
    "content/project_confirm_delete.html", "Project",
)

manage_activities, activity_create, activity_edit, activity_delete = _slug_gallery_views(
    Activity, ActivityForm, ActivityImageFormSet,
    "content:manage_activities",
    "content/activity_manage_list.html", "content/activity_form.html",
    "content/activity_confirm_delete.html", "Activity",
)
