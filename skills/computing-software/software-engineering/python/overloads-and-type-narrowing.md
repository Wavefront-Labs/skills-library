---
id: computing-software.software-engineering.python.overloads-and-type-narrowing
name: overloads-and-type-narrowing
category: computing-software
field: software-engineering
product: python
tags: [python, python-typing, typing-overload, typeguard, typeis, type-narrowing, assert-never, exhaustiveness, cast]
level: advanced
status: verified
description: "Express return types that depend on arguments with @overload, write custom narrowing functions with TypeIs/TypeGuard, and enforce exhaustiveness with assert_never."
sources: ["https://typing.python.org/en/latest/spec/overload.html", "https://peps.python.org/pep-0742/", "https://typing.python.org/en/latest/spec/narrowing.html", "https://docs.python.org/3/library/typing.html#typing.assert_never"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overloads, TypeIs/TypeGuard and narrowing

**Goal:** precise types for functions whose return type depends on inputs, and
checker-understood validation helpers.

## @overload
```python
from typing import overload, Literal

@overload
def fetch(id: int, *, raw: Literal[True]) -> bytes: ...
@overload
def fetch(id: int, *, raw: Literal[False] = ...) -> User: ...
def fetch(id: int, *, raw: bool = False) -> bytes | User:   # implementation, not visible to callers
    ...
```
- Overload signatures have `...` bodies; the implementation must accept every overload.
- Order matters: the checker picks the FIRST match; put narrow cases first.
- If one return type works (`T | None`), skip overloads; they add maintenance.

## Built-in narrowing the checker understands
`isinstance`, `is None`, `==` against literals, `in` with literal tuples, `callable()`,
truthiness, `len()` on tuples, and `match` statements.

## Custom narrowing functions
```python
from typing import TypeIs, TypeGuard   # TypeIs: 3.13+ or typing_extensions

def is_int(v: object) -> TypeIs[int]:
    return isinstance(v, int)
def is_str_list(xs: list[object]) -> TypeGuard[list[str]]:   # TypeIs here is rejected: list[str] is not a
    return all(isinstance(x, str) for x in xs)               # subtype of list[object] (list is invariant)
```
- **TypeIs** (PEP 742) narrows in both branches (in `else` it removes the type) and the
  narrowed type must be a subtype of the input. Prefer it.
- **TypeGuard** only narrows the `if` branch and allows non-subtype results
  (e.g. `list[object]` -> `list[str]`), but nothing in `else`.
- The function body is NOT verified to match its claim; a wrong guard lies to the checker.

## Exhaustiveness
```python
from typing import assert_never
def area(s: Circle | Square) -> float:
    match s:
        case Circle(): return pi * s.r ** 2
        case Square(): return s.side ** 2
        case _: assert_never(s)     # error if a new variant is added and not handled
```

## cast and ignores
`typing.cast(T, x)` asserts without checking; use sparingly with a comment. Prefer an
`assert isinstance(x, T)` which also checks at runtime.

## Verify
- [ ] `reveal_type` on each overload call site shows the expected return type.
- [ ] Adding a new union member makes the `assert_never` function fail type checking.

## Checked
- mypy (current pip release) on Python 3.14.0: overload calls reveal `User` and `bytes`; the old `TypeIs[list[str]]` example was rejected ("Narrowed type is not a subtype of input type"), `TypeGuard[list[str]]` accepted; `TypeIs[int]` narrowed both branches (`int` / `str`) while `TypeGuard[int]` left `int | str` in else; `assert_never` flagged an unhandled `Tri`; `==` literal, `len()` on tuple unions and `in` narrowing worked. `typing.TypeIs` imports on 3.14; the 3.13 introduction was not re-read from docs.
