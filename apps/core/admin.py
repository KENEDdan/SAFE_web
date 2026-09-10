from django.contrib import admin

from .models import OrganizationProfile, SiteSettings


class _SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(_SingletonAdmin):
    pass


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(_SingletonAdmin):
    pass
