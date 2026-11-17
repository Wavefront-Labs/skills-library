---
id: computing-software.web-development.django-ninja.django-ninja-create-schema-function
name: django-ninja-create-schema-function
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, create-schema, depth, custom-fields, base-class, dynamic-schema]
level: practitioner
status: docs-checked
description: "Build Django Ninja schemas at runtime with create_schema: fields, exclude, depth, optional_fields, custom_fields, name, base_class and caching."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/create-schema.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# create_schema: runtime schema generation

Goal: make a Schema from a model when the model, fields or depth are only known at runtime. Otherwise prefer `ModelSchema` (a real class: editor support, `isinstance`, your own fields and `resolve_*` methods).

```python
from ninja.orm import create_schema

UserSchema = create_schema(User, fields=["id", "username"])
```

With no `fields`/`exclude` it includes **every** field (may expose a hashed password); always pass one. Passing both raises `ConfigError`.

## Arguments

- `name`: class name (defaults to the model name). A name already used by an earlier call, even for another model, gets a numeric suffix (`User2`, `User3`).
- `depth`: levels of related models to introspect.
- `fields` / `exclude`, `optional_fields`, `custom_fields`, `base_class`.

## depth

By default FK/M2M become primary keys. `depth=1` builds nested schemas:

```python
UserSchema = create_schema(User, depth=1, fields=["username", "groups"])
# groups: list[Group]
```

The nested `Group` uses **all** its fields; `fields`/`exclude` apply only to the top-level model. Keep depth small; it pulls in more data and queries.

## optional_fields

`optional_fields=["first_name", "last_name"]` or `"__all__"`.

## custom_fields

A list of `(name, type, default)` tuples to add or override fields:

```python
from ninja import Field

UserSchema = create_schema(
    User,
    fields=["id", "username"],
    custom_fields=[
        ("full_name", str, None),
        ("id", str, Field(..., description="UUID")),
    ],
)
```

`...` marks required; any other default (including `None`) makes it omittable. A plain default does not change the type: `("full_name", str, None)` still rejects an explicit `None`. Use `Optional[str]` / `str | None` to accept `None`.

## Self reference

```python
UserSchema = create_schema(
    User, name="UserSchema", fields=["id", "username"],
    custom_fields=[("manager", "UserSchema", None)],
)
UserSchema.model_rebuild()
```

`name` is required and must match the quoted type.

## base_class

`create_schema(User, fields=[...], base_class=BaseSchema)` inherits your Schema subclass.

## Caching

Same `model`, `name`, `depth`, `fields`, `exclude`, `optional_fields`, `custom_fields` returns the same class, so calling per request is cheap. `base_class` is **not** in the cache key: calls differing only by `base_class` return the first result unless you give them distinct `name`s.

## Checked

2026-11-07: Confirmed against guide/create-schema.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
