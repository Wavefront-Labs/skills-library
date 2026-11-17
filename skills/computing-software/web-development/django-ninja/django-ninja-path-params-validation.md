---
id: computing-software.web-development.django-ninja.django-ninja-path-params-validation
name: django-ninja-path-params-validation
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, path-params, path-validation, pydantic, router-prefix, schema]
level: practitioner
status: docs-checked
description: "Constrain Django Ninja path parameters with Path(), group them in a Schema with Path[...], and read placeholders from a router prefix."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/path-params.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Validating and grouping Django Ninja path parameters

Goal: add ranges/patterns to path params, validate them as a group, or read them from a Router prefix.

## Constraints with `Path`

```python
from ninja import NinjaAPI, P, Path

@api.get("/items/{item_id}")
def read_item(request, item_id: Path[int, P(gt=0, le=1000)]):
    return {"item_id": item_id}
```

`Path[...]` takes its options in `P(...)`, the same options as `Query`: `alias`, `title`, `description`, `gt`/`ge`/`lt`/`le`, `min_length`, `max_length`, `pattern`, `example`, `examples`, `deprecated`, `include_in_schema`, plus any keyword Pydantic's `Field` understands.

## Group in a Schema
Annotate a `Schema` argument with `Path[...]`:

```python
import datetime
from ninja import NinjaAPI, Path, Schema

class EventDate(Schema):
    year: int
    month: int
    day: int

    def value(self) -> datetime.date:
        return datetime.date(self.year, self.month, self.day)

@api.get("/events/{year}/{month}/{day}")
def events(request, date: Path[EventDate]):
    return {"date": date.value()}
```

- Every schema field must correspond to a `{placeholder}` in the path; Django Ninja warns at startup if a placeholder has no matching field.
- Nested schemas work like nested query parameters, as long as every leaf field maps to a name in the path.

## Placeholders from a router prefix
A Router mounted under a prefix with placeholders can read them with `Path[...]`:

```python
router = Router()

@router.get("/multiply/{c}")
def multiply(request, c: int, a: Path[int], b: Path[int]):
    return {"result": (a + b) * c}

api.add_router("add/{a}/{b}", router)
```

`a` and `b` come from the mount prefix `add/{a}/{b}`, not from the operation's own path.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/path-params.md from GitHub. Confirmed against the whole page: Path options, grouping parameters in a Schema, the startup warning for missing fields, nested path schemas and router prefix placeholders. Changed: examples now use the documented Path[int, P(...)] and Path[int] forms instead of Path(...) defaults.

Method: documentation only; no commands were run.
