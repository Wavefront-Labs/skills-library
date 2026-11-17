---
id: computing-software.software-engineering.pydantic.pydantic-field-annotated-constraints
name: pydantic-field-annotated-constraints
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-metadata, annotated, field-constraints, field, model-fields, fieldinfo, strict]
level: practitioner
status: docs-checked
description: "Attach constraints and metadata to Pydantic fields with Field and Annotated, inspect model_fields, and avoid mixing field and type metadata."
sources:
  - https://docs.pydantic.dev/latest/concepts/fields/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add validation constraints and metadata the right way.

Constraints via `Field()`:

```python
class Model(BaseModel):
    positive: int = Field(gt=0)
    short_str: str = Field(max_length=3)
    precise_decimal: Decimal = Field(max_digits=5, decimal_places=2)
```
Per-type constraints are listed in the standard library types docs. For a union with `None` (or the `MISSING` sentinel), constraints are applied to the remaining members: `positive: int | None = Field(gt=0)` and `negative: Annotated[int | None, Field(lt=0)]`.

Annotated pattern:

```python
class Model(BaseModel):
    name: Annotated[str, Field(strict=True), WithJsonSchema({'extra': 'data'})]
```
Advantages: avoids `f: T = Field(...)` suggesting a default; allows arbitrary metadata (`Field()` supports a limited set, so utilities like `WithJsonSchema` are needed); types become reusable. Drawback: static checkers do not understand `Annotated` for `default`, `default_factory` and `alias`.

Metadata on parts of a type: `int_list: list[Annotated[int, Field(gt=0)]]` accepts `[1, 3]` and rejects `[-1, 2]`.

Do not mix field and type metadata:

```python
field_bad: Annotated[int, Field(deprecated=True)] | None = None   # applies to int only, no effect
field_ok: Annotated[int | None, Field(deprecated=True)] = None    # applies to the field
```
The `annotated_types` library is also supported.

Strict per field: `Field(strict=True)` validates that field in strict mode; `strict=False` is the default.

Inspecting: `Model.model_fields['a']` is a `FieldInfo` with `.annotation`, `.alias`, `.metadata`. For `Annotated[int, Field(gt=1), WithJsonSchema({'extra': 'data'}), Field(alias='b')] = 1` the docs show annotation `int`, alias `b`, metadata `[Gt(gt=1), WithJsonSchema(json_schema={'extra': 'data'}, mode=None)]`. In v3, `model_fields` is accessible from the class only, not the instance. Pydantic dataclasses use `__pydantic_fields__`.

## Checked

Checked 2026-11-07. Re-read concepts/fields in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
