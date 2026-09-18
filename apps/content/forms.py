from django import forms
from django.forms import inlineformset_factory

from apps.core.forms import set_file_accept_attrs, style_form

from .models import (
    Activity,
    ActivityImage,
    CoreValue,
    CrossCuttingTheme,
    GalleryImage,
    ImpactStat,
    Milestone,
    Partner,
    Program,
    Project,
    ProjectImage,
    Resource,
    TargetBeneficiary,
    TeamMember,
    Testimonial,
)

_TEXTAREAS = {
    "description": forms.Textarea(attrs={"rows": 4}),
    "body": forms.Textarea(attrs={"rows": 8}),
    "bio": forms.Textarea(attrs={"rows": 5}),
    "story": forms.Textarea(attrs={"rows": 5}),
    "outcomes": forms.Textarea(attrs={"rows": 4}),
    "summary": forms.Textarea(attrs={"rows": 2}),
}

_DATE_WIDGETS = {"activity_date": forms.DateInput(attrs={"type": "date"})}


class StyledModelForm(forms.ModelForm):
    """Applies the shared field styling + file-picker accept attributes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form(self)
        set_file_accept_attrs(self)


def _form(model_cls, field_names):
    widgets = {name: _TEXTAREAS[name] for name in field_names if name in _TEXTAREAS}
    widgets.update({name: _DATE_WIDGETS[name] for name in field_names if name in _DATE_WIDGETS})
    meta = type("Meta", (), {"model": model_cls, "fields": field_names, "widgets": widgets})
    return type(f"{model_cls.__name__}Form", (StyledModelForm,), {"Meta": meta})


ProgramForm = _form(Program, ["title", "summary", "description", "icon", "image", "display_order", "is_published"])
CrossCuttingThemeForm = _form(CrossCuttingTheme, ["title", "description", "image", "display_order", "is_published"])
CoreValueForm = _form(CoreValue, ["title", "description", "icon", "display_order", "is_published"])
TeamMemberForm = _form(
    TeamMember,
    ["name", "role", "qualifications", "bio", "photo", "email", "phone", "linkedin_url",
     "is_leadership", "display_order", "is_published"],
)
PartnerForm = _form(
    Partner,
    ["name", "logo", "website_url", "partnering_on", "blurb", "display_order", "is_published"],
)
ActivityForm = _form(
    Activity,
    ["title", "category", "activity_date", "location", "sponsors", "summary", "body",
     "thumbnail", "youtube_url", "display_order", "is_published"],
)
ProjectForm = _form(
    Project,
    ["title", "location", "status", "summary", "body", "outcomes", "thumbnail",
     "program", "is_featured", "display_order", "is_published"],
)
ImpactStatForm = _form(ImpactStat, ["value", "label", "icon", "display_order", "is_published"])
TargetBeneficiaryForm = _form(TargetBeneficiary, ["value", "label", "display_order", "is_published"])
MilestoneForm = _form(Milestone, ["title", "description", "period", "display_order", "is_published"])
TestimonialForm = _form(
    Testimonial,
    ["author", "role", "location", "story", "photo", "is_featured", "display_order", "is_published"],
)
GalleryImageForm = _form(GalleryImage, ["image", "caption", "category", "display_order", "is_published"])
ResourceForm = _form(
    Resource,
    ["name", "description", "category", "availability", "image", "display_order", "is_published"],
)


ProjectImageFormSet = inlineformset_factory(
    Project,
    ProjectImage,
    fields=["image", "caption"],
    extra=3,
    can_delete=True,
    widgets={
        "caption": forms.TextInput(attrs={"class": "form-input", "placeholder": "Caption (optional)"}),
    },
)

ActivityImageFormSet = inlineformset_factory(
    Activity,
    ActivityImage,
    fields=["image", "caption"],
    extra=3,
    can_delete=True,
    widgets={
        "caption": forms.TextInput(attrs={"class": "form-input", "placeholder": "Caption (optional)"}),
    },
)
