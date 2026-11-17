---
id: computing-software.web-development.django.custom-error-views-and-error-reporting
name: custom-error-views-and-error-reporting
category: computing-software
field: web-development
product: django
tags: [handler404, handler500, django-error-reporting, error-pages, django]
level: practitioner
status: verified
description: "Custom 404, 403, 400 and 500 pages in Django: templates vs handler views, testing with DEBUG off, ADMINS email reports, Sentry, filtering sensitive data and CSRF failure views."
sources:
  - https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views
  - https://docs.djangoproject.com/en/stable/howto/error-reporting/
  - https://docs.sentry.io/platforms/python/integrations/django/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom error views and error reporting

## 1. Templates (simplest)
Put `404.html`, `500.html`, `403.html`, `400.html` in a template directory. Django's default handlers render them when `DEBUG = False`.
- `500.html` is rendered with **no context** (no request, no context processors) because the failure may come from them: keep it static, inline critical CSS, no `{% url %}` calls that could fail.
- `404.html` receives `request_path` and `exception`; context processors run.

## 2. Handler views
```python
# urls.py (root URLconf only)
handler404 = "core.views.not_found"
handler500 = "core.views.server_error"

# core/views.py
def not_found(request, exception):
    return render(request, "errors/404.html", {"path": request.path}, status=404)
def server_error(request):
    return render(request, "errors/500.html", status=500)
```
Return the right status code - a 200 "not found" page is a soft 404 for search engines. APIs: return JSON when `request.path.startswith("/api/")` or `Accept` prefers JSON.

## 3. CSRF failures
`CSRF_FAILURE_VIEW = "core.views.csrf_failure"` renders a friendly 403 explaining session expiry instead of the technical default. The view signature is `def csrf_failure(request, reason="")`. Without a custom view, a template named `403_csrf.html` is used automatically (it gets only the request context, no `reason`).

## 4. Testing error pages
`DEBUG=True` shows the technical page. Test with `DEBUG=False` and `ALLOWED_HOSTS` set, or unit test:
```python
@override_settings(DEBUG=False)
def test_404(client): assert client.get("/nope/").status_code == 404
```
Add a staff-only `/__raise__/` view in staging to verify 500 handling and reporting end to end.

## 5. Error reporting
- Built-in: with `DEBUG=False`, unhandled exceptions email `ADMINS` via the `mail_admins` logging handler; broken links email `MANAGERS` with `BrokenLinkEmailsMiddleware`. Fine for tiny sites; noisy otherwise.
- Sentry: `sentry_sdk.init(dsn=..., integrations=[DjangoIntegration()], traces_sample_rate=0.1, send_default_pii=False, environment="production", release=GIT_SHA)`.
- Scrub secrets: decorate sensitive views with `@sensitive_post_parameters("password", "card")` and functions with `@sensitive_variables(...)` so tracebacks and reports hide them.

## Verify
- [ ] 404/500 render branded pages with correct status codes when DEBUG is off; staging test exception reaches Sentry with release tag; no passwords in reported POST data.

## Checked
Django 6.1.2 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: with no handlers, `404.html` rendered `request_path`, `exception` (Resolver404) and the `user` context-processor variable; `500.html` rendered with no `user` and no `request` (empty context), as the skill says.
- Run: `handler404` / `handler500` module-level strings in the root URLconf were used (custom views returned 404 and 500 with the right status); `raise Http404("No such order")` -> the handler.
- Run: unhandled exception with DEBUG off emailed ADMINS via `mail_admins` (locmem) and logged an ERROR with traceback; a 404 with an internal Referer emailed MANAGERS via `BrokenLinkEmailsMiddleware`.
- Run: `CSRF_FAILURE_VIEW` custom view received `reason`; `403_csrf.html` was picked up by the default view.
- Run: `sentry_sdk.init(dsn="", integrations=[DjangoIntegration()], traces_sample_rate=0.1, send_default_pii=False, environment=..., release=...)` accepted with sentry-sdk 2.72.0; `sensitive_post_parameters` and `sensitive_variables` import from `django.views.decorators.debug`.
