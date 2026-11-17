---
id: computing-software.web-development.django.securing-the-admin
name: securing-the-admin
category: computing-software
field: web-development
product: django
tags: [django-admin, admin-security, admin-url, staff-permissions, admin-mfa, admin-audit-log, logentry, django-otp]
level: practitioner
status: verified
description: "Hardening the Django admin: non-default URL and network restriction, least-privilege staff permissions, MFA, rate limiting, audit via LogEntry and safe customisations."
sources:
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#adminsite-objects
  - https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
  - https://django-otp-official.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Securing the Django admin

**Goal:** the admin - a powerful UI over your whole database - is reachable only by the right people, protected by more than a password, and auditable.

## 1. Reduce exposure
- Move it off `/admin/` (`path("ops-9f3k/", admin.site.urls)`) to cut automated noise - obscurity, not a control.
- Restrict by network where possible: VPN or an IP allowlist at the reverse proxy (consult your proxy's documentation for the directive), or serve admin from a separate internal hostname.
- Never enable `DEBUG` in production (`python manage.py check --deploy` reports `security.W018` when it is on, and warnings such as W004 HSTS, W008 SSL redirect, W012 and W016 secure cookies).

## 2. Least privilege
- Few superusers. Give staff `is_staff` + group permissions (view/add/change/delete per model).
- Prefer `view` permission for support roles.
- Override `has_change_permission`/`has_delete_permission`/`get_queryset` for object-level limits (e.g. staff only see their region).
- Don't expose sensitive fields (password hashes, tokens): exclude them or make readonly; `UserAdmin` already handles password fields properly.

## 3. Strong authentication
- MFA for admin users: `django-otp` (`OTPAdminSite`) or `django-two-factor-auth`, or put admin behind SSO (OIDC via `mozilla-django-oidc`/`django-allauth`).
- Rate-limit admin login (`django-axes` lockout; read its docs for the lockout parameters).
- Session: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, short `SESSION_COOKIE_AGE` for staff if possible.

## 4. Audit
The admin writes `LogEntry` (`django_admin_log`) for add/change/delete via the admin - not for `queryset.update()` in actions or changes outside the admin. Log actions explicitly (`self.log_change(...)` / a proper audit package like `django-auditlog` or `django-simple-history`), and ship logs off-box.

## 5. Safe customisations
- Custom admin views must be wrapped with `self.admin_site.admin_view(view)` (enforces login, staff, CSRF, no-cache).
- `format_html` (never `mark_safe` with user data) in `list_display` methods - admin XSS is real since data comes from users.

## Verify
- [ ] Admin login requires a second factor; brute force gets throttled.
- [ ] A support user can't delete or see models outside their groups.
- [ ] Bulk actions appear in the audit log; `check --deploy` passes.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. Packages installed: django-otp 1.7.5, django-axes 8.3.1, django-auditlog 3.4.1, django-simple-history 3.13.0, mozilla-django-oidc 5.0.2; django-two-factor-auth and django-allauth existence checked with `pip index versions`.
- Run: `check --deploy` listed W002, W004, W008, W009, W012, W016 on the scratch settings and `security.W018` when `DEBUG = True`.
- Run: `from django_otp.admin import OTPAdminSite` imports; `ModelAdmin.log_change`, `get_queryset`, `has_*_permission` exist; `AdminSite.admin_view` wraps with `has_permission`, `never_cache` and `csrf_protect` (sites.py source); a queryset `update()` action produced 0 `LogEntry` rows.
- Removed: the nginx `allow`/`deny` snippet, which was not run here (no nginx).
