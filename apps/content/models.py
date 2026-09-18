from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.validators import validate_image_extension, validate_image_size

IMG_VALIDATORS = [validate_image_extension, validate_image_size]


class OrderedPublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class BaseContent(models.Model):
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderedPublishedQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ["display_order", "id"]


class Program(BaseContent):
    """A programme shown on the What We Do page."""

    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=40, blank=True,
        help_text="Optional emoji or short label shown in the card badge.",
    )
    image = models.ImageField(upload_to="programs/", blank=True, null=True, validators=IMG_VALIDATORS)

    def __str__(self):
        return self.title


class CrossCuttingTheme(BaseContent):
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="themes/", blank=True, null=True, validators=IMG_VALIDATORS)

    def __str__(self):
        return self.title


class CoreValue(BaseContent):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.title


class TeamMember(BaseContent):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    qualifications = models.CharField(max_length=255, blank=True, help_text="e.g. MSc Agronomy, University of Juba")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True, validators=IMG_VALIDATORS)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    linkedin_url = models.URLField(blank=True)
    is_leadership = models.BooleanField(
        default=False,
        help_text="Leadership members are shown first, in the leadership section.",
    )

    def __str__(self):
        return f"{self.name} — {self.role}"


class Partner(BaseContent):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="partners/", blank=True, null=True, validators=IMG_VALIDATORS)
    website_url = models.URLField(blank=True)
    partnering_on = models.CharField(
        max_length=255, blank=True, help_text="e.g. Climate-smart agriculture, farmer training"
    )
    blurb = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class ActivityCategory(models.TextChoices):
    TRAINING = "training", "Training / Workshop"
    FIELD_ACTIVITY = "field_activity", "Field Activity"
    COMMUNITY_EVENT = "community_event", "Community Event"
    DIALOGUE = "dialogue", "Community Dialogue"
    DISTRIBUTION = "distribution", "Distribution"
    AWARENESS = "awareness", "Awareness / Sensitization"


class Activity(BaseContent):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(
        max_length=30, choices=ActivityCategory.choices, default=ActivityCategory.FIELD_ACTIVITY
    )
    activity_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True)
    sponsors = models.CharField(max_length=255, blank=True, help_text="Partners / funders, comma-separated")
    summary = models.CharField(max_length=300)
    body = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="activities/", blank=True, null=True, validators=IMG_VALIDATORS)
    youtube_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-activity_date", "display_order", "-id"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or "activity"
            slug, n = base, 2
            while Activity.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("content:activity_detail", args=[self.slug])

    @property
    def youtube_id(self):
        import re

        m = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})", self.youtube_url or "")
        return m.group(1) if m else ""

    @property
    def youtube_embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}" if self.youtube_id else ""

    @property
    def youtube_thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg" if self.youtube_id else ""


class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="activities/gallery/", validators=IMG_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.caption or f"Image #{self.pk}"


class ProjectStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    ONGOING = "ongoing", "Ongoing"
    COMPLETED = "completed", "Completed"


class Project(BaseContent):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    location = models.CharField(max_length=150, blank=True, help_text="e.g. Warrap State")
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ONGOING)
    summary = models.CharField(max_length=300)
    body = models.TextField(blank=True)
    outcomes = models.TextField(
        blank=True,
        help_text="One outcome per line — shown as a bulleted list.",
    )
    thumbnail = models.ImageField(upload_to="projects/", blank=True, null=True, validators=IMG_VALIDATORS)
    is_featured = models.BooleanField(default=False, help_text="Featured projects appear on the homepage.")
    program = models.ForeignKey(
        Program, blank=True, null=True, on_delete=models.SET_NULL, related_name="projects",
        help_text="Which What We Do programme this project delivers, if any.",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or "project"
            slug = base
            n = 2
            while Project.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("content:project_detail", args=[self.slug])

    @property
    def outcome_list(self):
        return [line.strip() for line in self.outcomes.splitlines() if line.strip()]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/", validators=IMG_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.caption or f"Image #{self.pk}"


class ImpactStat(BaseContent):
    value = models.CharField(max_length=40, help_text="e.g. 5,000 or 3 Years")
    label = models.CharField(max_length=120, help_text="e.g. Households Reached")
    icon = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"{self.value} {self.label}"


class TargetBeneficiary(BaseContent):
    value = models.CharField(max_length=60)
    label = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.value} — {self.label}"


class Milestone(BaseContent):
    """A step on the impact / pathway-to-change timeline."""

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    period = models.CharField(max_length=60, blank=True, help_text="e.g. Year 1 or 2024")

    def __str__(self):
        return self.title


class Testimonial(BaseContent):
    author = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True, help_text="e.g. Farmer, Warrap State")
    location = models.CharField(max_length=150, blank=True)
    story = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True, validators=IMG_VALIDATORS)
    is_featured = models.BooleanField(default=False, help_text="Featured testimonials appear on the homepage.")

    def __str__(self):
        return f"{self.author} ({self.role})" if self.role else self.author


class GalleryImage(BaseContent):
    image = models.ImageField(upload_to="gallery/", validators=IMG_VALIDATORS)
    caption = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.caption or f"Gallery image #{self.pk}"


class ResourceStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    LIMITED = "limited", "Limited"
    OUT_OF_STOCK = "out_of_stock", "Out of stock"


class Resource(BaseContent):
    """An item in the community resource-distribution catalogue."""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=80, blank=True, help_text="e.g. Seeds, Tools, Training")
    availability = models.CharField(
        max_length=20, choices=ResourceStatus.choices, default=ResourceStatus.AVAILABLE
    )
    image = models.ImageField(upload_to="resources/", blank=True, null=True, validators=IMG_VALIDATORS)

    def __str__(self):
        return self.name
