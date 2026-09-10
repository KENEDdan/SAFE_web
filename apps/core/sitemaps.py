from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return [
            "pages:home",
            "pages:about",
            "pages:what_we_do",
            "pages:impact",
            "pages:resources",
            "pages:get_involved",
            "pages:contact",
            "content:project_list",
            "content:activity_list",
            "content:team_list",
            "newsfeed:post_list",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        from apps.content.models import Project

        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class NewsPostSitemap(Sitemap):
    priority = 0.4
    changefreq = "weekly"

    def items(self):
        from apps.newsfeed.models import NewsPost

        return NewsPost.objects.live()

    def lastmod(self, obj):
        return obj.updated_at


class ActivitySitemap(Sitemap):
    priority = 0.4
    changefreq = "monthly"

    def items(self):
        from apps.content.models import Activity

        return Activity.objects.published()

    def lastmod(self, obj):
        return obj.updated_at


SITEMAPS = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "activities": ActivitySitemap,
    "news": NewsPostSitemap,
}
