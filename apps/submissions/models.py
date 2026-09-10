import secrets

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import SingletonModel
from apps.core.validators import validate_document_extension, validate_document_size


class Submission(models.Model):
    """Common shape for every public form landing in the console inbox."""

    is_handled = models.BooleanField(default=False)
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+",
    )
    handled_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class InquiryType(models.TextChoices):
    GENERAL = "general", "General Inquiry"
    PROGRAMS = "programs", "Programmes"
    MEDIA = "media", "Media"
    VOLUNTEER = "volunteer", "Volunteering"
    OTHER = "other", "Other"


class ContactInquiry(Submission):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    inquiry_type = models.CharField(
        max_length=20, choices=InquiryType.choices, default=InquiryType.GENERAL
    )
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    class Meta(Submission.Meta):
        verbose_name = "Contact inquiry"
        verbose_name_plural = "Contact inquiries"

    def __str__(self):
        return f"{self.name} — {self.get_inquiry_type_display()}"


class PartnershipRequest(Submission):
    organization_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    proposal = models.TextField(help_text="Describe the partnership proposal and how we can work together.")

    def __str__(self):
        return self.organization_name


class VolunteerInterest(Submission):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    interest = models.TextField(help_text="Background, skills, and areas of interest.")

    def __str__(self):
        return self.name


class ResourceRequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    DISTRIBUTED = "distributed", "Distributed"
    DECLINED = "declined", "Declined"


class ResourceRequest(Submission):
    name = models.CharField(max_length=150, help_text="Contact person or group representative.")
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=150, help_text="Community / payam / county")
    resource_needed = models.TextField(
        help_text="Describe what resources your community needs (e.g. seeds, tools, training)."
    )
    status = models.CharField(
        max_length=20, choices=ResourceRequestStatus.choices, default=ResourceRequestStatus.PENDING
    )

    def __str__(self):
        return f"{self.name} — {self.location}"


class DonationSettings(SingletonModel):
    bank_name = models.CharField(max_length=120, blank=True, default="Ecobank South Sudan")
    account_name = models.CharField(max_length=150, blank=True, default="SAFE - Sustainable Agriculture & Forest Environment")
    account_number = models.CharField(max_length=50, blank=True)
    branch = models.CharField(max_length=120, blank=True)
    swift_code = models.CharField(max_length=30, blank=True)
    mobile_money_note = models.CharField(max_length=200, blank=True)
    instructions = models.TextField(
        blank=True,
        default=(
            "Please transfer your donation to the account below and include your reference "
            "code in the transfer description, then upload your proof of payment. Our team "
            "will confirm receipt."
        ),
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Donation settings"
        verbose_name_plural = "Donation settings"

    def __str__(self):
        return "Donation settings"


class DonationStatus(models.TextChoices):
    PENDING = "pending", "Pending confirmation"
    CONFIRMED = "confirmed", "Confirmed"
    REJECTED = "rejected", "Proof rejected"


def generate_reference():
    return "SAFE-DON-" + secrets.token_hex(3).upper()


class Donation(models.Model):
    reference_code = models.CharField(max_length=20, unique=True, default=generate_reference)
    donor_name = models.CharField(max_length=150)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=40, blank=True)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("1.00"))]
    )
    currency = models.CharField(max_length=3, default="USD")
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=DonationStatus.choices, default=DonationStatus.PENDING
    )
    proof_of_payment = models.FileField(
        upload_to="donations/proofs/",
        blank=True,
        null=True,
        validators=[validate_document_extension, validate_document_size],
    )
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.donor_name} — {self.currency} {self.amount} ({self.get_status_display()})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
