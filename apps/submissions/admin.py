from django.contrib import admin

from . import models


@admin.register(models.Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("reference_code", "donor_name", "amount", "currency", "status", "created_at")
    list_filter = ("status", "currency")
    readonly_fields = ("reference_code", "created_at")


@admin.register(models.NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at", "is_active")
    search_fields = ("email",)


for _model in (
    models.ContactInquiry,
    models.PartnershipRequest,
    models.VolunteerInterest,
    models.ResourceRequest,
    models.DonationSettings,
):
    admin.site.register(_model)
