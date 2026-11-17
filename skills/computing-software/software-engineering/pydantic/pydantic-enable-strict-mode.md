---
id: computing-software.software-engineering.pydantic.pydantic-enable-strict-mode
name: pydantic-enable-strict-mode
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-strict-mode, strict, lax-mode, strictint, strict-metadata, validation]
level: practitioner
status: docs-checked
description: "Turn on Pydantic strict mode per call, per field with Field or Strict, or per model via ConfigDict, and know how JSON input differs."
sources:
  - https://docs.pydantic.dev/latest/concepts/strict_mode/
  - https://docs.pydantic.dev/latest/concepts/fields/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make Pydantic raise instead of coercing.

Default (lax) mode coerces, e.g. `'123'` to `123` for `int`. Strict mode mostly only accepts instances of the declared type, though JSON input is looser (date and time types accept strings even in strict mode). Strict behaviour per type is in the standard library types docs and the conversion table.

```python
class MyModel(BaseModel):
    x: int

MyModel.model_validate({'x': '123'})                # x=123
MyModel.model_validate({'x': '123'}, strict=True)   # int_type: Input should be a valid integer
```

Three levels:

1. Validation parameter: `strict=True` on `model_validate()` and TypeAdapter methods.
```python
TypeAdapter(date).validate_python('2000-01-01')               # OK
TypeAdapter(date).validate_python('2000-01-01', strict=True)  # date_type error
TypeAdapter(date).validate_json('"2000-01-01"', strict=True) # OK, JSON is looser
```
2. Field level: `age: int = Field(strict=True)` or `Annotated[int, Field(strict=True)]`. The validation parameter has priority over the field setting: `User.model_validate({...'age': '42'}, strict=False)` succeeds.
3. Config level: `model_config = ConfigDict(strict=True)` on models and model-like classes such as dataclasses, with field-level override:

```python
class User(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str
    age: int = Field(strict=False)

User(name='John', age='18')   #> name='John' age=18
```

Strict metadata class: `Annotated[UUID, Strict()]`. Aliases: `StrictBool`, `StrictInt`, `StrictFloat`, `StrictStr`, `StrictBytes`; `age: StrictInt` equals `Annotated[int, Strict()]`.

Rollout caveat: enabling strict mode on models an existing application relies on makes previously coerced inputs fail. If you cannot audit all callers, watch validation failures during rollout (the docs mention Logfire metrics and recorded rejected values).

## Checked

Checked 2026-11-07. Re-read concepts/strict_mode and concepts/fields in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
