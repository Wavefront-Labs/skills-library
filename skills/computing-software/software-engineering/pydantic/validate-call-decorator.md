---
id: computing-software.software-engineering.pydantic.validate-call-decorator
name: validate-call-decorator
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validate-call, validate-call, function-arguments, validate-return, raw-function, async, python]
level: practitioner
status: docs-checked
description: "Validate and coerce function arguments with Pydantic validate_call: signatures, Field constraints, return validation, config, async use, raw_function and limits."
sources:
  - https://docs.pydantic.dev/latest/concepts/validation_decorator/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `validate_call` decorator

Goal: parse and validate a function's arguments from its annotations before the call.

```python
from pydantic import ValidationError, validate_call

@validate_call
def repeat(s: str, count: int, *, separator: bytes = b'') -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))

repeat('x', '4', separator=b' ')   # b'x x x x' ('4' coerced to int)
repeat('hello', 'wrong')           # ValidationError, location 1
```

## Types and return values

Unannotated parameters are `Any`. Arguments are coerced by default (a `'2000-01-01'` string becomes a `date`); use a custom config for strict mode. The return value is **not** validated unless you pass `validate_return=True` to the decorator.

## Signatures supported

Positional-or-keyword, keyword-only (after `*,`), positional-only (before `/`), `*args`, `**kwargs`. `Unpack` with a `TypedDict` can annotate `**kwargs` (v2.10+):

```python
class Point(TypedDict):
    x: int
    y: int

@validate_call
def add_coords(**kwargs: Unpack[Point]) -> int:
    return kwargs['x'] + kwargs['y']
```

## Field constraints

Use the Annotated pattern so type checkers see the parameter as required:

```python
@validate_call
def how_many(num: Annotated[int, Field(gt=10)]):
    return num
```

`how_many(1)` errors at location `0`: `Input should be greater than 10`. A default can be `value: str = Field(default='default value')`. Aliases work: `Annotated[int, Field(gt=10, alias='number')]` called as `how_many(number=42)`.

## Config

`@validate_call(config=ConfigDict(arbitrary_types_allowed=True))` accepts custom classes; wrong instances give `Input should be an instance of Foobar`.

## Async

Decorate `async def` functions directly; errors arrive when awaited, e.g. `PositiveInt` with `-4` gives type `greater_than`, `loc (0,)`.

## raw_function and pre-validation

`repeat.raw_function('good bye', 2, separator=b', ')` calls the original without validation (type checkers may need `# type: ignore`). To validate before a costly call, return an inner function:

```python
@validate_call
def validate_foo(a: int, b: int):
    def foo():
        return a + b
    return foo

foo = validate_foo(a=1, b=2)
```

## Limits

Failures raise `ValidationError`, even for missing required arguments (Python normally raises `TypeError`). Calls cost more than the undecorated function; it is not a strongly typed language substitute.

## Checked

Checked 2026-11-07. Re-read concepts/validation_decorator in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
