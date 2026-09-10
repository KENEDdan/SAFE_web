from django import forms

from apps.core.forms import set_file_accept_attrs, style_form

from .models import (
    ContactInquiry,
    Donation,
    NewsletterSubscriber,
    PartnershipRequest,
    ResourceRequest,
    VolunteerInterest,
)


class HoneypotMixin(forms.Form):
    """Bots fill hidden fields; humans don't. A non-empty ``website`` means drop
    the submission silently."""

    website = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "tabindex": "-1", "class": "hp-field", "aria-hidden": "true"}
        ),
    )

    @property
    def is_bot(self):
        return bool(self.is_valid() and self.cleaned_data.get("website"))


class PublicModelForm(HoneypotMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form(self)
        set_file_accept_attrs(self)
        self.fields["website"].widget.attrs["class"] = "hp-field"


class ContactInquiryForm(PublicModelForm):
    class Meta:
        model = ContactInquiry
        fields = ["name", "email", "phone", "inquiry_type", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class PartnershipRequestForm(PublicModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ["organization_name", "contact_person", "email", "phone", "proposal"]
        widgets = {
            "proposal": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Describe your partnership proposal and how we can work together..."}
            )
        }


class VolunteerInterestForm(PublicModelForm):
    class Meta:
        model = VolunteerInterest
        fields = ["name", "email", "phone", "skills", "interest"]
        widgets = {"interest": forms.Textarea(attrs={"rows": 5})}


class ResourceRequestForm(PublicModelForm):
    class Meta:
        model = ResourceRequest
        fields = ["name", "email", "phone", "location", "resource_needed"]
        widgets = {
            "resource_needed": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Please describe what resources your community needs (e.g. seeds, tools, training)"}
            )
        }


class DonationForm(PublicModelForm):
    class Meta:
        model = Donation
        fields = ["donor_name", "donor_email", "donor_phone", "amount", "currency", "message", "proof_of_payment"]
        widgets = {"message": forms.Textarea(attrs={"rows": 3})}


class NewsletterSubscriberForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-input", "placeholder": "Your email address", "required": True}
            )
        }
