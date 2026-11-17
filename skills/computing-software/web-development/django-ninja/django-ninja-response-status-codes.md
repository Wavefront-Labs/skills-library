---
id: computing-software.web-development.django-ninja.django-ninja-response-status-codes
name: django-ninja-response-status-codes
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, response-codes, status, codes-4xx, empty-response, httpresponse, queryset]
level: practitioner
status: docs-checked
description: "Declare Django Ninja response schemas per status code with Status(), code ranges, Ellipsis fallback, empty 204 bodies, querysets, raw HttpResponse."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/responses.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responses: schemas per status code

Goal: control what an operation may return.

- No `response=`: the return value goes to the renderer with no validation.
- `response=UserOut`: validates and keeps only declared fields (extra attributes like `password` are dropped).
- `response=list[UserOut]` for lists.
- Returning a queryset needs no `.all()`/`list()`; validation evaluates it.

## Async

That shortcut runs the query synchronously, which Django forbids in `async def`. Evaluate first:

```python
return await sync_to_async(list)(Task.objects.all())
```

## Multiple schemas

```python
from ninja import NinjaAPI, Schema, Status

@api.post("/login", response={200: Token, 401: Message, 402: Message})
def login(request, username: str, password: str):
    if username != "admin":
        return Status(401, {"message": "Unauthorized"})
    return Status(200, {"token": "xyz", "expires": datetime.now()})
```

`Status(code, value)` picks the schema and sets the HTTP status. Returning a tuple `return 401, {...}` is deprecated (DeprecationWarning). If `response` names only one code and it is not 200, e.g. `{201: TaskOut}`, it is used automatically. A returned code that is not declared (and no `...`) raises `ConfigError`.

## Ranges and fallback

```python
from ninja.responses import codes_4xx
@api.post("/login", response={200: Token, codes_4xx: Message})
```

Built-ins: `codes_1xx` (100-101), `codes_2xx` (200-206), `codes_3xx` (300-308), `codes_4xx` (400-412, 416, 418, 425, 429, 451), `codes_5xx` (500-504). Or your own `frozenset({410, 429})`. `...` matches any unlisted code; it is excluded from the OpenAPI schema and docs.

## Empty body

```python
@api.post("/tasks/{task_id}", response={204: None})
def delete_task(request, task_id: int):
    return Status(204, None)
```

## Raw Django response

Returning an `HttpResponse` (or subclass, e.g. `redirect(...)`) passes through untouched, with no validation.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/responses.md from GitHub. Confirmed against the whole page: response schemas, list and queryset returns, the async warning, Status, the deprecated tuple return, single-code shortcut, ConfigError, code ranges with their numbers, Ellipsis fallback, empty 204 body and raw HttpResponse. Nothing removed.

Method: documentation only; no commands were run.
