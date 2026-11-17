---
id: computing-software.software-engineering.pydantic.fix-model-and-call-argument-errors
name: fix-model-and-call-argument-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validation-error-types, frozen-instance, from-attributes, validate-call, missing-argument, extra-forbidden, model-type]
level: practitioner
status: docs-checked
description: "Diagnose Pydantic model-level and validate_call errors: model_type, frozen_instance, get_attribute_error, no_such_attribute, missing_argument, unexpected_keyword_argument."
sources:
  - https://docs.pydantic.dev/latest/errors/validation_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: identify why a model, dataclass or `@validate_call` function rejected its input from the error `type`.

## Model input
- `model_type`: input to a model is not a model instance or dict (`Model.model_validate('not an object')`).
- `model_attributes_type`: with `from_attributes=True`, input is not a dict, model instance, or object fields can be extracted from. Use `Model.model_validate(obj, from_attributes=True)` for arbitrary objects.
- `get_attribute_error`: with `model_config['from_attributes'] == True`, reading an attribute raised (e.g. a property raising `RuntimeError`).
- `invalid_key`: a `dict` input has a non-`str` key (e.g. `b'y'` with `extra='allow'`).
- `extra_forbidden`: extra input with `ConfigDict(extra='forbid')`.
- `default_factory_not_called`: a default factory that takes validated data (`Field(default_factory=lambda data: data['a'])`) cannot run because an earlier field failed; you get the earlier field's error plus this one.
- `dataclass_type`: input not valid for a dataclass field. `dataclass_exact_type`: with `strict=True`, input must be an instance of the dataclass, not a dict.
- `missing_sentinel_error`: `MISSING` is the only value allowed for the field and it was not provided (page example: `f: MISSING` given `f=1`).

## Mutation
- `frozen_field`: assigning to or deleting a field declared `Field('test', frozen=True)`.
- `frozen_instance`: assigning or deleting any field when `ConfigDict(frozen=True)`.
- `no_such_attribute`: with `validate_assignment=True`, assigning an attribute that is not a field (page uses a pydantic dataclass with `config=ConfigDict(validate_assignment=True)`).

## `@validate_call` functions
| Type | Cause |
|---|---|
| `missing_argument` | required positional-or-keyword arg not passed |
| `missing_keyword_only_argument` | required `*, a` arg not passed |
| `missing_positional_only_argument` | required `a, /` arg not passed |
| `multiple_argument_values` | `foo(1, a=2)` for `def foo(a: int)` |
| `unexpected_keyword_argument` | keyword given for a positional-only arg (check `errors()[1]`); also raised by pydantic dataclasses with `extra='forbid'` |
| `unexpected_positional_argument` | positional given for a keyword-only arg (check `errors()[1]`) |
| `arguments_type` | arguments object is not a `dict` (`TypeAdapter(func).validate_python('invalid')`) |

## Custom validators
- `assertion_error`: a failing `assert` inside a validator.
- `value_error`: a `ValueError` raised in a validator.
- `recursion_depth_exceeded`: input nested deeper than allowed (varies by platform and release). `recursion_loop`: cyclic reference in input; see handle-cyclic-references.
- `needs_python_object`: validating from JSON where Python object checks (`isinstance`, `issubclass`) are needed, e.g. `type[BaseModel]` field.

## Checked

Checked 2026-11-07. Compared every claim with the validation errors page (errors/validation_errors.md). Corrected `arguments_type`, which the page describes as the arguments object not being a `dict` (the skill said tuple, list or dict). Reworded `missing_sentinel_error` to match the page. All other model, mutation and `validate_call` entries confirmed.

Method: documentation only; no commands were run.
