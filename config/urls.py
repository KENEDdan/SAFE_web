import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.views.static import serve as serve_static

from apps.core.sitemaps import SITEMAPS


def robots_txt(request):
    # Staff paths are deliberately absent: listing them here would publish the
    # console's location. They return 404 to anonymous visitors instead.
    lines = [
        "User-agent: *",
        "Disallow:",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


_STAFF = settings.STAFF_URL_PREFIX

urlpatterns = [
    path("robots.txt", robots_txt),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(f"{_STAFF}/django-admin/", admin.site.urls),
    path(f"{_STAFF}/", include("apps.accounts.urls", namespace="accounts")),
    path("", include("apps.content.urls", namespace="content")),
    path("", include("apps.newsfeed.urls", namespace="newsfeed")),
    path("", include("apps.submissions.urls", namespace="submissions")),
    path("", include("apps.pages.urls", namespace="pages")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    _PUBLIC_MEDIA_PREFIXES = [
        "site", "pages", "programs", "themes", "projects", "team", "testimonials",
        "gallery", "resources", "newsfeed",
    ]
    urlpatterns += [
        re_path(
            r"^media/(?P<path>(?:%s)/.*)$" % "|".join(re.escape(p) for p in _PUBLIC_MEDIA_PREFIXES),
            serve_static,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]
