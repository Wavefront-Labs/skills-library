---
id: computing-software.web-development.django.view-decorators
name: view-decorators
category: computing-software
field: web-development
product: django
tags: [view-decorators, login-required, require-http-methods, cache-page, django]
level: practitioner
status: verified
description: "Django view decorators: login_required and permission_required, require_POST, cache_page and vary_on_headers, CSRF and never_cache, and use on CBVs."
sources:
  - https://docs.djangoproject.com/en/stable/topics/http/decorators/
  - https://docs.djangoproject.com/en/stable/topics/auth/default/#the-login-required-decorator
  - https://docs.djangoproject.com/en/stable/topics/cache/#the-per-view-cache
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# View decorators

## 1. Access control
```python
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

@login_required                                   # redirects to settings.LOGIN_URL?next=...
def dashboard(request): ...

@permission_required("orders.change_order", raise_exception=True)   # 403 instead of login redirect (run: anonymous and logged-in-without-permission users both got 403)
def edit_order(request, pk): ...

@user_passes_test(lambda u: u.is_staff)
def staff_report(request): ...
```
- Django 5.1+ (5.1 release notes): `LoginRequiredMiddleware` makes login the default; mark public views with `@login_not_required`. Safer than remembering the decorator on every view.
- Decorators check *who*; still check object ownership inside the view (IDOR).

## 2. HTTP methods
```python
from django.views.decorators.http import require_http_methods, require_POST, require_safe
@require_POST
def delete_item(request, pk): ...           # 405 for GET - state changes never on GET
@require_safe                                # GET and HEAD only
def feed(request): ...
```

## 3. Caching and headers
```python
from django.views.decorators.cache import cache_page, never_cache, cache_control
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

@cache_page(60 * 15)                         # caches full response in the cache backend + sets Cache-Control
@vary_on_headers("Accept-Language")
def public_pricing(request): ...

@never_cache                                  # sends Cache-Control: max-age=0, no-cache, no-store, must-revalidate, private (run)
def account(request): ...
```
- `cache_page` keys on URL (+ Vary headers); never use it on views that render per-user content unless you `vary_on_cookie` (which makes the cache nearly per-session).
- `@condition(etag_func=..., last_modified_func=...)` for conditional GETs.

## 4. CSRF
`@csrf_protect` (explicit), `@ensure_csrf_cookie` (SPA bootstrap page that must set the cookie), `@csrf_exempt` only for endpoints authenticated by something else (signed webhooks) - verify the signature.

## 5. Class-based views
```python
from django.utils.decorators import method_decorator
@method_decorator([login_required, never_cache], name="dispatch")
class AccountView(TemplateView): ...
```
Or mixins: `LoginRequiredMixin`, `PermissionRequiredMixin` (must be leftmost in bases).

Order matters: decorators apply bottom-up; put `cache_page` outermost only if auth checks are inside the cache key logic (generally avoid caching authenticated views).

## Verify
- [ ] Every non-public view requires login (or LoginRequiredMiddleware is on); state-changing views reject GET; cached views contain no per-user data.
