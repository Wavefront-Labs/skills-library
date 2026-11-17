---
id: computing-software.software-engineering.pydantic.field-serializers
name: field-serializers
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-serializers, field-serializer, plain-serializer, wrap-serializer, annotated, serialization, custom-serializer]
level: practitioner
status: docs-checked
description: "Write Pydantic field serializers with PlainSerializer, WrapSerializer or @field_serializer, and choose between the annotated and decorator patterns."
sources:
  - https://docs.pydantic.dev/latest/concepts/serialization/
  - https://docs.pydantic.dev/latest/errors/usage_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom field serializers

Goal: change how one field (or several) is serialized.

Only one serializer can be defined per field. Plain and wrap serializers cannot be combined.

A field serializer takes the value and returns the serialized value. If `return_type` is passed (or the function has a return annotation), Pydantic builds an extra serializer so the output complies with that type.

## Plain: called unconditionally

Pydantic's own logic for the type is not called. Output is not validated against the field type.

```python
from typing import Annotated, Any
from pydantic import BaseModel, PlainSerializer, field_serializer

def ser_number(value: Any) -> Any:
    return value * 2 if isinstance(value, int) else value

class A(BaseModel):
    number: Annotated[int, PlainSerializer(ser_number)]

class B(BaseModel):
    number: int

    @field_serializer('number', mode='plain')  # 'plain' is the default
    def ser_number(self, value: Any) -> Any:
        return value * 2 if isinstance(value, int) else value
```

`Model(number=4).model_dump()` gives `{'number': 8}`. After `m.number = 'invalid'`, dumping gives `{'number': 'invalid'}` (no validation).

## Wrap: run code around Pydantic's logic

Requires an extra `handler` parameter (`SerializerFunctionWrapHandler`) that delegates to Pydantic. You may skip calling it.

```python
def ser_number(value: Any, handler: SerializerFunctionWrapHandler) -> int:
    return handler(value) + 1
# Annotated[int, WrapSerializer(ser_number)]  ->  {'number': 5} for 4
# or @field_serializer('number', mode='wrap') with (self, value, handler)
```

## Annotated vs decorator

- Annotated pattern: reusable (`DoubleNumber = Annotated[int, PlainSerializer(lambda v: v * 2)]`), visible in the annotation, and can target parts of a type (`list[DoubleNumber]` serializes items only).
- Decorator: apply to several fields, `@field_serializer('f1', 'f2', mode='plain')`.
- `'*'` as the field name applies to all fields, including those in subclasses.
- Names are checked at class creation; pass `check_fields=False` when the serializer sits on a base class and the field exists only on subclasses.

## Valid decorator signatures (usage-errors page)

Instance method `(self, value, info)`, static method or function `(value, info)`; wrap mode adds `nxt: SerializerFunctionWrapHandler` before `info`. `info` (`FieldSerializationInfo`) can be omitted.

Gotcha: two `@field_serializer` functions covering the same field raise `multiple-field-serializers`.

## Checked

Checked 2026-11-07. Compared every claim with the serialization concepts page (concepts/serialization.md) and the usage errors page (errors/usage_errors.md): one serializer per field, `return_type`, plain and wrap behaviour and the `{'number': 8}` / `{'number': 5}` results, annotated versus decorator benefits, `'*'`, `check_fields=False`, the valid `field_serializer` signatures and the `multiple-field-serializers` code. All confirmed; nothing removed.

Method: documentation only; no commands were run.
