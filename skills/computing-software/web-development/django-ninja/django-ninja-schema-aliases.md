---
id: computing-software.web-development.django-ninja.django-ninja-schema-aliases
name: django-ninja-schema-aliases
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, schema-aliases, alias, dotted-path, choices, pydantic]
level: practitioner
status: docs-checked
description: "Read Django Ninja schema fields from dotted paths, call methods automatically, and expose get_FOO_display() using Field(alias=...)."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/schemas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema aliases: dotted paths and callables

Goal: populate a schema field from somewhere other than the same-named attribute or key.

By default a field is read from the attribute (or dict key) with the same name. `ninja.Field(..., alias=...)` extends Pydantic's alias to follow **dotted paths** and to **call** attributes that are callable.

```python
from ninja import Field, Schema

class TaskSchema(Schema):
    id: int
    # first Field() argument is the default; use ... for required
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
    owner_title: str = Field(None, alias="owner.get_title")  # called automatically
```

`TaskSchema.from_orm(task).dict()` then gives `{"id": 1, "completed": True, "owner_first_name": "Sam", "owner_title": "owner"}` for the sample objects in the docs.

## Indexes

Dotted aliases use Django's template variable lookup, so they also traverse dict keys and list/tuple indexes, e.g. `alias="message_set.0.text"`.

## Choices display value

Django generates `get_<field>_display()` for fields with `choices=`. Alias straight to it, no resolver needed:

```python
class TaskSchema(Schema):
    type: str
    type_display: str = Field(None, alias="get_type_display")
```

## Gotcha: plain dict input

Dotted-path resolution only applies when the source is **not** a `dict`. A dict source is only looked up by its exact top-level key, so when validating from a dict (most request bodies) use a plain non-dotted `alias`.

For computed values that an alias cannot express, see the resolvers skill.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/schemas.md from GitHub. Confirmed against the whole page: dotted and callable aliases, template-style lookup with indexes, get_<field>_display aliasing and the plain dict gotcha. Nothing removed.

Method: documentation only; no commands were run.
