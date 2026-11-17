---
id: computing-software.web-development.django-ninja.django-ninja-schema-resolvers
name: django-ninja-schema-resolvers
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, schema-resolvers, resolver, staticmethod, context, pydantic]
level: practitioner
status: docs-checked
description: "Compute Django Ninja schema fields with resolve_<field> static methods and read the request from the validation context."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/schemas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema resolvers and context

Goal: compute a field's value (or add one the source object lacks) with `resolve_<field>`.

```python
from ninja import Schema

class TaskSchema(Schema):
    id: int
    title: str
    lower_title: str

    @staticmethod
    def resolve_lower_title(obj):
        return obj.title.lower()
```

- The resolver takes the object being serialized as its only required argument.
- It overrides whatever the object would supply, even a matching attribute, so it can add a field that does not exist on the source at all.

## Must be @staticmethod

Only `@staticmethod` resolvers are supported. A regular method (expecting `self`) raises `NotImplementedError` when it runs.

## Accessing context

Add a `context` argument (or `**kwargs`) to receive Pydantic v2's validation context:

```python
class TaskSchema(Schema):
    id: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

- Used as a `response=` schema, Ninja passes `{"request": request, "response_status": <code>}` automatically.
- Used as request input (a body parameter, say), the context is `{"request": request}`, so input resolvers and validators can read `context["request"]` too.
- Outside a view, pass your own:

```python
TaskSchema.model_validate({"id": 1}, context={"request": my_request})
```

## Checked

2026-11-08: Read django-ninja docs/docs/guide/schemas.md from GitHub. Confirmed against the whole page: resolve_<field> as a staticmethod, NotImplementedError for regular methods, override behaviour, and the context arguments for response and input schemas. Nothing removed.

Method: documentation only; no commands were run.
