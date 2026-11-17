---
id: computing-software.web-development.django-ninja.django-ninja-session-function-multiple-auth
name: django-ninja-session-function-multiple-auth
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, authenticators, session-auth, django-auth, multiple-auth, authentication]
level: practitioner
status: docs-checked
description: "Use Django Ninja django_auth session instances, a plain function as auth, or a list of authenticators tried in order, plus request.auth checks."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick session auth, a one-off function, or several schemes at once.

## Django session auth
`ninja.security` ships three instances built on Django's session framework (they read the cookie named by `settings.SESSION_COOKIE_NAME` and check `request.user`):

| Instance | Grants access to |
|---|---|
| `django_auth` | any authenticated user |
| `django_auth_superuser` | superusers only |
| `django_auth_is_staff` | superusers and staff members |

```python
from ninja.security import django_auth_superuser

@api.get("/admin-only", auth=django_auth_superuser)
def admin_view(request):
    return {"message": f"Hello superuser {request.auth}"}
```

Backing classes are `SessionAuth`, `SessionAuthSuperUser`, `SessionAuthIsStaff`; subclass one to add checks.

## Plain function auth
No subclassing needed:

```python
def ip_whitelist(request):
    if request.META.get("REMOTE_ADDR") == "8.8.8.8":
        return "8.8.8.8"

@api.get("/ipwhitelist", auth=ip_whitelist)
def ipwhitelist(request):
    return f"Authenticated client, IP = {request.auth}"
```

## Multiple authenticators
Pass a list. They are tried in order; first truthy result wins, otherwise the request is rejected.

```python
class AuthCheck:
    def authenticate(self, request, key):
        if constant_time_compare(key, "supersecret"):
            return key

class QueryKey(AuthCheck, APIKeyQuery):
    pass

class HeaderKey(AuthCheck, APIKeyHeader):
    pass

@api.get("/multiple", auth=[QueryKey(), HeaderKey()])
def multiple(request):
    return f"Token = {request.auth}"
```

## Authorization
Authentication says who; permission is your own condition on `request.auth` (a `User` for `django_auth`):

```python
@api.get("/admin")
def admin_view(request):
    if not request.auth.is_staff:
        return api.create_response(request, {"detail": "Forbidden"}, status=403)
    return {"message": "Welcome!"}
```

The page points to `raise HttpError(403, ...)` / `AuthorizationError` as the exception-based alternative.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/authentication.md from GitHub. Confirmed against the whole page: session auth instances and backing classes, function-based auth, multiple authenticators, and the authorization note. Nothing removed.

Method: documentation only; no commands were run.
