from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN = "admin", "Administrator"


class User(AbstractUser):
    """Single-role staff account for the content console. Django's own
    ``is_superuser`` still grants everything; ``role`` exists so the console
    can show a badge and leave room for more roles later."""

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)
    must_change_password = models.BooleanField(
        default=True,
        help_text="Forces a password reset on first login for admin-created accounts.",
    )
    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_accounts",
    )
    phone_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_console_admin(self):
        return self.is_superuser or self.role == Role.ADMIN
