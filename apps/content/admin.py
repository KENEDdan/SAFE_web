from django.contrib import admin

from . import models


class ProjectImageInline(admin.TabularInline):
    model = models.ProjectImage
    extra = 1


class ActivityImageInline(admin.TabularInline):
    model = models.ActivityImage
    extra = 1


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "status", "is_featured", "is_published", "display_order")
    list_filter = ("status", "is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "activity_date", "location", "is_published")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ActivityImageInline]


for _model in (
    models.Program,
    models.CrossCuttingTheme,
    models.CoreValue,
    models.TeamMember,
    models.Partner,
    models.ImpactStat,
    models.TargetBeneficiary,
    models.Milestone,
    models.Testimonial,
    models.GalleryImage,
    models.Resource,
):
    admin.site.register(_model)
