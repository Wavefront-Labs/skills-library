---
id: computing-software.web-development.django-ninja.django-ninja-async-orm
name: django-ninja-async-orm
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, async, asgi, orm, sync-to-async, uvicorn]
level: practitioner
status: docs-checked
description: "Write async def Django Ninja operations, serve them under ASGI, and call the Django ORM safely with a-prefixed methods or sync_to_async."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/async.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use async operations for IO-bound work without breaking the ORM.

## Async operation
Add `async` and use async-aware libraries:
```python
@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```
Sync and async operations can coexist in one `NinjaAPI`/`Router`. If a GET and POST share a path and only one is `async def`, the sync one is transparently wrapped.

## Serve with ASGI
```
pip install uvicorn
uvicorn your_project.asgi:application --reload
```
Replace `your_project` with the package containing `asgi.py`; no `--reload` in production. `manage.py runserver` can run async views but not every async library behaves; prefer Uvicorn or Daphne. The page shows 100 concurrent 3-second requests finishing in about 3 s via `ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"`.

## ORM is async-unsafe
Calling `Blog.objects.get(pk=post_id)` directly inside `async def` raises an error.

Django 4.1+: use `a`-prefixed methods (`aget`, `acreate`, `aupdate`, `adelete`, `aget_or_create`, ...):
```python
blog = await Blog.objects.aget(pk=post_id)
```
Iterate with `async for`:
```python
return [blog async for blog in Blog.objects.values()]
```

## sync_to_async fallback
For things without an async counterpart (`from asgiref.sync import sync_to_async`):
```python
@sync_to_async
def get_blog(post_id):
    return Blog.objects.get(pk=post_id)

blog = await get_blog(post_id)
# or inline
blog = await sync_to_async(Blog.objects.get)(pk=post_id)
```

Gotcha, querysets are lazy: `await sync_to_async(Blog.objects.all)()` still fails later when iterated. Evaluate inside the wrapper:
```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
```

## Elsewhere
Async `authenticate()` is supported; built-in pagination works with async operations (custom paginators can subclass `AsyncPaginationBase`); `ninja.testing.TestAsyncClient` tests async operations.

## Checked

2026-11-07: Confirmed against the Async Support guide: the async operation, ASGI serving with Uvicorn/Daphne, the `ab` example, async-unsafe ORM, `a`-prefixed methods (Django 4.1+), `sync_to_async` and the lazy queryset warning, and the notes on async auth, pagination and `TestAsyncClient`. Nothing removed.

Method: documentation only; no commands were run.
