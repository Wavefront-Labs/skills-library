---
id: computing-software.software-engineering.pydantic.model-serializers-and-context
name: model-serializers-and-context
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-model-serializers, model-serializer, serialization-info, serialization-context, wrap-serializer, plain-serializer]
level: practitioner
status: docs-checked
description: "Customize whole-model serialization with @model_serializer and pass runtime context to serializers through the info argument and the context parameter."
sources:
  - https://docs.pydantic.dev/latest/concepts/serialization/
  - https://docs.pydantic.dev/latest/errors/usage_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model serializers, serialization info and context

Goal: control the output of an entire model, and feed runtime data into serializers.

## `@model_serializer`

If `return_type` is given (or a return annotation exists), an extra serializer checks the output against it. Only one serializer per model.

Plain (default `mode='plain'`) is called unconditionally and may return a non-dict, though that can upset type checkers because `model_dump()` is typed `dict[str, Any]`:

```python
class UserModel(BaseModel):
    username: str
    password: str

    @model_serializer(mode='plain')
    def serialize_model(self) -> str:
        return f'{self.username} - {self.password}'
# model_dump() -> 'foo - bar'
```

Wrap needs a `handler` parameter that serializes the instance via Pydantic; you may not call it:

```python
@model_serializer(mode='wrap')
def serialize_model(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
    serialized = handler(self)
    serialized['fields'] = list(serialized)
    return serialized
# {'username': 'foo', 'password': 'bar', 'fields': ['username', 'password']}
```

Valid signatures (usage-errors page): instance method `(self)` or `(self, info: SerializationInfo)`; wrap adds `handler: SerializerFunctionWrapHandler` before `info`. A `@model_serializer` on a classmethod or without `self` raises `model-serializer-instance-method`; wrong arguments raise `model-serializer-signature`.

## Serialization info

Field and model serializers (any mode) may take an extra `info` argument exposing:

- `context` (user-defined),
- `mode` (`'python'` or `'json'`),
- the serialization-method parameters, e.g. `exclude_unset`, `serialize_as_any`,
- `field_name` (field serializers only, `FieldSerializationInfo`).

## Context

Pass `context=` to any serialization method and read `info.context` in the serializer:

```python
@field_serializer('text', mode='plain')
@classmethod
def remove_stopwords(cls, v: str, info: FieldSerializationInfo) -> str:
    if isinstance(info.context, dict):
        stopwords = info.context.get('stopwords', set())
        v = ' '.join(w for w in v.split() if w.lower() not in stopwords)
    return v

model.model_dump(context={'stopwords': ['this', 'is', 'an']})
# {'text': 'example document'}
```

Without `context`, the text is unchanged. A validation context also exists (see the validators docs).

## Checked

Checked 2026-11-07. Compared every claim with the serialization concepts page (concepts/serialization.md) and the usage errors page (errors/usage_errors.md): plain and wrap `@model_serializer` examples, `return_type`, the info argument contents (`context`, `mode`, method parameters, `field_name`), the `context=` parameter example, valid model serializer signatures, and the `model-serializer-instance-method` / `model-serializer-signature` codes. All confirmed; nothing removed.

Method: documentation only; no commands were run.
