---
id: computing-software.web-development.django-ninja.django-ninja-operation-options
name: django-ninja-operation-options
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, operation-options, openapi, tags, summary, operation-id, deprecated, by-alias, exclude-none]
level: practitioner
status: docs-checked
description: "Tune a Django Ninja operation: tags, summary, description, operation_id, deprecated, include_in_schema, openapi_extra and response serialization switches."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/operations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operation options

All of `get/post/put/patch/delete/api_operation` take the same keyword-only options in addition to `path`.

| Option | Default | Effect |
|---|---|---|
| `response` | not set | schema, or `dict[int, schema]` keyed by status code, to validate/serialize the return value |
| `operation_id` | auto (view module + function name) | OpenAPI `operationId`; must be unique across the schema |
| `summary` | function name, title-cased | short name in docs |
| `description` | the docstring | longer text in docs |
| `tags` | inherited from router | grouping in docs |
| `deprecated` | `None` (False) | flags operation deprecated |
| `url_name` | view function name | name for `reverse()` |
| `include_in_schema` | `True` | `False` hides it from schema and docs |
| `openapi_extra` | `None` | extra keys merged into this operation's OpenAPI entry |
| `by_alias`, `exclude_unset`, `exclude_defaults`, `exclude_none` | `None` (False) | response serialization switches |

`auth` and `throttle` override the API/router defaults for one operation.

## Examples

```python
@api.post("/orders/", tags=["orders"], summary="Say Hello",
          description="Creates an order and updates stock")
def create_order(request, order: str):
    return {"success": True}

@api.post("/tasks", operation_id="create_task")
def new_task(request): ...

@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str): ...

@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request): pass
```

A docstring works as a multi-line description and renders simple Markdown.

Tags can also be set on `Router(tags=["events"])` or `api.add_router("/events/", router, tags=["events"])`; an operation's own `tags` wins.

## Extra OpenAPI content

```python
@api.post(
    "/tasks",
    openapi_extra={
        "responses": {
            400: {"description": "Error Response"},
            404: {"description": "Not Found Response"},
        },
    },
)
def some_operation_2(request): pass
```
`openapi_extra` can likewise carry a `requestBody` description for a body not backed by a schema.

## Serialization switches

```python
class UserOut(Schema):
    name: str = Field(alias="userName")
    nickname: str | None = None

@api.get("/users/{user_id}", response=UserOut, by_alias=True, exclude_none=True)
def get_user(request, user_id: int):
    return UserOut(userName="John", nickname=None)
```
The response is keyed by `userName` and `nickname` is dropped. These map onto Pydantic `model_dump()`; they shape output only, not validation. They can also be set once on `Router(...)` unless an operation overrides them.

To change `operationId` for the whole API, override `get_openapi_operation_id` on a `NinjaAPI` subclass.

## Checked

2026-11-07: Confirmed against the Operations guide options table and examples: defaults for each option, title-cased summary, module-plus-function `operationId`, docstring description and the `auth`/`throttle` override. Corrected: `response` is described as `dict[int, schema]` keyed by status code, as in the table.

Method: documentation only; no commands were run.
