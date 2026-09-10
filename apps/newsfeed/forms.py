from django import forms
from django.forms import inlineformset_factory

from apps.core.forms import set_file_accept_attrs, style_form

from .models import DOCUMENT_REQUIRED_CATEGORIES, NewsMedia, NewsPost


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = [
            "title", "category", "brief_description", "body",
            "thumbnail", "youtube_url", "document",
            "is_published", "scheduled_for", "display_until",
        ]
        widgets = {
            "brief_description": forms.Textarea(attrs={"rows": 2}),
            "body": forms.Textarea(attrs={"rows": 10}),
            "scheduled_for": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "display_until": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form(self)
        set_file_accept_attrs(self)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("category") in DOCUMENT_REQUIRED_CATEGORIES and not cleaned.get("document"):
            self.add_error("document", "A PDF document is required for this category.")
        return cleaned


NewsMediaFormSet = inlineformset_factory(
    NewsPost,
    NewsMedia,
    fields=["image", "youtube_url", "caption"],
    extra=3,
    can_delete=True,
    widgets={
        "youtube_url": forms.URLInput(attrs={"class": "form-input", "placeholder": "YouTube link"}),
        "caption": forms.TextInput(attrs={"class": "form-input", "placeholder": "Caption (optional)"}),
    },
)
