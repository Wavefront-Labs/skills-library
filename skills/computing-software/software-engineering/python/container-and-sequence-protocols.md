---
id: computing-software.software-engineering.python.container-and-sequence-protocols
name: container-and-sequence-protocols
category: computing-software
field: software-engineering
product: python
tags: [python, py-data-model, container-protocol, getitem, len, contains, collections-abc, slicing]
level: practitioner
status: docs-checked
description: "Make a custom class behave as a sequence or mapping by implementing __len__, __getitem__, __contains__ and slice support, or by subclassing collections.abc mixins."
sources: ["https://docs.python.org/3/reference/datamodel.html#emulating-container-types", "https://docs.python.org/3/library/collections.abc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container and sequence protocols

**Goal:** a class that works with `len`, indexing, slicing, `in`, `for`, `reversed`.

## Minimum for a read-only sequence
```python
from collections.abc import Sequence

class Ring(Sequence):
    def __init__(self, items): self._items = list(items)
    def __len__(self): return len(self._items)
    def __getitem__(self, i):
        if isinstance(i, slice):
            return type(self)(self._items[i])       # slices return the same type
        return self._items[i]                       # raises IndexError for you
```
`Sequence` needs `__getitem__` and `__len__` and supplies the mixins `__contains__`, `__iter__`, `__reversed__`, `index` and `count`. `Mapping` needs `__getitem__`, `__iter__`, `__len__` and supplies `__contains__`, `keys`, `items`, `values`, `get`, `__eq__`, `__ne__`; `MutableMapping` additionally needs `__setitem__` and `__delitem__` and supplies `pop`, `popitem`, `clear`, `update`, `setdefault`. `MutableSequence` needs `__setitem__`, `__delitem__` and `insert` as well.

## Data model rules
- For a sequence the allowable keys are integers `0 <= k < N` or slice objects; slicing goes through `__getitem__` (`a[1:2] = b` becomes `a[slice(1, 2, None)] = b`, missing items filled with `None`). The reference defers negative-index and slice behaviour to the sequence documentation.
- Wrong subscript type: raise `TypeError`. Wrong value: raise `LookupError` or a subclass, `IndexError` for sequences, `KeyError` for mappings. The for-loop iteration protocol relies on `IndexError` to detect the end.
- Both mappings and sequences should implement `__contains__` and `__iter__` for efficiency. For mappings `in` and iteration use the keys.
- Without `__contains__`, `in` tries `__iter__`, then the old sequence iteration protocol via `__getitem__`.
- Without `__reversed__`, `reversed()` falls back to `__len__` and `__getitem__`; provide `__reversed__` only if it is more efficient.
- An object with no `__bool__` whose `__len__` returns zero is false. In CPython the length must be at most `sys.maxsize`.
- `__missing__` is called by `dict.__getitem__` for `dict` subclasses when the key is absent.
- Sequence types should implement concatenation and repetition via `__add__`, `__radd__`, `__iadd__`, `__mul__`, `__rmul__`, `__imul__` and should not define other numeric operators.
- Subscripting a class may call `__class_getitem__` instead of `__getitem__`.

## Verify
- [ ] `list(reversed(x)) == list(x)[::-1]`, `x[1:3]` returns your type, `-1 in x` behaves as intended.
- [ ] `isinstance(x, collections.abc.Sequence)` is true and `len(x)` matches iteration length.

## Checked
Date: 2026-11-03. Confirmed against the data model "Emulating container types" section and the collections.abc abstract-method and mixin table. Removed as not on those pages: tuple subscripts and `operator.index`, claim that subclassing `dict`/`list` bypasses overrides in `update`, `UserDict`/`UserList` advice, O(1) membership remark.
Method: documentation only; no commands were run.
