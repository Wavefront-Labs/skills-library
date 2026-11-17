---
id: computing-software.web-development.django-ninja.django-ninja-body-multiple-patch
name: django-ninja-body-multiple-patch
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, body, body-multiple, patchdict, patch, singular-body]
level: practitioner
status: docs-checked
description: "Use Body for scalar values, understand embedded keys with multiple body params, and do partial PATCH updates with PatchDict."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/body.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Singular body values, multiple bodies, and PatchDict

## Scalar from the body
A scalar defaults to query. Mark it with `Body`:

```python
from ninja import Body, NinjaAPI

@api.put("/items/{item_id}")
def update_item(request, item_id: int, importance: Body[int]):
    return {"item_id": item_id, "importance": importance}
```

`Body` takes the same arguments as `Query` (`gt/ge/lt/le`, `min_length`, `max_length`, `pattern`, `alias`, `title`, `description`, `example/examples`, `deprecated`, `include_in_schema`, Pydantic `Field` keywords). Annotated forms also work: `Annotated[int, Body(gt=0)]` or `Body[int, P(gt=0)]` with `from ninja import P`.

Gotcha: if `importance` is the only body argument, the request body is the bare value `5`, not `{"importance": 5}` (that gives `422`, "Input should be a valid integer").

## Multiple body parameters
With more than one body-sourced argument (several schemas, or a schema plus a `Body` scalar), each is expected nested under its parameter name (or alias):

```python
@api.post("/items/{item_id}")
def update_item(request, item_id: int, item: Item, user: User):
    ...
```

```json
{
    "item": {"name": "Katana", "price": 299.00},
    "user": {"username": "vitaliy"}
}
```

With a single body parameter there is no wrapping key.

## Partial updates with PatchDict
`PatchDict[Schema]` makes every field optional and gives a plain `dict` with only the fields the client sent:

```python
from ninja import PatchDict

@api.patch("/items/{item_id}")
def patch_item(request, item_id: int, payload: PatchDict[ItemPatch]):
    items_db[item_id].update(payload)
    return {"item_id": item_id, "updated": list(payload.keys())}
```

Fields stay required on other views using the same schema. A body of `{"price": 250.00}` gives `payload == {"price": 250.0}`.

## Checked

2026-11-07: Confirmed against the Request Body guide sections Singular values in the body, Multiple body parameters and Partial updates with `PatchDict`. Corrected: the scalar example now uses the page's `Body[int]` form instead of `int = Body(...)`, which the page does not show.

Method: documentation only; no commands were run.
