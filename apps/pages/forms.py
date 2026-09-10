from django import forms

from apps.core.forms import set_file_accept_attrs, style_form

from . import models


class _PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("rows", 4)
        style_form(self)
        set_file_accept_attrs(self)


def _page_form(model_cls):
    meta = type("Meta", (), {"model": model_cls, "exclude": ["id"]})
    return type(f"{model_cls.__name__}Form", (_PageForm,), {"Meta": meta})


HomePageForm = _page_form(models.HomePage)
AboutPageForm = _page_form(models.AboutPage)
WhatWeDoPageForm = _page_form(models.WhatWeDoPage)
ImpactPageForm = _page_form(models.ImpactPage)
ResourcesPageForm = _page_form(models.ResourcesPage)
GetInvolvedPageForm = _page_form(models.GetInvolvedPage)
