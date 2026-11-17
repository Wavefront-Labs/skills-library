---
id: computing-software.web-development.django-ninja.django-ninja-request-body-schema
name: django-ninja-request-body-schema
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, body, body-schema, schema, post, pydantic]
level: intro
status: docs-checked
description: "Declare a Django Ninja JSON request body with a Schema, handle optional fields and 422 errors, and mix body with path and query params."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/body.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Declare a request body with a Schema

Goal: accept and validate a JSON payload for POST/PUT/PATCH.

```python
from ninja import NinjaAPI, Schema

class Item(Schema):
    name: str
    description: str | None = None
    price: float
    quantity: int

@api.post("/items")
def create_item(request, item: Item):
    return item
```

A `Schema` argument is recognised as the body automatically. Django Ninja parses the JSON, coerces and validates it, hands you an `Item` instance, and adds its JSON Schema to the OpenAPI docs. The default parser reads the body as JSON regardless of `Content-Type`; for other formats see request parsers.

## Optional vs required
Fields with a default are optional. A missing required field gives `422`, e.g. `"type": "missing"`, `"loc": ["body", "item", "quantity"]`, `"msg": "Field required"`. Note the argument name appears in the error path even with a single body parameter.

## Where each argument comes from

- Name that appears as a `{placeholder}`: path.
- `Schema` subclass or a collection such as `list[...]`: body.
- Any other singular type (`int`, `str`, `float`, `bool`, `UUID`): query.

```python
@api.put("/items/{item_id}")
def update_item(request, item_id: int, item: Item, q: str | None = None):
    return {"item_id": item_id, "item": item.dict(), "q": q}
```

## Lists

```python
@api.post("/items/bulk")
def create_items(request, items: list[Item]):
    return {"count": len(items)}
```

The body is a JSON array. Unlike `int`/`str`, a plain `list[...]` defaults to body, not query; use `Query` for a query list. `Body` accepts `min_length` and `max_length` (passed in `P(...)`), so you can constrain a list body directly:

```python
from ninja import Body, P

@api.post("/tags")
def create_tags(request, tags: Body[list[str], P(min_length=1)]):
    return {"tags": tags}
```

## Checked

2026-11-08: Read django-ninja docs/docs/guide/body.md from GitHub. Confirmed against the whole page: Schema body detection, JSON parsing regardless of Content-Type, optional fields, the missing field 422 error and loc, argument source rules, and list bodies. Changed: the list constraint example now uses the documented Body[list[str], P(min_length=1)] form.

Method: documentation only; no commands were run.
