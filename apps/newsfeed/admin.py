from django.contrib import admin

from .models import NewsMedia, NewsPost


class NewsMediaInline(admin.TabularInline):
    model = NewsMedia
    extra = 1


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "scheduled_for", "created_at")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [NewsMediaInline]
