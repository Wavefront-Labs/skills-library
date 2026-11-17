---
id: computing-software.web-development.django-ninja.django-ninja-modelschema-fields-relations
name: django-ninja-modelschema-fields-relations
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, modelschema, meta-fields, foreignkey, many-to-many, register-field, exclude]
level: practitioner
status: docs-checked
description: "Generate Django Ninja ModelSchema from a model with Meta fields/exclude, handle relations and FK ids, override fields, and register custom field types."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/model-schema.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ModelSchema: fields, relations, overrides

Goal: generate a Schema from a Django model without retyping fields.

```python
from ninja import ModelSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]
```

`model` also accepts `"app_label.ModelName"` (e.g. `"auth.User"`). `null`/`blank` become optional with `None` default; `default`, `help_text` (description) and `verbose_name` (title) are copied.

## Selecting fields

- `fields = "__all__"` includes everything, but is not recommended (can expose e.g. a hashed password).
- `exclude = ["password", "last_login", "user_permissions"]` takes everything else.
- One of `fields` or `exclude` is required; combining them raises `ConfigError`.

## Relations

A `ForeignKey` becomes the related primary-key type (`int` by default); a `ManyToManyField` becomes a list of it. For nested objects, declare the field with another schema (or use `create_schema(..., depth=...)`). Reverse relations are never included, even with `"__all__"`; declare them yourself.

## FK ids

List the field name (`author`), not `author_id` (that raises `ConfigError`). To expose the raw id, declare it as an annotated field; it reads `obj.author_id` with no extra query:

```python
class CommentSchema(ModelSchema):
    author: UserSchema  # nested object
    author_id: int      # plain id

    class Meta:
        model = Comment
        fields = ["id", "text"]
```

## Overriding and adding

A normal annotated attribute takes priority over the generated field:

```python
class UserSchema(ModelSchema):
    groups: list[GroupSchema] = []

    class Meta:
        model = User
        fields = ["id", "username"]
```

Do not also list it in `Meta.fields`: that emits a `DeprecationWarning` and will become an error. Methods work as on any Schema.

## Custom field types

An unknown Django field type gives a `ConfigError`. Register it once before the schema is defined:

```python
from ninja.orm import register_field

register_field("VectorField", list[float])
```

The first argument is the field's internal type name.

## Tip

`TextField.max_length` is enforced only on incoming data, not when serializing. Identical definitions reuse the cached generated class.

## Checked

2026-11-07: Confirmed against guide/model-schema.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
