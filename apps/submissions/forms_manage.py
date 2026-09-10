from django import forms

from apps.core.forms import style_form

from .models import DonationSettings


class DonationSettingsForm(forms.ModelForm):
    class Meta:
        model = DonationSettings
        exclude = ["id", "updated_at"]
        widgets = {"instructions": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form(self)
