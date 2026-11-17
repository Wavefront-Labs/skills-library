---
id: computing-software.web-development.django-ninja.django-ninja-permission-and-async-decorators
name: django-ninja-permission-and-async-decorators
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, decorators, permissions, async-decorators, require-perm, operation-mode]
level: advanced
status: docs-checked
description: "Write a reusable Django Ninja permission decorator, handle request.auth timing, and make one decorator work on both sync and async operations."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/decorators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: reusable permission checks and decorators that survive async endpoints.

## Permission decorator
Placed below `@api.<method>`, a decorator wraps the endpoint itself (OPERATION mode), so it runs after auth and validation and `request.auth` is set.

```python
from functools import wraps
from ninja.errors import HttpError

def require_perm(perm: str):
    def decorator(func):
        @wraps(func)  # keeps the signature so Ninja still parses parameters
        def wrapper(request, *args, **kwargs):
            if not request.auth.has_perm(perm):
                raise HttpError(403, "Permission denied")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

@api.delete("/posts/{post_id}", auth=django_auth)
@require_perm("blog.delete_post")
def delete_post(request, post_id: int):
    return {"deleted": post_id}
```

For a whole router: `router = Router(auth=django_auth); router.add_decorator(require_perm("blog.view_post"))`. With a custom authenticator returning a token/API-key object, check that object's fields instead.

## request.auth timing
`@decorate_view` and `add_decorator(..., mode="view")` run before authentication, so `request.auth` is unavailable there. For per-request setup that needs the user before body validation (e.g. activating a tenant), do it inside `authenticate()`. A VIEW decorator needing the raw body and the user should read `request.body` first, call the view (auth runs inside), then use `getattr(request, "auth", None)` afterwards.

## Sync and async
A sync decorator wrapping an async function gets a coroutine, not the result. Options:

1. Branch at decoration time:
```python
def universal_decorator(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(request, *args, **kwargs):
            result = await func(request, *args, **kwargs)
            if isinstance(result, dict):
                result["decorated"] = True
            return result
        return async_wrapper

    @wraps(func)
    def sync_wrapper(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        if isinstance(result, dict):
            result["decorated"] = True
        return result
    return sync_wrapper
```
2. If every endpoint on the router is `async def`, use a plain `async def` wrapper that awaits `func`.
3. Keep a sync wrapper, call `func`, and if `asyncio.iscoroutine(result)` return an inner `async def` that awaits it; otherwise handle the plain value.

Feature-flag gates can return a `(status, data)` tuple instead of raising, e.g. `return 403, {"error": ...}`.

## Checked

2026-11-08. Confirmed against the django-ninja decorators guide (read in full): OPERATION mode runs after auth and parameter validation, so `request.auth` is set; `@wraps` keeps the signature; the `require_perm` example; `add_decorator` on a router; VIEW-mode decorators run before authentication; do tenant setup in `authenticate()`; the raw-body VIEW decorator pattern with `getattr(request, "auth", None)`; the three sync/async options; the `(status, data)` feature-flag gate.

Method: documentation only; no commands were run.
