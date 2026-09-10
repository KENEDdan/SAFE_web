from django.urls import path

from . import views

app_name = "newsfeed"

urlpatterns = [
    path("news/", views.post_list, name="post_list"),
    path("news/manage/", views.manage_list, name="manage_list"),
    path("news/manage/calendar/", views.content_calendar, name="content_calendar"),
    path("news/manage/add/", views.post_create, name="post_create"),
    path("news/manage/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("news/manage/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("news/<slug:slug>/", views.post_detail, name="post_detail"),
]
