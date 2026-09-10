from django.db import models

from .validators import validate_image_extension, validate_image_size


class SingletonModel(models.Model):
    """Base for one-row content models edited through a single console form."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    organization_name = models.CharField(max_length=150, default="SAFE")
    organization_full_name = models.CharField(
        max_length=200,
        default="Sustainable Agriculture & Forest Environment",
    )
    tagline = models.CharField(max_length=200, default="Restoring Nature, Sustaining Life")
    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
    )
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)

    # Contact block — powers the footer, the contact page, and structured data.
    contact_email = models.EmailField(default="ayom.mawien@safe-ss.org")
    secondary_email = models.EmailField(blank=True, default="admin@safengo.org")
    phone_primary = models.CharField(max_length=40, blank=True, default="+211 922 144 884")
    phone_secondary = models.CharField(max_length=40, blank=True, default="+211 989 446 688")
    whatsapp_number = models.CharField(
        max_length=40, blank=True, default="211989446688",
        help_text="Digits only, international format — used to build the wa.me link.",
    )
    address = models.CharField(max_length=255, blank=True, default="Juba, Central Equatoria, South Sudan")
    office_hours = models.CharField(max_length=200, blank=True, default="Mon–Fri, 8:00 AM – 5:00 PM")
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed link, optional.")

    facebook_url = models.URLField(blank=True, default="https://facebook.com/safengo")
    twitter_url = models.URLField(blank=True, default="https://twitter.com/safengo")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/company/safengo")
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    footer_blurb = models.TextField(
        default=(
            "SAFE is a non-governmental organization dedicated to building resilient "
            "communities through sustainable agriculture and environmental stewardship "
            "in South Sudan."
        )
    )
    newsletter_blurb = models.CharField(
        max_length=255,
        default="Stay connected with our mission to restore nature and sustain life.",
    )

    meta_description = models.CharField(
        max_length=255,
        default=(
            "SAFE — Sustainable Agriculture & Forest Environment. Building climate-resilient "
            "communities in South Sudan through sustainable farming, food security, and "
            "environmental conservation."
        ),
    )

    donate_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    @property
    def whatsapp_link(self):
        digits = "".join(ch for ch in self.whatsapp_number if ch.isdigit())
        return f"https://wa.me/{digits}" if digits else ""


class OrganizationProfile(SingletonModel):
    """Headcount and reach figures shown on the About / Team pages and the
    console dashboard."""

    heading = models.CharField(max_length=150, default="SAFE at a glance")
    intro = models.CharField(
        max_length=255,
        blank=True,
        default="The people and reach behind our work across South Sudan.",
    )

    staff_count = models.PositiveIntegerField(default=0, help_text="Full-time staff.")
    field_staff_count = models.PositiveIntegerField(default=0, help_text="Field officers / extension workers.")
    volunteers_count = models.PositiveIntegerField(default=0, help_text="Active volunteers.")
    communities_served = models.PositiveIntegerField(default=0)
    states_covered = models.PositiveIntegerField(default=0)
    partners_count = models.PositiveIntegerField(default=0)
    years_active = models.PositiveIntegerField(default=0)

    auto_staff_count = models.BooleanField(
        default=True,
        help_text="Show the number of published team members instead of the fixed staff figure above.",
    )
    show_on_about = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organization profile"
        verbose_name_plural = "Organization profile"

    def __str__(self):
        return "Organization profile"

    @property
    def effective_staff_count(self):
        if self.auto_staff_count:
            from apps.content.models import TeamMember

            return TeamMember.objects.published().count()
        return self.staff_count

    @property
    def tiles(self):
        """(value, label) pairs for the non-zero figures, ready to render."""
        rows = [
            (self.effective_staff_count, "Team members"),
            (self.field_staff_count, "Field officers"),
            (self.volunteers_count, "Active volunteers"),
            (self.communities_served, "Communities served"),
            (self.states_covered, "States covered"),
            (self.partners_count, "Partners"),
            (self.years_active, "Years active"),
        ]
        return [(v, label) for v, label in rows if v]
