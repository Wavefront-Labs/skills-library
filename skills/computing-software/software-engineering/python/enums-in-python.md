---
id: computing-software.software-engineering.python.enums-in-python
name: enums-in-python
category: computing-software
field: software-engineering
product: python
tags: [python, python-enum, strenum, intflag, enum-auto, enum-serialization, python-data-model]
level: practitioner
status: verified
description: "Model fixed choices with enum: Enum vs StrEnum/IntEnum vs Flag, auto(), unique, value lookup, methods on members, JSON/DB serialisation and pattern matching."
sources: ["https://docs.python.org/3/library/enum.html", "https://docs.python.org/3/howto/enum.html", "https://docs.python.org/3/library/enum.html#enum.StrEnum"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums in Python

**Goal:** replace magic strings and ints with enum members that are type-checkable,
serialise predictably and fail fast on bad values.

## Choosing the base
| Base | Members compare equal to | Use for |
|---|---|---|
| `Enum` | only themselves | default; safest |
| `StrEnum` (3.11) | their string value | JSON/HTTP/DB values, `f"{x}"` gives the value |
| `IntEnum` | ints | C/protocol codes, legacy int APIs |
| `Flag` / `IntFlag` | bit combinations | permissions, option sets (`Perm.R | Perm.W`) |

```python
from enum import Enum, StrEnum, Flag, auto, unique

@unique
class Status(StrEnum):
    PENDING = auto()      # StrEnum auto() -> lowercase name: "pending"
    PAID = auto()
    REFUNDED = auto()

class Perm(Flag):
    R = auto(); W = auto(); X = auto()
    RW = R | W
```

## Lookup and iteration
```python
Status("paid")            # by value -> Status.PAID; ValueError on unknown
Status["PAID"]            # by name
list(Status)              # definition order (aliases excluded)
Status.PAID.name, Status.PAID.value
Perm.R in (Perm.R | Perm.W)     # True
```
Handle unknown external values explicitly: catch `ValueError`, or define `_missing_`:
```python
class Status(StrEnum):
    ...
    @classmethod
    def _missing_(cls, value):
        return cls.PENDING if value == "new" else None    # None -> ValueError
```

## Behaviour on members
```python
class Plan(Enum):
    FREE = (0, 1)
    PRO = (20, 10)
    def __init__(self, price, seats): self.price, self.seats = price, seats
    @property
    def is_paid(self): return self.price > 0
```

## Serialisation
- `json.dumps(Status.PAID)` works for StrEnum/IntEnum (they are str/int); plain `Enum`
  raises TypeError - use `.value` or a custom encoder.
- pydantic and SQLAlchemy (`Enum(Status, values_callable=lambda e: [m.value for m in e])`)
  store values; by default SQLAlchemy stores *names*, a common surprise.
- Renaming a member changes its name, not value; persist values, never names.

## Matching
```python
match status:
    case Status.PAID | Status.REFUNDED: ...
    case Status.PENDING: ...
```
Dotted names are value patterns (compared with `==`); a bare name would bind a variable.

## Gotchas
- Comparing `Status.PAID == "paid"` is True only for StrEnum; for `Enum` it is False silently.
- `IntEnum` members sort and do arithmetic like ints, leaking meaning; prefer `Enum` unless needed.
- Type checkers treat enums as exhaustive in `match`/`if` chains: use `assert_never` in the default branch.

## Verify
- [ ] Every external value path handles unknown values (ValueError or `_missing_`).
- [ ] Persistence stores `.value`; tests round-trip each member.

## Checked
- Python 3.14.0 (plus SQLAlchemy 2.1.5 on SQLite): `StrEnum` `auto()` gives lowercase names; lookup by value and name; `ValueError` on unknown values and from `_missing_` returning `None`; `StrEnum == str`, `IntEnum == int`, plain `Enum` not equal to its value; `f"{Status.PAID}"` gives the value; `Flag` membership and `RW = R | W`; `list(Flag)` shows only the single-bit members; tuple-valued members with `__init__` and a property; `json.dumps` works for `StrEnum`/`IntEnum` and raises `TypeError` for plain `Enum`; `@unique` rejects duplicate values and plain aliases are left out of `list()`; `SAEnum(Status)` stored `PAID` while `values_callable` stored `paid`. The 3.11 notes add `StrEnum`. `match` with dotted `Status.PAID | Status.REFUNDED` patterns matches members and the plain string (StrEnum), while a bare name binds anything; `IntEnum` sorts and adds like ints.
