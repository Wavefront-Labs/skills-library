---
id: computing-software.web-development.django.authentication-permissions-and-security
name: authentication-permissions-and-security
category: computing-software
field: web-development
product: django
tags: [django, authentication, custom-user-model, permissions, csrf, security-middleware, settings, python, web-development, django-permissions]
level: advanced
status: docs-checked
description: "Django auth done right: custom user model from day one, permission/group patterns, CSRF mechanics, and the security settings an audit checks."
sources:
  - https://docs.djangoproject.com/en/stable/topics/auth/customizing/
  - https://docs.djangoproject.com/en/stable/topics/security/
  - https://docs.djangoproject.com/en/stable/howto/csrf/
  - https://docs.djangoproject.com/en/stable/ref/settings/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Django authentication, permissions, and security settings

**Goal:** an auth setup that doesn't need a painful migration later, and the
settings checklist a security review will actually ask about.

## 1. Custom user model — decide before the first migration, not after
```python
# AUTH_USER_MODEL = "accounts.User" in settings.py, set before the first migrate
class User(AbstractUser):
    email = models.EmailField(unique=True)
```
Swapping `AUTH_USER_MODEL` after the initial migration has run is painful —
every `ForeignKey(User)` across every app needs a new migration path, and
existing data must be moved by hand. Django's docs show a custom user model that subclasses `AbstractUser` and behaves identically to the default, and say to point `AUTH_USER_MODEL` at it before creating any migrations or running `migrate` for the first time; changing it after tables exist is significantly more difficult.

## 2. Permissions — model-level, object-level, and DRF-specific
- **Model-level** (`add_order`, `change_order` — auto-created per model):
  check with `user.has_perm('app.change_order')`. Fine for admin-style access
  control, not for "can this user edit *this specific* order."
- **Object-level**: Django's permission framework has no built-in per-object
  check — use `django-guardian` for genuine row-level permissions, or (more
  commonly, and simpler) just check ownership explicitly in the view
  (`if order.customer != request.user: raise PermissionDenied`). Don't reach
  for a permissions library before confirming a plain ownership check isn't
  enough.
- **Groups**: assign permissions to a `Group`, add users to groups, instead of
  granting permissions to users one by one — the maintainable pattern once
  there's more than a couple of roles.
- **DRF**: `permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]` — a
  custom `BasePermission.has_object_permission` is where the per-object check
  belongs for API views; `has_permission` alone only gates the endpoint, not
  the specific object.

## 3. CSRF — what `{% csrf_token %}` is actually defending against
Django's CSRF protection requires a token (from a cookie, matched against a
hidden form field or header) because browsers automatically attach cookies
(including the session cookie) to cross-site form submissions — without this
check, a malicious page could POST to your app and the browser would
helpfully include the victim's valid session cookie. `{% csrf_token %}` in
every POST form; for an API consumed by JS, `X-CSRFToken` header read from the
`csrftoken` cookie by the JS client. `@csrf_exempt` should be rare and
justified (a webhook endpoint verified by signature instead) — never applied
to make a failing form "just work" without understanding why it failed.

## 4. The settings an audit checks
```python
DEBUG = False                          # never True in production — leaks stack traces, settings, SQL
SECRET_KEY = env("DJANGO_SECRET_KEY")  # never hardcoded, never committed
ALLOWED_HOSTS = ["app.example.com"]    # not ["*"] in production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
X_FRAME_OPTIONS = "DENY"
```
`DEBUG = True` in production is still, after many years of being the textbook
example, a real recurring incident cause — it renders a detailed error page with the traceback and most settings (names containing API, KEY, PASS, SECRET, SIGNATURE or TOKEN are masked) to any visitor who triggers an error. Django's docs say never to deploy with `DEBUG` on. `python manage.py check --deploy` runs Django's own
deployment checklist and flags most of this automatically — run it in CI.

## Verify
- [ ] `AUTH_USER_MODEL` is a custom model set before any migration ran, even if currently identical to `AbstractUser`.
- [ ] Object-level access is checked explicitly (ownership or `django-guardian`), not assumed covered by model-level permissions.
- [ ] No `@csrf_exempt` exists without a replacement verification mechanism (signature, API key) documented next to it.
- [ ] `python manage.py check --deploy` passes with no warnings in CI against production settings.
- [ ] `DEBUG = False` and `SECRET_KEY` sourced from environment, confirmed in the actual deployed settings module, not just the default.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (topics/auth/customizing, topics/auth/default, howto/csrf, ref/settings, ref/django-admin), DRF docs.
Confirmed: `AbstractUser` subclass guidance and "set AUTH_USER_MODEL before the first migrate", four default permissions (add, change, delete, view), "foundation for object permissions but no core implementation", `X-CSRFToken` header and `csrftoken` cookie, `check --deploy`, the DEBUG masking rule, `SECRET_KEY_FALLBACKS`.
Corrected or removed: the claim that the docs say to "always" use a custom user model (they show it as the way to start a new project), and the claim that the debug page shows local variables with secrets (the docs describe masking of sensitive setting names).
Method: documentation only; no commands were run.
