---
id: computing-software.software-engineering.pydantic.read-validation-error-details
name: read-validation-error-details
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-error-details, validation-error, errors, loc, error-type, debugging]
level: practitioner
status: docs-checked
description: "Catch a Pydantic ValidationError and read its errors(), error_count(), json() and ErrorDetails keys (loc, type, msg, input, ctx, url) to locate bad fields."
sources:
  - https://docs.pydantic.dev/latest/errors/errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: turn a raised `ValidationError` into a precise list of which fields failed, where, and why.

## Raising rule
Validation code should not raise `ValidationError` itself. Raise `ValueError` or `AssertionError` (or a subclass); Pydantic catches it and uses it to populate the final `ValidationError`.

## Accessing the errors
A `ValidationError` holds information about all errors, not just the first.

| Method | Returns |
|---|---|
| `errors()` | list of `ErrorDetails` found in the input |
| `error_count()` | number of errors |
| `json()` | JSON representation of the list of errors |
| `str(e)` | human-readable representation |

## ErrorDetails keys
`ErrorDetails` is a dictionary with:

- `ctx`: optional object with values needed to render the message
- `input`: the input provided for validation
- `loc`: the error location as a list
- `msg`: human-readable explanation
- `type`: computer-readable identifier of the error type
- `url`: documentation URL for the error

The first item of `loc` is the field where the error occurred. For a sub-model field, further items give the nested location, e.g. `('recursive_model', 'lng')`. List positions appear as integers, e.g. `('list_of_ints', 2)`.

## Example pattern
```python
try:
    Model(**data)
except ValidationError as e:
    print(e)           # "5 validation errors for Model" + one entry per field
    print(e.errors())  # list of dicts
```
In the page's example, a missing field gives `type` `'missing'` with `msg` `'Field required'`; `Field(gt=42)` given 21 gives `'greater_than'` with `ctx` `{'gt': 42}`; a failing `@field_validator` that raises `ValueError('Invalid float value')` gives `'value_error'` with `msg` `'Value error, Invalid float value'` and `ctx` `{'error': ValueError(...)}`.

## Reference
Each error `type` is documented in the Validation Errors page (and usage errors in Usage Errors). The `url` key points at `https://errors.pydantic.dev/2/v/<type>`.

## Checked

Checked 2026-11-07. Re-read errors/errors in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
