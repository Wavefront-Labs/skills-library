---
id: computing-software.software-engineering.pydantic.validation-utility-types
name: validation-utility-types
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-utility-types, instanceof, skipvalidation, validateas, onerroromit, failfast, python]
level: practitioner
status: docs-checked
description: "Apply Pydantic utility annotations InstanceOf, SkipValidation, ValidateAs, OnErrorOmit and FailFast to tailor how fields and collections are validated."
sources:
  - https://docs.pydantic.dev/latest/concepts/validators/
  - https://docs.pydantic.dev/latest/concepts/types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validation utility types

Goal: pick the right built-in annotation instead of writing a custom validator.

## `InstanceOf`

Validate that a value is an instance of a class (no coercion).

```python
class Basket(BaseModel):
    fruits: list[InstanceOf[Fruit]]

Basket(fruits=[Banana(), 'Apple'])
# fruits.1  Input should be an instance of Fruit [type=is_instance_of, ...]
```

## `SkipValidation`

Skip validation on a field or part of one. A wrong-typed value then emits a warning during serialization.

```python
class Model(BaseModel):
    names: list[SkipValidation[str]]

Model(names=['foo', 123])  # names=['foo', 123]
```

## `ValidateAs`

Validate a custom type from a type Pydantic supports natively; useful for custom types with multiple fields.

```python
ta = TypeAdapter(
    Annotated[MyCls, ValidateAs(ValModel, lambda v: MyCls(a=v.a))]
)
ta.validate_python({'a': 1})  # MyCls(a=1)
```

(`ValModel` is a `BaseModel` with `a: int`.)

## `OnErrorOmit` (v2.6+)

Normally one failing item discards the whole collection (list, dict, `TypedDict`). With `OnErrorOmit`, failing items are silently dropped and valid ones kept.

```python
ta = TypeAdapter(list[OnErrorOmit[int]])
ta.validate_python([1, 2, 'a', 3])  # [1, 2, 3]
```

## `FailFast` (v2.8+)

By default every item is validated and all errors reported. Apply `FailFast()` to a collection type (list, tuple, set, dict) to stop at the first failure: faster, but less error information.

```python
ta = TypeAdapter(Annotated[list[int], FailFast()])
ta.validate_python([1, 'a', 2, 'b'])
# 1 validation error for list[int]
# 1
#   Input should be a valid integer, unable to parse string as an integer
```

Only the first failure (index 1) is reported.

## Imports

`from pydantic import InstanceOf, SkipValidation, ValidateAs, OnErrorOmit, FailFast, TypeAdapter`.

## Checked

Checked 2026-11-07. Re-read the Special types section of concepts/validators and the Utility types section of concepts/types, which hold every claim; the rest of the types page was not read. Compared every claim; no changes needed.

Method: documentation only; no commands were run.
