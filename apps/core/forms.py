from django import forms
from django.core.validators import FileExtensionValidator

from .models import OrganizationProfile, SiteSettings


def set_file_accept_attrs(form):
    """Set an ``accept`` attribute on file/image inputs from their model
    field's FileExtensionValidator, so the OS file picker filters by extension
    — the validator stays the single source of truth."""
    model = getattr(getattr(form, "_meta", None), "model", None)
    if model is None:
        return
    for name, field in form.fields.items():
        if not isinstance(field, (forms.FileField, forms.ImageField)):
            continue
        try:
            model_field = model._meta.get_field(name)
        except Exception:
            continue
        for validator in getattr(model_field, "validators", []):
            if isinstance(validator, FileExtensionValidator):
                field.widget.attrs["accept"] = ",".join(
                    f".{ext}" for ext in validator.allowed_extensions
                )
                break


def style_form(form):
    """Add ``form-input`` to every visible widget except checkboxes."""
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
            continue
        css = widget.attrs.get("class", "")
        widget.attrs["class"] = (css + " form-input").strip()


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        exclude = ["id", "updated_at"]
        widgets = {
            "footer_blurb": forms.Textarea(attrs={"rows": 3}),
            "meta_description": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form(self)
        set_file_accept_attrs(self)


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        exclude = ["id", "updated_at"]
        widgets = {"intro": forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form(self)
