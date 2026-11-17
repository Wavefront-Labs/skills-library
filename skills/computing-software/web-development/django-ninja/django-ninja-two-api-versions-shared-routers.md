---
id: computing-software.web-development.django-ninja.django-ninja-two-api-versions-shared-routers
name: django-ninja-two-api-versions-shared-routers
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, versioning, ninjaapi, add-router, url-namespace, reverse, api-v2]
level: advanced
status: docs-checked
description: "Run a breaking v2 of a Django Ninja API beside v1: split routers, mount shared ones on two NinjaAPI instances, keep URL namespaces unique."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-8.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: ship a breaking response change as version 2 while version 1 keeps working unchanged.

## 1. Isolate what differs in its own router

A router is mounted as a unit, so operations that differ between versions must sit in their own router. Keep shared ones (e.g. `signup`) on `router` and move the changing ones to `tokens`, marked deprecated:

```python
router = Router(tags=["auth"], auth=None)  # shared by v1 and v2
tokens = Router(tags=["auth"], auth=None)  # v1 only

@tokens.post("/token", response=TokenOut, deprecated=True)
def obtain_token(request, payload: TokenIn):
    """Use `POST /api/v2/auth/token` instead."""
    ...
```

## 2. Write the v2 router

When only the shape changes, v2 calls the v1 view functions (an operation decorator returns the function unchanged) and reshapes the result:

```python
from . import api as v1
tokens = Router(tags=["auth"], auth=None)

@tokens.post("/token", response=OAuthTokenOut)
def obtain_token(request, payload: TokenIn):
    return oauth_response(v1.obtain_token(request, payload))
```

An `HttpError` raised in a v1 view propagates and becomes the same response from v2.

## 3. Mount both on two NinjaAPI instances

```python
api = NinjaAPI(title="TaskFlow API", version="1.0", description=DESCRIPTION, auth=JWTAuth())
api.add_router("/auth", "accounts.api.router")
api.add_router("/auth", "accounts.api.tokens")
api.add_router("/projects", "projects.api.router")

api_v2 = NinjaAPI(title="TaskFlow API", version="2.0", description=..., auth=JWTAuth())
api_v2.add_router("/auth", "accounts.api.router")
api_v2.add_router("/auth", "accounts.api_v2.tokens")
api_v2.add_router("/projects", "projects.api.router")
```

```python
# urls.py - v2 first, v1 keeps /api/
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v2/", api_v2.urls),
    path("api/", api.urls),
]
```

- Each mount gets its own copy of the router's operations bound to that API, so a fix in a shared router reaches both versions.
- Two routers at the same prefix are fine if their paths do not overlap.
- Endpoints registered on `api` only (like `/health`) do not exist on v2.
- Mounting the **same router twice on one API** raises `ConfigError: Router is already mounted to this API...`; pass a unique `url_name_prefix="..."` to the second `add_router()` if you really need that.
- Tokens from either version work on both when both use the same `JWTAuth`.

## 4. Namespaces

Each `NinjaAPI` registers under namespace `api-<version>`, so `reverse('api-1.0:obtain_token')` is `/api/auth/token` and `reverse('api-2.0:obtain_token')` is `/api/v2/auth/token`.

Two APIs with the same version (default `"1.0.0"`) share a namespace; `manage.py check` warns `urls.W005 ... isn't unique`, and `reverse()` may return a URL from the wrong API. Give distinct `version` values or `urls_namespace=`.

## 5. Test each version

`TestClient` takes any `NinjaAPI`: `client_v2 = TestClient(api_v2)`; paths are relative to that API (`/auth/token`).

## Checked

2026-11-08: Read django-ninja docs/docs/tutorial/part-8.md from GitHub. Confirmed against the versioning sections of the page (from the second version through the testing both versions section; the title and OpenAPI polish sections before it were not needed for these claims): router split, v2 router calling v1 views, two NinjaAPI mounts, urls.py order, ConfigError text, namespaces api-<version>, the urls.W005 warning and TestClient per version. Nothing removed.

Method: documentation only; no commands were run.
