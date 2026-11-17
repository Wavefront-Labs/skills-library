---
id: computing-software.software-engineering.python.slots-and-instance-memory
name: slots-and-instance-memory
category: computing-software
field: software-engineering
product: python
tags: [python, python-slots, python-data-model, memory-footprint, dataclass-slots, weakref]
level: advanced
status: verified
description: "Use __slots__ to cut per-instance memory and block typo attributes: inheritance rules, __dict__/__weakref__ slots, dataclass(slots=True) and when slots get in the way."
sources: ["https://docs.python.org/3/reference/datamodel.html#slots", "https://docs.python.org/3/howto/descriptor.html#member-objects-and-slots", "https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# __slots__ and instance memory

**Goal:** shrink millions of small objects and make attribute typos fail loudly,
without breaking pickling, weakrefs or subclasses.

## What slots do
```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
p.z = 3        # AttributeError: 'Point' object has no attribute 'z' and no __dict__ for setting new attributes (3.14)
```
Each name becomes a member descriptor on the class with a fixed offset; instances get no
`__dict__`. Saving: on 3.14.0 a two-attribute instance took about 88 bytes slotted vs 128 bytes with a
`__dict__` (tracemalloc, 1M instances); older CPythons without inline values save more.
Attribute access was not faster in a `timeit` check (about 10 ns either way).

Measure, do not guess:
```python
import tracemalloc; tracemalloc.start()
pts = [Point(i, i) for i in range(1_000_000)]
print(tracemalloc.get_traced_memory())
```

## Rules that bite
- **Every class in the MRO must define `__slots__`**, or instances get a `__dict__` anyway
  (from the slot-less class) and the saving vanishes. Subclasses declare only new names:
  `class Point3(Point): __slots__ = ("z",)`.
- Repeating a parent's slot name wastes space and hides the parent descriptor.
- No `__weakref__` by default: `weakref.ref(p)` fails. Add `"__weakref__"` to slots if needed.
- Add `"__dict__"` to slots to allow dynamic attributes too (rarely sensible).
- Class attributes cannot double as defaults for slotted names (`ValueError: 'x' in
  __slots__ conflicts with class variable`). Set defaults in `__init__`.
- Multiple inheritance from two classes with non-empty slots raises
  `TypeError: multiple bases have instance lay-out conflict`. Use empty `__slots__ = ()`
  in mixins.
- `functools.cached_property` needs `__dict__`; it fails on slotted classes.
- Pickling works with protocol 2+ (default); old custom `__getstate__` code may assume `__dict__`.

## dataclasses
```python
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Point:
    x: float
    y: float = 0.0     # defaults fine here; dataclass handles them
```
`slots=True` (3.10+) creates a new class with `__slots__`; `weakref_slot=True` (3.11)
adds `__weakref__`. Because the decorator recreates the class, zero-arg `super()` in its
methods raised `TypeError: super(type, obj): obj must be an instance or subtype of type` on 3.10 (works on 3.14.0); use explicit `super(Point, self)` if
you hit it.

## When not to bother
Few instances, classes needing dynamic attributes, or heavy use of mixins from libraries
you do not control.

## Verify
- [ ] `hasattr(obj, "__dict__")` is False for slotted instances (proves the MRO is fully slotted).
- [ ] Memory measured before/after with tracemalloc on realistic counts.

## Checked
- Python 3.14.0 (plus 3.10 for the super() case): ran all snippets and error messages (no attribute, class variable conflict, "multiple bases have instance lay-out conflict", weakref failure, empty-slot mixins, subclass without slots regains `__dict__`); memory 88 vs 128 MB per million instances with tracemalloc; pickling worked (default protocol 5); `dataclass(slots=True, frozen=True)` and `weakref_slot=True` worked on 3.14 while 3.10 rejected `weakref_slot`; zero-arg `super()` with `slots=True` failed on 3.10 only.
