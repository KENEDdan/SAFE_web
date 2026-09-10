from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class SafeUserAdmin(UserAdmin):
    list_display = ("username", "email", "get_full_name", "role", "is_active", "must_change_password")
    list_filter = ("role", "is_active", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        ("SAFE console", {"fields": ("role", "must_change_password", "phone_number", "created_by")}),
    )
