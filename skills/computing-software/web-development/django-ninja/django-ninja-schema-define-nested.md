---
id: computing-software.web-development.django-ninja.django-ninja-schema-define-nested
name: django-ninja-schema-define-nested
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, schema-definition, schema, pydantic, nested-schema, response, n-plus-one]
level: intro
status: docs-checked
description: "Define Django Ninja Schema classes for input and output, nest them, return ORM objects and querysets, and avoid N+1 queries."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/schemas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Define and nest Django Ninja schemas

Goal: describe request and response data with `ninja.Schema` (a `pydantic.BaseModel` subclass, named Schema to avoid clashing with `django.db.models.Model`).

## Define

```python
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str
    is_active: bool = True
```

- No default = required. A default = optional (the default is used when missing).
- Use `field: type | None = None` for a field that is optional and may be `null`.
- Any Pydantic-supported type works (`str`, `int`, `datetime`, `UUID`, `Decimal`, `Enum`, `list[...]`, `dict[...]`, other Schemas).

## Separate in and out schemas

```python
class UserIn(Schema):
    username: str
    password: str

class UserOut(Schema):
    id: int
    username: str

@api.post("/users", response=UserOut)
def create_user(request, data: UserIn):
    user = User.objects.create_user(data.username, password=data.password)
    return user
```

The response is limited to the fields declared on `UserOut`, even if the returned object has more attributes.

## Nesting

A field can be another Schema or `list[...]` of one:

```python
class OwnerSchema(Schema):
    id: int
    first_name: str

class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: OwnerSchema | None = None

@api.get("/tasks", response=list[TaskSchema])
def tasks(request):
    return Task.objects.select_related("owner")
```

This validates straight off ORM objects (no dicts needed). A task without an owner serializes `owner` as `null`.

## Relations

When the source value for a field is a Django `Manager` or `QuerySet` (a `related_set`, say), Ninja evaluates it to a plain list before validation, so type the field `list[ChildSchema]` without calling `.all()` or `list()`.

## Gotcha: N+1 queries

Serializing `owner` touches `task.owner` per task. Use `select_related` for `ForeignKey`/`OneToOneField` and `prefetch_related` for to-many or reverse relations.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/schemas.md from GitHub. Confirmed against the whole page: schema definition, required versus optional fields, separate in and out schemas, nesting, Manager and QuerySet evaluation and the N+1 note. Nothing removed.

Method: documentation only; no commands were run.
