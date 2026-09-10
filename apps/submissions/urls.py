from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    # Public form endpoints
    path("submit/contact/", views.contact_submit, name="contact_submit"),
    path("submit/partnership/", views.partnership_submit, name="partnership_submit"),
    path("submit/volunteer/", views.volunteer_submit, name="volunteer_submit"),
    path("submit/resource-request/", views.resource_request_submit, name="resource_request_submit"),
    path("submit/donation/", views.donation_submit, name="donation_submit"),
    path("submit/newsletter/", views.newsletter_signup, name="newsletter_signup"),
    # Console inboxes
    path("manage/inbox/<str:key>/", views.inbox_list, name="inbox_list"),
    path("manage/inbox/<str:key>/<int:pk>/", views.inbox_detail, name="inbox_detail"),
    path("manage/resource-requests/", views.resource_request_list, name="resource_request_list"),
    path("manage/resource-requests/<int:pk>/", views.resource_request_detail, name="resource_request_detail"),
    path("manage/donations/", views.donation_list, name="donation_list"),
    path("manage/donations/settings/", views.donation_settings, name="donation_settings"),
    path("manage/donations/<int:pk>/", views.donation_detail, name="donation_detail"),
    path("manage/subscribers/", views.subscriber_list, name="subscriber_list"),
    path("manage/subscribers/export/", views.subscriber_export, name="subscriber_export"),
]
