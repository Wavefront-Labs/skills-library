---
id: computing-software.web-development.django-ninja.django-ninja-schema-files-selfref-standalone
name: django-ninja-schema-files-selfref-standalone
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, files-images, self-reference, model-rebuild, from-orm, imagefield]
level: practitioner
status: docs-checked
description: "Serialize FileField/ImageField as URLs, build self-referencing Django Ninja schemas with model_rebuild, and use Schema outside a view."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/schemas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Files, self-referencing schemas, and serializing outside a view

## FileField / ImageField

These convert to their `str` URL by default. For `image = models.ImageField(upload_to="images")`:

```python
class PictureSchema(Schema):
    title: str
    image: str
```

A `FieldFile` serializes to its `.url`, e.g. `"/media/images/zebra.jpg"`. If the field can be empty, type it `str | None`: an empty `FieldFile` then becomes `None`. With a plain `str`, an empty value raises a validation error.

## Self-referencing schema

Quote the type and call `model_rebuild()` after the class is defined:

```python
class Comment(Schema):
    text: str
    replies: "list[Comment] | None" = None

Comment.model_rebuild()  # required to resolve the quoted type
```

For a schema from `create_schema()`, pass `name="..."` explicitly so it can be rebuilt (see the create_schema skill).

## Serializing outside a view

Useful in management commands, signal handlers, tests:

```python
>>> data = PersonSchema.from_orm(person)
>>> data
PersonSchema(name='Mr. Smith')
>>> data.dict()
{'name': 'Mr. Smith'}
>>> [PersonSchema.from_orm(p).dict() for p in Person.objects.all()]
[{'name': 'Mr. Smith'}, {'name': 'Mrs. Smith'}]
```

`.from_orm(obj)` is an alias for `.model_validate(obj)`; `.dict()` is an alias for `.model_dump()`. You can also use `.model_dump_json()`.

## Schema vs plain Pydantic

`Schema` has `from_attributes=True` by default, so it reads objects as well as dicts without opting in.

## Deprecated

`.schema()` still works but emits a `DeprecationWarning`; use `.model_json_schema()` or Ninja's `.json_schema()` (which also cleans up the output for OpenAPI).

## Checked

2026-11-08: Read django-ninja docs/docs/guide/schemas.md from GitHub. Confirmed against the whole page: FileField and ImageField as str URLs, self-referencing schemas with model_rebuild, create_schema name, from_orm and dict aliases, from_attributes default and the deprecated schema() method. Nothing removed.

Method: documentation only; no commands were run.
