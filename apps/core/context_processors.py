from .models import SiteSettings


def site_processor(request):
    return {"site": SiteSettings.get_solo()}
