---
id: computing-software.web-development.django-ninja.django-ninja-api-key-bearer-basic-auth
name: django-ninja-api-key-bearer-basic-auth
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, authenticators, api-key, bearer, basic-auth, authentication, django]
level: practitioner
status: docs-checked
description: "Protect Django Ninja operations with API key (query, header, cookie), HTTP Bearer or HTTP Basic authenticators by subclassing ninja.security classes."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: require credentials on an operation with a ready-made `ninja.security` class.

## Core protocol
`auth=` takes any callable of `request`. A truthy return is stored in `request.auth` and the operation runs; a falsy/`None` return gives HTTP 401 `{"detail": "Unauthorized"}` and the operation never runs.

## API key
Subclass `APIKeyQuery`, `APIKeyHeader` or `APIKeyCookie` and implement `authenticate(self, request, key)`. `param_name` names the query param/header/cookie to read; it defaults to `"key"` on all three.

```python
from django.utils.crypto import constant_time_compare
from ninja.security import APIKeyHeader

class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if constant_time_compare(key, "supersecret"):
            return key

@api.get("/headerkey", auth=ApiKey())
def headerkey(request):
    return f"Token = {request.auth}"
```

For a query key, subclass `APIKeyQuery` with `param_name = "api_key"` and return e.g. `CLIENTS.get(key)`. For cookies, subclass `APIKeyCookie`. Note: `APIKeyCookie` (and `django_auth`) also runs a CSRF check by default; pass `csrf=False` to its `__init__` to disable.

## HTTP Bearer
Subclass `HttpBearer`, implement `authenticate(self, request, token)`. Client sends `Authorization: Bearer <token>`.

```python
from ninja.security import HttpBearer

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if constant_time_compare(token, "supersecret"):
            return token

@api.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"token": request.auth}
```

The scheme is matched case-insensitively. A missing header, wrong scheme or missing token counts as unauthenticated, not an error, so later authenticators in a list still run.

## HTTP Basic
Subclass `HttpBasicAuth`, implement `authenticate(self, request, username, password)`; return something truthy (e.g. the username) to accept.

## Gotchas
- Use `constant_time_compare` (from `django.utils.crypto`) for secret comparison, as the page's examples do.
- Instantiate the class: `auth=ApiKey()`, not `auth=ApiKey`.

## Checked

2026-11-07: Confirmed against the Authentication guide: the callable protocol and 401 `{"detail": "Unauthorized"}`, `APIKeyQuery`/`APIKeyHeader`/`APIKeyCookie` with `authenticate(self, request, key)`, `param_name` default `"key"`, the cookie CSRF note with `csrf=False`, `HttpBearer`, `HttpBasicAuth` and the case-insensitive Bearer scheme. Nothing removed.

Method: documentation only; no commands were run.
