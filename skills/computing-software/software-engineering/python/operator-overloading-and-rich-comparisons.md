---
id: computing-software.software-engineering.python.operator-overloading-and-rich-comparisons
name: operator-overloading-and-rich-comparisons
category: computing-software
field: software-engineering
product: python
tags: [python, operator-overloading, total-ordering, rich-comparisons, dunder-methods, notimplemented, hash-eq-contract]
level: practitioner
status: verified
description: "Implement __eq__/__hash__/__lt__ and arithmetic dunders correctly: return NotImplemented, reflected and in-place operators, total_ordering, and the hash/eq contract."
sources: ["https://docs.python.org/3/reference/datamodel.html#object.__lt__", "https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types", "https://docs.python.org/3/library/functools.html#functools.total_ordering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator overloading and rich comparisons

**Goal:** value types (Money, Vector, Version) that compare, hash and do arithmetic
correctly with themselves and refuse silently-wrong mixes.

## Equality and hashing
```python
class Money:
    __slots__ = ("amount", "currency")
    def __init__(self, amount: int, currency: str):
        self.amount, self.currency = amount, currency

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented          # NOT False: lets the other operand try
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __hash__(self):
        return hash((self.amount, self.currency))
```
Contract: `a == b` implies `hash(a) == hash(b)`. Defining `__eq__` sets `__hash__ = None`
(unhashable) unless you define `__hash__` too. Only hash immutable state; a mutable object
whose hash changes gets lost in sets/dicts.

`NotImplemented` vs `False`: returning `NotImplemented` makes Python try the reflected
operation on the other object, then fall back to identity for `==`. Raising
`NotImplementedError` here is a bug.

## Ordering
```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, *parts): self.parts = parts
    def __eq__(self, o): return self.parts == o.parts if isinstance(o, Version) else NotImplemented
    def __lt__(self, o): return self.parts < o.parts if isinstance(o, Version) else NotImplemented
```
`total_ordering` derives `<=, >, >=` (slower than writing all four; fine for most code).
Or use `@dataclass(order=True, frozen=True)` which compares fields as tuples in order.

## Arithmetic
```python
    def __add__(self, other):
        if not isinstance(other, Money): return NotImplemented
        if other.currency != self.currency: raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)
    __radd__ = __add__              # reflected form for other + m when other's type returns NotImplemented
    # note: this does NOT make 0 + m work (it returns NotImplemented for ints); see sum() below
    def __mul__(self, k):
        return Money(self.amount * k, self.currency) if isinstance(k, int) else NotImplemented
    __rmul__ = __mul__
```
- `a + b` tries `a.__add__(b)`, then `b.__radd__(a)` if the first returned NotImplemented
  (or first if b's type is a subclass of a's).
- `+=` calls `__iadd__` if defined (mutate in place, return self), else falls back to `__add__`.
  Immutable types should NOT define `__iadd__`.
- `sum()` starts from `0`, so `sum([m1, m2])` raises `TypeError` unless `__radd__` handles `0` explicitly;
  simply pass `start=Money(0, "EUR")` (works with `__add__` alone).

## Other useful dunders
`__bool__` (truthiness), `__len__`, `__contains__`, `__getitem__`, `__matmul__` (`@`),
`__neg__`, `__abs__`, `__format__` for f-string specs, `__repr__` for debugging.

## Verify
- [ ] `Money(1, "EUR") == 1` is False (not an exception) and `{m1, m2}` dedupes equal values.
- [ ] Tests cover mixed-type operations returning TypeError, not wrong results.

## Checked
- Python 3.14.0: ran every snippet: `Money(1,'EUR') == 1` is False and the set dedupes; `sum([...])` raised `TypeError` with `__radd__ = __add__` (so the old comment was wrong) while `start=Money(0,'EUR')` worked; mixed `+` gave `TypeError`; a class defining only `__eq__` has `__hash__ = None`; `total_ordering` supplied `<=, >, >=` and returned TypeError for foreign types (`a<=b` 0.088 s vs 0.051 s for a hand-written `__le__` per 1e6); reflected-operand order including the subclass-first rule; `__iadd__` used for `+=`; `dataclass(order=True, frozen=True)` compares as tuples.
