---
id: computing-software.web-development.django-ninja.django-ninja-csrf-cookie-auth
name: django-ninja-csrf-cookie-auth
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, csrf, cookie-auth, ensure-csrf-cookie, csrf-exempt, security]
level: practitioner
status: docs-checked
description: "Understand when Django Ninja enforces CSRF (cookie-based auth only), disable it with csrf=False, and serve a CSRF-cookie endpoint with ensure_csrf_cookie."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/csrf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get CSRF protection right with cookie auth in Django Ninja.

## How it works
Every Ninja view is CSRF-exempt at the Django middleware level. CSRF is instead checked at authentication time by any `APIKeyCookie`-based auth class (including `django_auth`, which is `SessionAuth()`):
- No auth, or non-cookie auth (Authorization header, query-string key, `HttpBasicAuth`, `HttpBearer`): nothing to check.
- Cookie auth: the auth class validates the token itself, accepting the `csrfmiddlewaretoken` form field and the `X-CSRFToken` header.

```python
class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return constant_time_compare(key, "test")

api = NinjaAPI(auth=CookieAuth())
```

POST/PUT/PATCH/DELETE on this API now need a valid CSRF token.

## Turning it off for a cookie class
`APIKeyCookie` takes `csrf` (default `True`):

```python
class UnprotectedCookieAuth(APIKeyCookie):
    def __init__(self):
        super().__init__(csrf=False)
```

Warning from the page: only do this if the cookie cannot be used to forge a request from another site; never for `django_auth`/session cookies.

## Endpoint that hands out the CSRF cookie
```python
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf", auth=None)
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```

Rules from the page:
- The route decorator must be above `ensure_csrf_cookie`.
- Also apply `@csrf_exempt`; Ninja reads that flag and skips its cookie-auth CSRF check.
- `ensure_csrf_cookie` needs a real `HttpResponse` (or subclass such as `JsonResponse`), not a returned dict.
- If a cookie-based auth is set globally, pass `auth=None` on this operation or it rejects the request (no CSRF cookie exists yet).

## Frontend and tests
Send the token as `X-CSRFToken` header or `csrfmiddlewaretoken` form field (see Django's CSRF howto). Swagger at `/api/docs` sends it automatically. Cross-origin frontends need CORS set up separately (e.g. django-cors-headers); Ninja has no CORS handling. Ninja's `TestClient` skips CSRF; use Django's own test client to test it.

## Checked

2026-11-07: Confirmed against guide/csrf.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
