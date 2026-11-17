---
id: computing-software.software-engineering.pydantic.field-after-before-validators
name: field-after-before-validators
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-validators, field-validator, aftervalidator, beforevalidator, validation, python]
level: practitioner
status: docs-checked
description: "Write Pydantic field validators in after and before mode, with the Annotated pattern or the field_validator decorator, and know what each mode receives."
sources:
  - https://docs.pydantic.dev/latest/concepts/validators/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field after and before validators

Goal: add custom checks or coercion to one field, running after or before Pydantic's own validation.

A field validator is a callable that takes the value and **returns the validated value**. It may raise to reject, or return a changed value.

## After validators (more type safe, easier)

Run after Pydantic's internal validation.

```python
from typing import Annotated
from pydantic import AfterValidator, BaseModel

def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value  # always return the value

class Model(BaseModel):
    number: Annotated[int, AfterValidator(is_even)]
```

Decorator form (`'after'` is the default `mode`, so it can be omitted):

```python
from pydantic import BaseModel, field_validator

class Model(BaseModel):
    number: int

    @field_validator('number', mode='after')
    @classmethod
    def is_even(cls, value: int) -> int:
        ...
```

Error text shown by the page: `Value error, 1 is not an even number [type=value_error, input_value=1, input_type=int]`.

## Before validators (raw input)

Run before parsing, so the input can be any object; annotate it `Any`. The returned value is then validated against the field type.

```python
def ensure_list(value: Any) -> Any:
    if not isinstance(value, list):
        return [value]
    return value

numbers: Annotated[list[int], BeforeValidator(ensure_list)]
# decorator: @field_validator('numbers', mode='before')
```

`Model(numbers=2)` gives `numbers=[2]`; `Model(numbers='str')` still fails with `Input should be a valid integer` at `numbers.0`, because Pydantic validates against `int` regardless.

## Gotchas stated by the page

- In before validators you must handle every input shape (for example tuples that `list` would normally accept).
- Do not mutate the raw value and then raise later: the mutated value may reach other validators when unions are used.
- Default values are not validated unless configured to be, so custom validators do not run on defaults.

## Checked

Checked 2026-11-07. Compared every claim with the validators concepts page (concepts/validators.md): after and before semantics, the `is_even` example and its error text, `'after'` as the default decorator mode, the `ensure_list` example and its `numbers.0` error, the raw-input and union-mutation warnings, and that defaults are not validated. All confirmed; nothing removed.

Method: documentation only; no commands were run.
