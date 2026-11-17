---
id: computing-software.software-engineering.pydantic.fix-validate-call-errors
name: fix-validate-call-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-usage-errors, validate-call, unpack, typeddict, self-type, classmethod, pydantic-user-error]
level: practitioner
status: docs-checked
description: "Fix Pydantic validate-call-type, unpack-typed-dict, overlapping-unpack-typed-dict and invalid-self-type errors raised when decorating functions with validate_call."
sources:
  - https://docs.pydantic.dev/latest/errors/usage_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Usage errors with `validate_call`

Goal: resolve `PydanticUserError` codes raised by `@validate_call`.

## `validate-call-type`

Supported callables: functions (including lambdas, not built-ins), methods, and instances of `functools.partial` (the wrapped function must itself be supported).

- `@classmethod`, `@staticmethod`, `@property` must go before (outside) `validate_call`:

```python
class A:
    @validate_call
    @classmethod
    def f1(cls): ...      # error

@classmethod
@validate_call
def f2(cls): ...          # correct
```

- Classes: `@validate_call class A1: ...` fails because Pydantic needs to know whether to use `__init__` or `__new__`. Decorate the appropriate method instead (`@validate_call def __init__(self)` or `def __new__(cls)`).
- Callable instances: `validate_call(A1())` fails (the page says this may change). Decorate `__call__` explicitly: `@validate_call def __call__(self): ...`.
- Invalid signature: validating a method without at least one argument (usually `self`), e.g. `def f(): ...` on a class, fails.

## `unpack-typed-dict`

`Unpack` used for `**kwargs` must wrap a `TypedDict` class: `def func(**kwargs: Unpack[int])` fails. Spec reference: PEP 692.

## `overlapping-unpack-typed-dict`

The TypedDict's field names must not overlap other parameters (unless those are positional-only):

```python
class TD(TypedDict):
    a: int

@validate_call
def func(a: int, **kwargs: Unpack[TD]): ...   # error
```

## `invalid-self-type`

`Self` is only allowed to annotate a field of a class (`BaseModel`, `NamedTuple`, `TypedDict` or dataclass subclasses). `@validate_call def func(self: Self)` fails. The page notes that `def func(self, arg: Self)` as a `validate_call` method on a `BaseModel` also raises this error even though it type-checks, and that this may be supported in the future.

## Checked

Checked 2026-11-07. Compared every claim with the usage errors page (errors/usage_errors.md): supported callables, decorator ordering for `@classmethod` / `@staticmethod` / `@property`, classes, callable instances, invalid signature, `unpack-typed-dict`, `overlapping-unpack-typed-dict` and `invalid-self-type` including the `Self` method note. All confirmed; nothing removed.

Method: documentation only; no commands were run.
