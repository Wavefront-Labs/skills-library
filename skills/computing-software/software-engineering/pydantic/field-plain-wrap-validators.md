---
id: computing-software.software-engineering.pydantic.field-plain-wrap-validators
name: field-plain-wrap-validators
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-validators, plainvalidator, wrapvalidator, handler, field-validator, python]
level: practitioner
status: docs-checked
description: "Use Pydantic plain validators to bypass type validation and wrap validators to run code around it with a handler, via Annotated or field_validator."
sources:
  - https://docs.pydantic.dev/latest/concepts/validators/
  - https://docs.pydantic.dev/latest/concepts/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field plain and wrap validators

Goal: take over validation for a field (plain) or intercept Pydantic's validation (wrap).

## Plain validators

Act like before validators but **terminate validation immediately**: no further validators run and Pydantic does no internal validation against the field type.

```python
from typing import Annotated, Any
from pydantic import BaseModel, PlainValidator

def val_number(value: Any) -> Any:
    if isinstance(value, int):
        return value * 2
    return value

class Model(BaseModel):
    number: Annotated[int, PlainValidator(val_number)]

print(Model(number=4))          # number=8
print(Model(number='invalid'))  # number='invalid' -- accepted, type check skipped
```

Decorator form: `@field_validator('number', mode='plain')` on a classmethod.

## Wrap validators

Most flexible: run code before or after Pydantic and other validators, return early, or raise. They need a **mandatory** extra `handler` parameter, a callable that delegates to Pydantic. You may wrap it in `try..except` or not call it at all.

```python
from typing import Annotated, Any
from pydantic import BaseModel, Field, ValidationError, ValidatorFunctionWrapHandler, WrapValidator

def truncate(value: Any, handler: ValidatorFunctionWrapHandler) -> str:
    try:
        return handler(value)
    except ValidationError as err:
        if err.errors()[0]['type'] == 'string_too_long':
            return handler(value[:5])
        raise

class Model(BaseModel):
    my_string: Annotated[str, Field(max_length=5), WrapValidator(truncate)]

print(Model(my_string='abcdef'))  # my_string='abcde'
```

Decorator form: `@field_validator('my_string', mode='wrap')` with signature `(cls, value, handler: ValidatorFunctionWrapHandler)` on a classmethod.

## Notes from the pages

- Wrap validators are generally slower than other validators because data must be materialised in Python; avoid them when performance is critical.
- For plain validators `json_schema_input_type` defaults to `Any`, since the field type is completely discarded.
- Default values are not validated unless configured, so these validators do not run on defaults.

## Checked

Checked 2026-11-07. Compared every claim with the validators concepts page (concepts/validators.md) and the performance page (concepts/performance.md): plain validators ending validation, the `val_number` results, the mandatory `handler` parameter and `try..except` freedom, the `truncate` example, `json_schema_input_type` defaulting to `Any` for plain validators, the slower-wrap note (data materialised in Python) and unvalidated defaults. All confirmed; nothing removed.

Method: documentation only; no commands were run.
