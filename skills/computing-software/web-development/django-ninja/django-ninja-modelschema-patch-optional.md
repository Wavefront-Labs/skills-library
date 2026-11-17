---
id: computing-software.web-development.django-ninja.django-ninja-modelschema-patch-optional
name: django-ninja-modelschema-patch-optional
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, patch-update, fields-optional, patchdict, exclude-unset, modelschema]
level: practitioner
status: docs-checked
description: "Build PATCH endpoints in Django Ninja with ModelSchema fields_optional, exclude_unset, or PatchDict so unsent fields stay untouched."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/model-schema.md
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/create-schema.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PATCH payloads: fields_optional and PatchDict

Goal: accept partial updates where every field is optional.

## fields_optional

```python
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ["id", "name"]  # name is required on the model
        fields_optional = "__all__"
```

Or only a subset: `fields_optional = ["name"]`.

## Apply only what was sent

Use `exclude_unset=True` so fields the client omitted are not reset to `None`:

```python
@api.patch("/patch/{pk}", response=PatchGroupSchema)
def patch(request, pk: int, payload: PatchGroupSchema):
    obj = get_object_or_404(Group, pk=pk)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(obj, attr, value)
    obj.save()
    return obj
```

## PatchDict shortcut

Wrap any Schema in `PatchDict[...]`. Every field becomes optional and the validated payload is a plain `dict` holding only the keys actually sent; no `fields_optional` or `exclude_unset` needed.

```python
from ninja import NinjaAPI, PatchDict, Schema

class GroupSchema(Schema):
    name: str  # no need to declare Optional

@api.patch("/groups/{pk}", response=GroupSchema)
def update_group(request, pk: int, payload: PatchDict[GroupSchema]):
    obj = get_object_or_404(Group, pk=pk)
    for attr, value in payload.items():
        setattr(obj, attr, value)
    obj.save()
    return obj
```

The same idea exists in `create_schema` as `optional_fields`.

## Checked

2026-11-07: Confirmed against the ModelSchema guide (`fields_optional`, `exclude_unset`, `PatchDict`); the closing `create_schema` `optional_fields` note is confirmed on the Create Schema guide, added as a source after reading it. Nothing removed.

Method: documentation only; no commands were run.
