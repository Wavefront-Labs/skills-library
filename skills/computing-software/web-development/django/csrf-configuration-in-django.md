---
id: computing-software.web-development.django.csrf-configuration-in-django
name: csrf-configuration-in-django
category: computing-software
field: web-development
product: django
tags: [csrf-trusted-origins, django-csrf, csrfviewmiddleware, x-csrftoken, csrf-failure, django]
level: practitioner
status: verified
description: "Configuring Django CSRF: CSRF_TRUSTED_ORIGINS with schemes, proxies and HTTPS settings, AJAX headers, ensure_csrf_cookie for SPAs, csrf_exempt webhooks and diagnosing 403s."
sources:
  - https://docs.djangoproject.com/en/stable/ref/csrf/
  - https://docs.djangoproject.com/en/stable/howto/csrf/
  - https://docs.djangoproject.com/en/stable/ref/settings/#csrf-trusted-origins
  - https://guides.rubyonrails.org/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSRF configuration in Django

`CsrfViewMiddleware` (on by default) checks unsafe methods: the `Origin` header (Django 4.0+), then for HTTPS the `Referer`, then the token from the form field or header against the `csrftoken` cookie.

## 1. Templates and AJAX
```django
<form method="post">{% csrf_token %}...</form>
```
```js
const token = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/)?.[1];
fetch("/api/items/", { method: "POST", headers: { "X-CSRFToken": token, "Content-Type": "application/json" }, body });
```
SPA served by Django but never rendering `{% csrf_token %}`: decorate the entry view with `@ensure_csrf_cookie` so the cookie exists. If `CSRF_USE_SESSIONS = True`, the token is not in a cookie; render it into the page.

## 2. Trusted origins
```python
CSRF_TRUSTED_ORIGINS = ["https://app.example.com", "https://*.example.com"]   # scheme required since 4.0
```
Needed when the request's `Origin` differs from the host Django sees: separate front-end domain, or a proxy/CDN hostname.

## 3. Behind a proxy (most common 403 cause)
"Origin checking failed - https://example.com does not match any trusted origins" usually means Django thinks the request is HTTP or for another host:
```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")   # only if the proxy sets/overwrites it
USE_X_FORWARDED_HOST = True                                     # if the proxy rewrites Host
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

## 4. Exemptions
`@csrf_exempt` only for machine-to-machine endpoints (payment webhooks) that verify their own signature. DRF: `SessionAuthentication` enforces CSRF for authenticated requests; token/JWT auth classes do not.

## 5. Debugging 403s
- Set `CSRF_FAILURE_VIEW` or read the debug page reason: "CSRF cookie not set", "CSRF token missing", "Origin checking failed", "Referer checking failed - no Referer" (a `Referrer-Policy: no-referrer` on HTTPS breaks the Referer fallback; use `same-origin`).
- Cookie not set across subdomains: `CSRF_COOKIE_DOMAIN = ".example.com"` (and trusted origins).
- Cached pages with embedded tokens serve stale tokens; vary on cookie or exclude forms from caching.
- In tests, `override_settings(CSRF_TRUSTED_ORIGINS=...)` does not affect a test `Client` whose middleware is already loaded (the middleware reads the setting once): create a new `Client` inside the override.
- A project template named `403_csrf.html` is used by the default failure view (it receives no `reason` variable); `CSRF_FAILURE_VIEW` is called as `view(request, reason="")`.

Rails equivalent for comparison: `protect_from_forgery with: :exception` (on by default in new apps via `default_protect_from_forgery`), `csrf_meta_tags`, `skip_forgery_protection` for webhooks (Rails Security guide and `ActionController::RequestForgeryProtection` API page).

## Verify
- [ ] POST from the real front-end origin succeeds; from an untrusted origin returns 403 with "Origin checking failed".

## Checked
Django 6.1.2 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run (test Client with enforce_csrf_checks): POST with no cookie -> 403 `CSRF cookie not set.`; with cookie but no token -> `CSRF token missing.`; `X-CSRFToken` header -> 200; `@ensure_csrf_cookie` view sets `csrftoken`; `@csrf_exempt` -> 200.
- Run: a mismatching `Origin` -> 403 `Origin checking failed - https://evil.example does not match any trusted origins.`; `CSRF_TRUSTED_ORIGINS = ["https://*.example.com"]` accepted `https://app.example.com` (new Client); a scheme-less trusted origin fails system check `4_0.E001`.
- Run: an `https://testserver` Origin was rejected without `SECURE_PROXY_SSL_HEADER` and accepted with it plus `X-Forwarded-Proto: https`; an HTTPS request with no Origin and no Referer -> `Referer checking failed - no Referer.`; same-host Referer -> 200.
- Run: the cookie regex from the JS snippet extracts the token in Node 20; DRF `SessionAuthentication` POST with enforce_csrf_checks -> 403, default APIClient -> 201.
- Fetched: Django 4.0 release notes (Origin header consulted), ref/csrf.txt and the 403 failure view source (the `no-referrer` Referrer-Policy warning, `reason` strings, `403_csrf.html`), settings reference (`CSRF_COOKIE_DOMAIN`, `CSRF_USE_SESSIONS`), Rails security guide.
- Fetched: DRF authentication docs (SessionAuthentication enforces CSRF for authenticated requests).
