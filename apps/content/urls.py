from django.urls import path

from . import views
from .collections import COLLECTIONS

app_name = "content"

urlpatterns = [
    # Public
    path("projects/", views.project_list, name="project_list"),
    path("activities/", views.activity_list, name="activity_list"),
    path("team/", views.public_team, name="team_list"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("activities/<slug:slug>/", views.activity_detail, name="activity_detail"),
    # Projects management (bespoke)
    path("manage/projects/", views.manage_projects, name="manage_projects"),
    path("manage/projects/add/", views.project_create, name="projects_create"),
    path("manage/projects/<int:pk>/edit/", views.project_edit, name="projects_edit"),
    path("manage/projects/<int:pk>/delete/", views.project_delete, name="projects_delete"),
    # Activities management (bespoke)
    path("manage/activities/", views.manage_activities, name="manage_activities"),
    path("manage/activities/add/", views.activity_create, name="activities_create"),
    path("manage/activities/<int:pk>/edit/", views.activity_edit, name="activities_edit"),
    path("manage/activities/<int:pk>/delete/", views.activity_delete, name="activities_delete"),
]

# Generic collection routes: manage_<key>, <key>_create, <key>_edit, <key>_delete
for _coll in COLLECTIONS:
    urlpatterns += [
        path(f"manage/{_coll.key}/", getattr(views, f"{_coll.key}_list"), name=f"manage_{_coll.key}"),
        path(f"manage/{_coll.key}/add/", getattr(views, f"{_coll.key}_create"), name=f"{_coll.key}_create"),
        path(f"manage/{_coll.key}/<int:pk>/edit/", getattr(views, f"{_coll.key}_edit"), name=f"{_coll.key}_edit"),
        path(f"manage/{_coll.key}/<int:pk>/delete/", getattr(views, f"{_coll.key}_delete"), name=f"{_coll.key}_delete"),
    ]
