---
id: computing-software.web-development.django-ninja.django-ninja-routers-nesting
name: django-ninja-routers-nesting
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, routers, add-router, nested-routers, url-name-prefix, tags]
level: practitioner
status: docs-checked
description: "Split a Django Ninja API into per-app Routers, mount them by object or import path, nest them, inherit auth/throttle/tags, mount one twice."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: organise operations into modules (typically one `Router` per Django app) under one `NinjaAPI`.

## Define and mount
```python
# events/api.py
from ninja import Router
router = Router()

@router.get("/")
def list_events(request): ...
```

```python
# project api.py
api = NinjaAPI()
api.add_router("/events/", events_router)      # by object
api.add_router("/news/", "news.api.router")    # or by Python import path
```
A dotted string avoids importing the app's api module (and its models) at the top, which helps with circular imports. `Router` supports `.get/.post/.put/.patch/.delete/.api_operation` like `NinjaAPI`.

## Constructor options (keyword-only, all defaults operations can override)
`auth`, `throttle`, `tags`, `by_alias`, `exclude_unset`, `exclude_defaults`, `exclude_none`.

Auth priority for an operation: its own `auth=`, then `add_router(..., auth=)`, then the Router's `auth`, then a parent router's, finally `NinjaAPI(auth=...)`. Throttle follows the same order.

## Tags
Tags passed to `add_router()` replace the router's own tags for that mount. Tags set on the Router accumulate with a parent router's when nested. An operation's own `tags=` wins over both.

## Nested routers
Call `add_router()` on a router instead of the api:

```python
second_router.add_router("l3", third_router)
first_router.add_router("l2", second_router)
api.add_router("l1", first_router)
# -> /api/l1/add, /api/l1/l2/add, /api/l1/l2/l3/add
```
`auth`, `throttle` and `tags` on a parent flow down unless a child or operation overrides them.

Parent prefix path params are available in the nested router via `Path`:

```python
@router.get("/multiply/{c}")
def multiply(request, c: int, a: Path[int], b: Path[int]):
    return {"result": (a + b) * c}

api.add_router("add/{a}/{b}", router)
```

## Mounting the same router twice
Raises `ConfigError` unless each extra mount has a unique `url_name_prefix`:

```python
api.add_router("/v1/things/", things_router)
api.add_router("/v2/things/", things_router, url_name_prefix="things_v2")
```

## Other
- `RouterPaginated` (from `ninja.pagination`) auto-paginates operations whose `response` is a collection.
- `NinjaAPI(default_router=...)` sets the router that `@api.get()` registers on.
- Routers freeze when `api.urls` is first accessed; adding operations or routers afterwards raises `ConfigError`.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/routers.md from GitHub. Confirmed against the whole page: add_router by object or dotted path, constructor options, auth and tag priority, nested routers and the generated paths, url_name_prefix and ConfigError, RouterPaginated, default_router and router freezing. Changed: the nested path parameter example now uses the documented Path[int] annotation instead of Path(...) defaults.

Method: documentation only; no commands were run.
