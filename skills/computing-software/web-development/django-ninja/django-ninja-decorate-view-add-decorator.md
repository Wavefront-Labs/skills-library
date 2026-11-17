---
id: computing-software.web-development.django-ninja.django-ninja-decorate-view-add-decorator
name: django-ninja-decorate-view-add-decorator
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, decorators, decorate-view, add-decorator, view-mode, operation-mode]
level: advanced
status: docs-checked
description: "Wrap Django Ninja operations with decorate_view or router/API add_decorator in VIEW or OPERATION mode, and know the resulting execution order."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/decorators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: apply Django or custom decorators to one operation, a router, or a whole API.

## VIEW vs OPERATION
| Mode | Wraps | Runs | Receives | Returns |
|---|---|---|---|---|
| `"view"` | Ninja's whole request handler | before auth, throttling, param parsing | raw `HttpRequest` + URL kwargs | `HttpResponse` |
| `"operation"` (default) | your endpoint function | after parsing/validation and auth/throttle | validated args | raw return value (dict, Schema, `(status, data)`) |

VIEW suits caching, headers, reusing `cache_page`/`vary_on_headers`. OPERATION suits typed data or the pre-serialization return value.

## Per operation: decorate_view (always VIEW mode)
```python
from django.views.decorators.cache import cache_page
from ninja.decorators import decorate_view

@api.get("/cached")
@decorate_view(cache_page(60 * 15))
def cached_endpoint(request):
    return {"data": "this response is cached for 15 minutes"}
```
It may sit above or below `@api.get`. With several decorators, the last argument ends up outermost: `@decorate_view(cache_page(300), vary_on_headers("User-Agent"))` makes `vary_on_headers` run first.

## Router or API wide: add_decorator
```python
router.add_decorator(decorator, mode="operation")   # or mode="view"
api.add_decorator(decorator, mode="operation")
```
`mode` defaults to `"operation"`; an invalid value raises `ValueError`. Call it multiple times to stack, before or after `add_router()`. It must happen before URLs are generated, otherwise `ConfigError`.

```python
def cors_headers(func):
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    return wrapper

api.add_decorator(cors_headers, mode="view")
```

## Execution order
Applied API-level first, then parents, then children, so the most specific router is outermost (child, parent, api in the page's example). Full request path:
1. most specific router VIEW decorators, 2. parents', 3. API VIEW, 4. operation `@decorate_view`, 5. Ninja auth + throttling, 6. parse/validate, 7-9. OPERATION decorators (child, parent, API), 10. endpoint, 11. serialize.

## Tips
- Always use `functools.wraps`; without it an OPERATION decorator swallowing `**kwargs` yields a `TypeError` hinting "Did you fail to use functools.wraps() in a decorator?".
- Mounting a router twice clones operations, so decorators never stack or leak between mounts.

## Checked

2026-11-07: Confirmed against guide/decorators.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
