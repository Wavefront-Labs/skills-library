---
id: computing-software.web-development.django-ninja.django-ninja-form-data
name: django-ninja-form-data
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, form-data, form, urlencoded, multipart, pydantic]
level: intro
status: docs-checked
description: "Read HTML form fields in Django Ninja with Form, group them in a Schema, validate them, and map empty strings to defaults."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/forms.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Handle form data in Django Ninja

Goal: read `application/x-www-form-urlencoded` or `multipart/form-data` fields (from `request.POST`).

```python
from ninja import NinjaAPI, Form, P

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {"username": username, "password": "*****"}
```

`Form[str]` is the preferred style; the older `username: str = Form(...)` still works and means the same. A default makes it optional: `remember_me: Form[bool] = False`.

## Schema grouping and mixing

```python
@api.post("/items/{item_id}")
def update(request, item_id: int, q: str, item: Form[Item]):
    return {"item_id": item_id, "item": item.dict(), "q": q}
```

`item_id` comes from the path, `q` from the query, `item` from form fields (each schema field read with its own type/default/validation).

## Constraints and aliases
Constraints go in `P(...)`, as for `Query`: `gt ge lt le` for numbers, `min_length max_length pattern` for strings, plus `title description example/examples deprecated include_in_schema`. For example `name: Form[str, P(min_length=1, max_length=100)]` and `quantity: Form[int, P(gt=0)] = 1`. Use `alias` as `Form[str, P(alias="item-name")]`, or Pydantic `Field(alias=...)` inside a Schema.

## Empty strings to defaults
HTML forms often send blank optional fields as `""`, which fails for `int`/`float`/`bool`. Use a wrap validator:

```python
from typing import Annotated, TypeVar
from pydantic import WrapValidator
from pydantic_core import PydanticUseDefault

T = TypeVar("T")

def _empty_str_to_default(v, handler, info):
    if isinstance(v, str) and v == "":
        raise PydanticUseDefault
    return handler(v)

EmptyStrToDefault = Annotated[T, WrapValidator(_empty_str_to_default)]

class Item(Schema):
    price: EmptyStrToDefault[float] = 0.0
    quantity: EmptyStrToDefault[int] = 0
```

Posting `price=""` now falls back to `0.0`.

## With files
`Form` fields plus a `File` parameter make the whole request `multipart/form-data` automatically (see file uploads). Undeclared form fields are ignored.

## Checked

2026-11-07: Confirmed against the Form Data guide: `Form[str]`, optional defaults, `Form[Item]` grouping, path/query mixing, constraints, aliases, the empty-string wrap validator and the multipart note. Corrected: `remember_me: bool = Form(False)` became `Form[bool] = False`; constraint and alias examples now use `P(...)` as on the page; the older `= Form(...)` form is stated as still working.

Method: documentation only; no commands were run.
