# SAFE — Sustainable Agriculture & Forest Environment

A Django rebuild of **safe-ss.org** with a content-management console. Every
public page section is database-backed and editable by staff — no code changes
needed to update the site.

## Stack

- Django 5.2, PostgreSQL, Pillow, WhiteNoise, django-axes (login lockout)
- No HR / finance / procurement / audit modules — content management only
- Structure follows the sibling `integrity_south_sudan` project; branding is SAFE's own (green / earth / orange)

## Apps

| App | Purpose |
|-----|---------|
| `accounts` | Single `admin` role, forced first-login password reset, staff-account management |
| `core` | `SiteSettings` singleton (logo, contact, socials, SEO), validators, `seed_safe` command |
| `pages` | Six one-row page models (Home, About, What We Do, Impact, Resources, Get Involved) + their console editors |
| `content` | Collections: programmes, cross-cutting themes, projects (+ galleries), core values, team, impact stats, target beneficiaries, milestones, testimonials, gallery, resource catalogue |
| `newsfeed` | News feed posts by category (update, news, field story, event, press statement, publication, job) with thumbnail / YouTube / PDF, per-post gallery, and publish scheduling (`scheduled_for` / `display_until`) |
| `submissions` | Public form inboxes: contact, partnership, volunteer, resource request, donations (+ bank settings), newsletter |

## Local setup

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
cp .env.example .env          # fill SECRET_KEY; Postgres defaults point at localhost:55432

# Postgres (either one):
docker compose up -d db                                   # via compose
# ...or a standalone container:
docker run -d --name safe_db -e POSTGRES_DB=safe_db -e POSTGRES_USER=safe_user \
  -e POSTGRES_PASSWORD=safe_pass -p 55432:5432 postgres:16-alpine

.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py seed_safe        # loads all launch content + seed images
.venv/Scripts/python manage.py createsuperuser  # then set role="admin", must_change_password=False
.venv/Scripts/python manage.py runserver
```

- Public site: `http://127.0.0.1:8000/`
- Console: `http://127.0.0.1:8000/accounts/login/` → dashboard at `/accounts/dashboard/`
- Django admin (fallback): `/django-admin/`

## Docker

`docker compose up --build` runs migrate + collectstatic + gunicorn on port 8006.

## Content model

- **Singletons** (`SiteSettings`, the six `*Page` models, `DonationSettings`) hold the fixed prose of each page and are edited through one form each.
- **Collections** are the repeating items. Each has `display_order` (low = first) and `is_published` (unchecked = hidden from the public site).
- `seed_safe` is idempotent: it re-saves singletons and only fills a collection when it is empty.
