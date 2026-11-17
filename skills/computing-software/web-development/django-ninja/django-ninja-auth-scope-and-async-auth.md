---
id: computing-software.web-development.django-ninja.django-ninja-auth-scope-and-async-auth
name: django-ninja-auth-scope-and-async-auth
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, auth-scope, authentication, async-auth, router-auth, exception-handler]
level: practitioner
status: docs-checked
description: "Set Django Ninja auth on the API, a router or one operation, opt out with auth=None, raise handled exceptions from authenticate(), and write async authenticators."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control where auth applies, and handle errors and async in authenticators.

## Scope: API, router, operation
The most specific setting wins: operation `auth=` over router over `NinjaAPI(auth=...)`.

```python
api = NinjaAPI(auth=django_auth)  # default for every operation
router = Router()

@router.get("/public")             # inherits django_auth
def public(request): ...

@router.get("/open", auth=None)    # explicitly no auth
def open_endpoint(request): ...

api.add_router("/items/", router)
```

A router may set its own default, which overrides API-level auth for its operations:

```python
router = Router(auth=AuthBearer())
# or
api.add_router("/events/", events_router, auth=AuthBearer())
```

`auth=None` (on an operation, router or `add_router`) is the only way to turn auth off for part of an API that sets it globally.

## Exceptions inside authenticate()
An exception raised in `authenticate()` is handled like one raised in the operation, so a registered handler builds the response:

```python
class InvalidToken(Exception):
    pass

@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if constant_time_compare(token, "supersecret"):
            return token
        raise InvalidToken
```

## Async authenticators
Ninja detects `async def authenticate` (or an async function passed to `auth=`) and awaits it whether the operation is sync or async.

```python
async def async_auth(request):
    return constant_time_compare(request.headers.get("X-Token", ""), "supersecret")

@api.get("/pets", auth=async_auth)
async def pets(request):
    return {"user": request.auth}
```

```python
class AsyncBearer(HttpBearer):
    async def authenticate(self, request, token):
        return token if constant_time_compare(token, "supersecret") else None
```

## Interactive docs
The `auth=` in use is added to the OpenAPI schema as a security requirement, so `/api/docs` shows an Authorize button.

## Checked

2026-11-07: Confirmed against the Authentication guide sections Applying auth at different levels, Raising exceptions from `authenticate()`, Async authentication and Interactive docs. Nothing removed.

Method: documentation only; no commands were run.
