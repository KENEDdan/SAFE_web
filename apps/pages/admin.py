from django.contrib import admin

from . import models

for _model in (
    models.HomePage,
    models.AboutPage,
    models.WhatWeDoPage,
    models.ImpactPage,
    models.ResourcesPage,
    models.GetInvolvedPage,
):
    admin.site.register(_model)
