---
id: computing-software.web-development.django-ninja.django-ninja-http-operations
name: django-ninja-http-operations
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, http-operations, operations, get, post, put, patch, delete, api-operation, async]
level: intro
status: docs-checked
description: "Declare Django Ninja operations with the HTTP method decorators, handle several methods or HEAD/OPTIONS via api_operation, and mix sync and async views."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/operations.md
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declare operations for each HTTP method

An operation is a Python function bound to a path and one or more HTTP methods. The same decorators exist on `NinjaAPI` and on `Router`.

## One decorator per method

```python
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/hello")
def get_hello(request):
    return {"message": "hello"}


@api.post("/hello")
def post_hello(request):
    return {"message": "hello"}


@api.put("/hello/{id}")
def put_hello(request, id: int):
    return {"message": "hello"}


@api.patch("/hello/{id}")
def patch_hello(request, id: int):
    return {"message": "hello"}


@api.delete("/hello/{id}")
def delete_hello(request, id: int):
    return {"message": "hello"}
```

## Several methods in one function

```python
@api.api_operation(["POST", "PATCH"], "/tasks/{task_id}")
def upsert_task(request, task_id: int):
    return {"task_id": task_id}
```

`api_operation` is also how to serve methods without a shortcut decorator:

```python
@api.api_operation(["HEAD", "OPTIONS"], "/tasks")
def tasks_meta(request):
    return {}
```

## Sync or async

Use `def` or `async def`; Django Ninja detects which and calls the view accordingly. Both kinds can be mixed on one API or router.

```python
@api.get("/hello")
async def hello(request):
    return {"message": "hello"}
```
Running under ASGI and calling async code from views is covered on the Async Support page.

## Notes

- Every decorator takes the same keyword-only options (`response`, `summary`, `tags`, `auth`, `throttle`, `operation_id`, `url_name`, ...); see the operation-options skill.
- Registering on `api` stores the operation on `api.default_router`.

## Checked

2026-11-07: Confirmed against the Operations guide (decorators, `api_operation`, path parameters, HEAD/OPTIONS handling). Added the NinjaAPI Instance guide as a source for the `api.default_router` note, after reading it. Nothing removed.

Method: documentation only; no commands were run.
