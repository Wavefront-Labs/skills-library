---
id: computing-software.software-engineering.python.self-final-classvar-and-override
name: self-final-classvar-and-override
category: computing-software
field: software-engineering
product: python
tags: [python, typing-self, typing-final, typing-override, classvar, type-hints, fluent-interfaces]
level: practitioner
status: verified
description: "Type class APIs precisely with typing.Self for fluent/alternate constructors, Final for constants, ClassVar for class attributes and @override to catch broken overrides."
sources: ["https://docs.python.org/3/library/typing.html#typing.Self", "https://peps.python.org/pep-0673/", "https://peps.python.org/pep-0591/", "https://peps.python.org/pep-0698/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self, Final, ClassVar and @override

**Goal:** class-level typing that survives subclassing and refactors.

## Self (3.11, `typing_extensions` before)
```python
from typing import Self

class QueryBuilder:
    def where(self, cond: str) -> Self:
        self._conds.append(cond)
        return self
    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return cls(**d)

class UserQuery(QueryBuilder): ...
UserQuery().where("x").where("y")      # still UserQuery, not QueryBuilder
```
Replaces the old `T = TypeVar("T", bound="QueryBuilder")` boilerplate. Not allowed in
staticmethods (mypy: "Static methods cannot use Self type").

## Final
```python
from typing import Final
MAX_RETRIES: Final = 5          # checker errors on reassignment anywhere
class Config:
    TIMEOUT: Final[float] = 2.5   # also cannot be overridden in subclasses

from typing import final
@final
class Token: ...                 # cannot be subclassed
class Base:
    @final
    def run(self) -> None: ...   # cannot be overridden
```
Purely static: nothing stops reassignment at runtime. `Final` names are treated as
literal types (`MAX_RETRIES` is `Literal[5]`).

## ClassVar
```python
from typing import ClassVar
class Model:
    registry: ClassVar[dict[str, type["Model"]]] = {}
    name: str                     # instance attribute
```
In dataclasses, `ClassVar` fields are excluded from `__init__` and fields; without it a
mutable class-level default raises `ValueError: mutable default ... use default_factory`.

## @override (3.12, `typing_extensions` before)
```python
from typing import override
class Base:
    def handle(self, event: str) -> None: ...
class Child(Base):
    @override
    def handle(self, event: str) -> None: ...    # error if Base.handle is renamed or removed
```
Enable strict enforcement: pyright `reportImplicitOverride`, mypy
`--enable-error-code explicit-override` - then every override must be marked.

## Verify
- [ ] `reveal_type(Sub().fluent_method())` shows the subclass.
- [ ] Renaming a base method makes the checker flag every `@override` that no longer overrides.

## Checked
- mypy 2.4.0 and pyright 1.1.414 on Python 3.14.0: `Self` kept `UserQuery` through a fluent method; staticmethod `Self` rejected; `Final` reassignment, `Final[float]` override in a subclass, `@final` class subclassing and `@final` method override were errors; `MAX_RETRIES` reveals `Literal[5]?`; `@override` on a missing base method errored in both; mypy `--enable-error-code explicit-override` and pyright `reportImplicitOverride` flagged unmarked overrides; `ClassVar` was excluded from dataclass `fields()` and `__init__`; mutable default raised `ValueError: mutable default <class 'list'> for field a is not allowed: use default_factory`; `@override` sets `__override__` at runtime.
