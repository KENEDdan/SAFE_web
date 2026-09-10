from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.decorators import admin_required

from .forms import NewsMediaFormSet, NewsPostForm
from .models import NewsCategory, NewsPost


def post_list(request):
    category = request.GET.get("category", "")
    posts = NewsPost.objects.live()
    if category:
        posts = posts.filter(category=category)
    return render(
        request,
        "public/news_list.html",
        {
            "posts": posts,
            "categories": NewsCategory.choices,
            "active_category": category,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(NewsPost.objects.live(), slug=slug)
    related = NewsPost.objects.live().exclude(pk=post.pk)[:3]
    return render(request, "public/news_detail.html", {"post": post, "related": related})


@admin_required
def manage_list(request):
    return render(request, "manage/news_list.html", {"posts": NewsPost.objects.all()})


@admin_required
def content_calendar(request):
    posts = NewsPost.objects.filter(
        scheduled_for__isnull=False
    ).order_by("scheduled_for") | NewsPost.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=30)
    )
    posts = posts.distinct().order_by("scheduled_for", "-created_at")
    return render(request, "manage/news_calendar.html", {"posts": posts})


@admin_required
def post_create(request):
    if request.method == "POST":
        form = NewsPostForm(request.POST, request.FILES)
        formset = NewsMediaFormSet(request.POST, request.FILES, prefix="gallery")
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            formset.instance = post
            formset.save()
            messages.success(request, f'"{post.title}" was published.')
            return redirect("newsfeed:manage_list")
    else:
        form = NewsPostForm()
        formset = NewsMediaFormSet(prefix="gallery")
    return render(
        request,
        "manage/news_form.html",
        {"form": form, "formset": formset, "mode": "Add"},
    )


@admin_required
def post_edit(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    if request.method == "POST":
        form = NewsPostForm(request.POST, request.FILES, instance=post)
        formset = NewsMediaFormSet(request.POST, request.FILES, instance=post, prefix="gallery")
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'"{post.title}" was updated.')
            return redirect("newsfeed:manage_list")
    else:
        form = NewsPostForm(instance=post)
        formset = NewsMediaFormSet(instance=post, prefix="gallery")
    return render(
        request,
        "manage/news_form.html",
        {"form": form, "formset": formset, "mode": "Edit", "object": post},
    )


@admin_required
def post_delete(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    if request.method == "POST":
        title = post.title
        post.delete()
        messages.success(request, f'"{title}" was deleted.')
        return redirect("newsfeed:manage_list")
    return render(request, "manage/news_confirm_delete.html", {"object": post})
