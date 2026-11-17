---
id: computing-software.software-engineering.python.descriptors-and-properties
name: descriptors-and-properties
category: computing-software
field: software-engineering
product: python
tags: [python, python-data-model, descriptors, python-property, cached-property, set-name, dunder-methods]
level: practitioner
status: verified
description: "Use properties, cached_property and custom descriptors (__get__/__set__/__set_name__) for validated, computed and lazily loaded attributes, and know lookup precedence."
sources:
  - https://docs.python.org/3/howto/descriptor.html
  - https://docs.python.org/3/reference/datamodel.html#implementing-descriptors
  - https://docs.python.org/3/library/functools.html#functools.cached_property
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Descriptors and properties

**Goal:** attribute access that validates, computes or caches, implemented once and reused across classes.

## 1. property for one attribute
```python
class Account:
    def __init__(self, balance: int):
        self.balance = balance          # goes through the setter
    @property
    def balance(self) -> int:
        return self._balance
    @balance.setter
    def balance(self, value: int) -> None:
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value
```
Start with a plain attribute; switch to a property later without changing callers. That is why Python does not need getters/setters.

## 2. cached_property for expensive, immutable derived values
```python
from functools import cached_property
class Report:
    @cached_property
    def rows(self) -> list[Row]:
        return load_rows(self.path)
# invalidate: del report.rows
```
Needs an instance `__dict__` (fails with `__slots__` unless `__dict__` is a slot). Not thread-locked since 3.12; wrap with a lock if concurrent first access matters.

## 3. Custom descriptor for reusable validation
```python
class Positive:
    def __set_name__(self, owner, name):
        self.private = "_" + name
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                      # accessed on the class
        return getattr(obj, self.private)
    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.private[1:]} must be > 0")
        setattr(obj, self.private, value)

class Order:
    qty = Positive()
    price = Positive()
```

## 4. Lookup precedence (instance attribute access)
1. **Data descriptors** on the type (define `__set__` or `__delete__`): property, slots, the class above.
2. Instance `__dict__`.
3. **Non-data descriptors** (only `__get__`): functions (that is how methods bind), `cached_property`, `classmethod`, `staticmethod`.
4. `__getattr__` if defined, only after normal lookup fails.
This is why `cached_property` works: the first call stores the value in `__dict__`, which then shadows the non-data descriptor.

## Gotchas
- Storing per-instance values on the descriptor itself (`self.value = v`) shares them across all instances; store on `obj`.
- `__getattribute__` overrides run for every access; prefer `__getattr__` for fallbacks.
- Type checkers understand `property` and `cached_property`; for custom descriptors annotate `__get__` with overloads (`obj: None -> Self`, `obj: Owner -> T`).
- `@property` on a classmethod chain stopped working in 3.13 (chained classmethod descriptors were removed); use a metaclass property or plain classmethod.

## Verify
- `Order().qty = -1` raises; `Order.qty` returns the descriptor object; two instances keep independent values.

## Checked
- Python 3.14.0: ran all snippets: `cached_property` stores into `__dict__` and `del` invalidates; it raises `TypeError` on a `__slots__` class without `__dict__`; `__slots__` entries are data descriptors (`member_descriptor` has `__set__`), `cached_property` has no `__set__` and its source has no lock; the `Positive` descriptor kept per-instance values, rejected -1, and returned itself on the class; `__getattr__` fallback worked; stacking `classmethod` on `property` no longer returns the value. Lock removal in 3.12 (functools docs) and chained-classmethod removal in 3.13 (What's New in 3.13) read from docs.python.org.
