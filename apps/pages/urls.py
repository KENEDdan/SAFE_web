from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("what-we-do/", views.what_we_do, name="what_we_do"),
    path("impact/", views.impact, name="impact"),
    path("resources/", views.resources, name="resources"),
    path("get-involved/", views.get_involved, name="get_involved"),
    path("contact/", views.contact, name="contact"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("manage/site/", views.manage_site, name="manage_site"),
    path("manage/organization/", views.manage_org, name="manage_org"),
    path("manage/pages/<str:key>/", views.manage_page, name="manage_page"),
]
