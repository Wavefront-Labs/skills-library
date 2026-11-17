---
id: computing-software.software-engineering.python.type-aliases-and-newtype
name: type-aliases-and-newtype
category: computing-software
field: software-engineering
product: python
tags: [python, type-alias, python-newtype, type-statement, typealiastype, pep-695, type-hints]
level: practitioner
status: verified
description: "Name complex types with aliases and the 3.12 type statement, and create distinct ID types with NewType: when each is checked, generic aliases, recursion and runtime costs."
sources: ["https://docs.python.org/3/library/typing.html#type-aliases", "https://docs.python.org/3/library/typing.html#newtype", "https://peps.python.org/pep-0695/", "https://typing.python.org/en/latest/spec/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type aliases and NewType

**Goal:** readable signatures for complex types, and IDs that cannot be mixed up
(`UserId` passed where `OrderId` is expected).

## Aliases: another name for the same type
```python
# 3.12+
type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None   # recursive OK
type Pair[T] = tuple[T, T]                                                    # generic alias
# older
from typing import TypeAlias
Headers: TypeAlias = dict[str, list[str]]
```
An alias is fully interchangeable with its target: `Headers` and `dict[str, list[str]]`
are the same type to the checker.

`type` statement aliases are lazily evaluated `TypeAliasType` objects: forward and recursive
references work without quotes, but they are not the target class at runtime -
`isinstance(x, JSON)` fails and `JSON.__value__` gives the target.

## NewType: a distinct subtype, zero runtime cost
```python
from typing import NewType
UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)

def get_user(uid: UserId) -> User: ...
get_user(UserId(42))       # ok
get_user(42)               # checker error: int is not UserId
get_user(OrderId(42))      # checker error
UserId(5) + 1              # int: arithmetic returns the base type
```
At runtime `UserId(42)` returns the plain int `42` (identity function), so there is no
validation and no overhead. Validate at the boundary that constructs it:
```python
def parse_user_id(raw: str) -> UserId:
    v = int(raw)
    if v <= 0: raise ValueError("bad user id")
    return UserId(v)
```
You cannot subclass a NewType or use it with `isinstance`. Need methods or runtime checks?
Use a small frozen dataclass instead.

## Choosing
| Need | Use |
|---|---|
| shorten a long type | alias |
| self-referencing/generic type | `type` statement (3.12) |
| prevent mixing same-shaped values | `NewType` |
| validation + behaviour | frozen dataclass / pydantic model |
| a fixed set of strings | `Literal[...]` or `StrEnum` |

## Verify
- [ ] Swapping two NewType IDs in a call is flagged by mypy/pyright in CI.
- [ ] No `isinstance(x, SomeAlias)` against `type` statement aliases.

## Checked
- mypy 2.4.0 on Python 3.14.0 plus runtime: `type JSON` is a `TypeAliasType` with `__value__` and `isinstance(1, JSON)` raises `TypeError`; generic `type Pair[T]` rejected `(1, 'a')`; `UserId(42)` returns a plain `int`; `get_user(42)` and `get_user(OrderId(42))` were errors; `UserId(5) + 1` reveals `int`; subclassing a NewType raised `TypeError: Cannot subclass an instance of NewType`; `isinstance(1, UserId)` raised `TypeError`. `TypeAlias` (older form) accepted.
