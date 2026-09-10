"""A small generic CRUD helper for the console's content collections.

Every collection behaves the same way — a list, an add form, an edit form, a
delete confirmation — so each collection is described once by a ``Collection``
entry and the views are generated from it.
"""

from dataclasses import dataclass
from typing import Type

from django.contrib import messages
from django.db.models import Model
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import admin_required


@dataclass(frozen=True)
class Collection:
    key: str            # url slug, e.g. "programs"
    verbose: str        # singular label, e.g. "Programme"
    verbose_plural: str
    model: Type[Model]
    form: Type[ModelForm]
    columns: tuple      # (header, attr) pairs shown in the list table
    order: tuple = ("display_order", "id")

    @property
    def list_url(self):
        return f"content:manage_{self.key}"

    @property
    def create_url(self):
        return f"content:{self.key}_create"

    @property
    def edit_url(self):
        return f"content:{self.key}_edit"

    @property
    def delete_url(self):
        return f"content:{self.key}_delete"


def _cell(obj, attr):
    value = getattr(obj, attr)
    if callable(value):
        value = value()
    return value


def make_views(coll: Collection):
    @admin_required
    def list_view(request):
        objects = coll.model.objects.all().order_by(*coll.order)
        rows = [
            {"obj": o, "cells": [_cell(o, attr) for _, attr in coll.columns]}
            for o in objects
        ]
        return render(
            request,
            "manage/collection_list.html",
            {"coll": coll, "rows": rows, "headers": [h for h, _ in coll.columns]},
        )

    @admin_required
    def create_view(request):
        if request.method == "POST":
            form = coll.form(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, f"{coll.verbose} added.")
                return redirect(coll.list_url)
        else:
            form = coll.form()
        return render(
            request,
            "manage/collection_form.html",
            {"coll": coll, "form": form, "mode": "Add"},
        )

    @admin_required
    def edit_view(request, pk):
        obj = get_object_or_404(coll.model, pk=pk)
        if request.method == "POST":
            form = coll.form(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request, f"{coll.verbose} updated.")
                return redirect(coll.list_url)
        else:
            form = coll.form(instance=obj)
        return render(
            request,
            "manage/collection_form.html",
            {"coll": coll, "form": form, "mode": "Edit", "object": obj},
        )

    @admin_required
    def delete_view(request, pk):
        obj = get_object_or_404(coll.model, pk=pk)
        if request.method == "POST":
            obj.delete()
            messages.success(request, f"{coll.verbose} deleted.")
            return redirect(coll.list_url)
        return render(
            request,
            "manage/collection_confirm_delete.html",
            {"coll": coll, "object": obj},
        )

    return list_view, create_view, edit_view, delete_view
