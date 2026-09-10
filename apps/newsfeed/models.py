import re

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from apps.core.validators import (
    validate_document_extension,
    validate_document_size,
    validate_image_extension,
    validate_image_size,
)

IMG_VALIDATORS = [validate_image_extension, validate_image_size]


class NewsCategory(models.TextChoices):
    UPDATE = "update", "Update"
    NEWS = "news", "News"
    FIELD_STORY = "field_story", "Field Story"
    EVENT = "event", "Event"
    PRESS_STATEMENT = "press_statement", "Press Statement"
    PUBLICATION = "publication", "Publication / Report"
    JOB = "job", "Job Advertisement"


# Categories that are PDF publications rather than ordinary posts.
DOCUMENT_REQUIRED_CATEGORIES = {NewsCategory.PRESS_STATEMENT, NewsCategory.PUBLICATION}


def youtube_id_from_url(url):
    if not url:
        return ""
    match = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})", url)
    return match.group(1) if match else ""


class NewsPostQuerySet(models.QuerySet):
    def live(self):
        now = timezone.now()
        return self.filter(is_published=True).filter(
            models.Q(scheduled_for__isnull=True) | models.Q(scheduled_for__lte=now)
        ).filter(
            models.Q(display_until__isnull=True) | models.Q(display_until__gte=now.date())
        )


class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=NewsCategory.choices, default=NewsCategory.UPDATE)
    brief_description = models.CharField(
        max_length=300, help_text="Shown on the news feed card."
    )
    body = models.TextField(help_text="Full detail shown on the article page.")

    thumbnail = models.ImageField(
        upload_to="newsfeed/thumbnails/", blank=True, null=True, validators=IMG_VALIDATORS
    )
    youtube_url = models.URLField(
        blank=True, help_text="YouTube link — used as the card preview when there is no thumbnail."
    )
    document = models.FileField(
        upload_to="newsfeed/documents/",
        blank=True,
        null=True,
        validators=[validate_document_extension, validate_document_size],
        help_text="Required for Press Statement and Publication posts. Shown as a download.",
    )

    is_published = models.BooleanField(default=True)
    scheduled_for = models.DateTimeField(
        null=True, blank=True, help_text="If set and in the future, the post stays hidden until then."
    )
    display_until = models.DateField(
        null=True, blank=True, help_text="Leave blank to keep the post visible indefinitely."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="news_posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NewsPostQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or "post"
            slug, n = base, 2
            while NewsPost.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("newsfeed:post_detail", args=[self.slug])

    @property
    def youtube_id(self):
        return youtube_id_from_url(self.youtube_url)

    @property
    def youtube_embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}" if self.youtube_id else ""

    @property
    def youtube_thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg" if self.youtube_id else ""

    @property
    def requires_document(self):
        return self.category in DOCUMENT_REQUIRED_CATEGORIES

    @property
    def is_scheduled(self):
        return bool(self.scheduled_for and self.scheduled_for > timezone.now())

    @property
    def is_expired(self):
        return bool(self.display_until and self.display_until < timezone.now().date())


class NewsMedia(models.Model):
    """A gallery item — image or YouTube video — on a post's detail page."""

    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(
        upload_to="newsfeed/gallery/", blank=True, null=True, validators=IMG_VALIDATORS
    )
    youtube_url = models.URLField(blank=True)
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.caption or f"Media for {self.post_id}"

    @property
    def youtube_id(self):
        return youtube_id_from_url(self.youtube_url)

    @property
    def youtube_embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}" if self.youtube_id else ""
