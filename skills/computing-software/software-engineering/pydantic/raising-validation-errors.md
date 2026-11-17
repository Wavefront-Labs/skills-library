---
id: computing-software.software-engineering.pydantic.raising-validation-errors
name: raising-validation-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validator-errors, valueerror, assertionerror, pydanticcustomerror, validation-error, python]
level: practitioner
status: docs-checked
description: "Reject data inside Pydantic validators with ValueError, assert or PydanticCustomError, and use PydanticUseDefault to fall back to a field default."
sources:
  - https://docs.pydantic.dev/latest/concepts/validators/
  - https://docs.pydantic.dev/latest/concepts/unions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raising validation errors in validators

Goal: signal invalid data from a validator so Pydantic reports a `ValidationError`.

## The three exception types

- `ValueError`: the most common choice. Message appears as `Value error, <message> [type=value_error, ...]`.
- `AssertionError`: an `assert` statement also works, but asserts are **skipped when Python runs with the `-O` flag**, so do not rely on them for required checks.
- `PydanticCustomError` (from `pydantic_core`): more verbose, gives control of the error type, message template and context.

```python
from pydantic_core import PydanticCustomError
from pydantic import BaseModel, ValidationError, field_validator

class Model(BaseModel):
    x: int

    @field_validator('x', mode='after')
    @classmethod
    def validate_x(cls, v: int) -> int:
        if v % 42 == 0:
            raise PydanticCustomError(
                'the_answer_error',
                '{number} is the answer!',
                {'number': v},
            )
        return v

try:
    Model(x=42 * 2)
except ValidationError as e:
    print(e)
    # 1 validation error for Model
    # x
    #   84 is the answer! [type=the_answer_error, input_value=84, input_type=int]
```

Arguments in order: error type string, message template with `{placeholders}`, context dict that fills them.

## Falling back to the default

Raise `PydanticUseDefault` (from `pydantic_core`) in a before validator to tell Pydantic to use the field's default:

```python
from typing import Annotated, Any
from pydantic_core import PydanticUseDefault
from pydantic import BaseModel, BeforeValidator

def default_if_none(value: Any) -> Any:
    if value is None:
        raise PydanticUseDefault()
    return value

class Model(BaseModel):
    name: Annotated[str, BeforeValidator(default_if_none)] = 'default_name'

print(Model(name=None))  # name='default_name'
```

## Reminders

- A validator must return the (possibly changed) value when it does not raise.
- Union-member errors can be customised on a callable `Discriminator` with `custom_error_type`, `custom_error_message`, `custom_error_context` (see the discriminated-unions skill).

## Checked

Checked 2026-11-07. Re-read concepts/validators (in chunks) and concepts/unions in full. Confirmed the ValueError and AssertionError, PydanticCustomError and PydanticUseDefault claims and the Discriminator custom_error_type, custom_error_message and custom_error_context claim; no changes needed.

Method: documentation only; no commands were run.
