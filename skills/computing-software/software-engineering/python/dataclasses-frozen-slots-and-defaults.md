---
id: computing-software.software-engineering.python.dataclasses-frozen-slots-and-defaults
name: dataclasses-frozen-slots-and-defaults
category: computing-software
field: software-engineering
product: python
tags: [python, python-data-model, dataclasses, python-dataclass, frozen, slots, field-defaults, kw-only]
level: practitioner
status: verified
description: "Model data with dataclasses correctly: mutable default traps, frozen and slots, kw_only, __post_init__ validation, ordering and when attrs or pydantic fit better."
sources:
  - https://docs.python.org/3/library/dataclasses.html
  - https://peps.python.org/pep-0557/
  - https://peps.python.org/pep-0681/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataclasses: frozen, slots and field defaults

**Goal:** concise value types with correct equality, hashing, defaults and memory use.

## 1. Baseline
```python
from dataclasses import dataclass, field, KW_ONLY

@dataclass(frozen=True, slots=True, kw_only=True)
class Money:
    amount: int            # minor units
    currency: str = "EUR"

@dataclass(slots=True)
class Order:
    id: str
    lines: list["Line"] = field(default_factory=list)   # never `= []`
    _: KW_ONLY
    note: str | None = None
    created: datetime = field(default_factory=lambda: datetime.now(UTC))
```
- `default_factory` for every mutable default; `= []` raises `ValueError: mutable default` (for list/dict/set) but other mutables (custom objects) are silently shared.
- `kw_only=True` (3.10+) avoids "non-default argument follows default argument" and makes call sites readable.
- `slots=True` (3.10+): smaller instances, faster attribute access, typo'd attribute assignment raises `AttributeError` on a regular dataclass. On `frozen=True, slots=True` the same typo raised a confusing `TypeError: super(type, obj): ...` on both 3.10 and 3.14.0.

## 2. Equality, hashing, ordering
| Options | `__eq__` | `__hash__` |
|---|---|---|
| default (`eq=True`) | field-wise | set to `None` (unhashable) |
| `frozen=True` | field-wise | generated from fields |
| `unsafe_hash=True` | field-wise | generated even though mutable (avoid) |
`order=True` adds `<`, `<=` etc. comparing fields as a tuple in declaration order. Exclude fields with `field(compare=False)` / `hash=False` / `repr=False` (secrets).

## 3. Validation and derived fields
```python
@dataclass(frozen=True, slots=True)
class Range:
    lo: int
    hi: int
    width: int = field(init=False)
    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError(f"lo {self.lo} > hi {self.hi}")
        object.__setattr__(self, "width", self.hi - self.lo)   # frozen: bypass the guard
```

## 4. Useful helpers
```python
from dataclasses import replace, asdict, astuple, fields
r2 = replace(r, hi=10)          # copy with changes; reruns __init__/__post_init__
asdict(order)                   # deep-copies recursively; slow for big graphs
[f.name for f in fields(Order)]
```

## When to use something else
- Parsing untrusted input (JSON, env): pydantic or msgspec validate and coerce; dataclasses do no type checking at runtime.
- Need converters/validators per field: attrs (`@define`, `field(converter=...)`).
- Tuple-like immutable record with positional unpacking: `typing.NamedTuple`.

## Gotchas
- `frozen` is shallow: a frozen dataclass holding a list is still mutable through the list, and then hashing is unsafe.
- `slots=True` replaces the class with a new one, so zero-argument `super()` in methods of that class can fail on older Pythons (fixed in 3.14); use `super(Cls, self)` or test on your minimum version.
- `ClassVar[...]` annotations are not fields; annotations without a type (`x = 1`) are not fields either.
- `asdict` follows nested dataclasses, lists, tuples and dicts but not arbitrary objects.

## Verify
- `hash(Money(amount=1))` works, `Order("a").lines is not Order("b").lines`, and `Order("a").nmae = 1` raises `AttributeError` with slots.

## Checked
- Python 3.14.0 (3.10.11 for the super and typo rows): `kw_only` rejects positional args, `KW_ONLY` makes later fields keyword-only, frozen assignment raises `FrozenInstanceError`, `= []`, `{}` and `set()` defaults raise `ValueError: mutable default`, a custom-object default is silently shared, non-default after default raises `TypeError`, `eq=True` leaves the class unhashable while `frozen=True` and `unsafe_hash=True` hash, `order=True` with `compare=False`/`repr=False` fields, the `Range` `__post_init__` with `object.__setattr__`, `replace()` rerunning `__post_init__`, `asdict` converting nested dataclasses and copying lists/objects, frozen shallowness (list mutable, hash fails), `ClassVar` and unannotated attributes not being fields; zero-argument `super()` with `slots=True` fails on 3.10 and works on 3.14 (changelog gh-90562). The attrs, pydantic and msgspec guidance is not re-tested.
