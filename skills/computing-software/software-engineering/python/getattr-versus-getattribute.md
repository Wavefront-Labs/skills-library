---
id: computing-software.software-engineering.python.getattr-versus-getattribute
name: getattr-versus-getattribute
category: computing-software
field: software-engineering
product: python
tags: [python, py-data-model, getattr-getattribute, attribute-access, proxies, delegation, dunder-methods]
level: practitioner
status: docs-checked
description: "Choose between __getattr__ (fallback) and __getattribute__ (every access) and __setattr__ for proxies and lazy attributes without infinite recursion."
sources: ["https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# __getattr__ versus __getattribute__

**Goal:** customise attribute access with the narrowest hook that works.

| Hook | Called | Use for |
|---|---|---|
| `__getattribute__(self, name)` | unconditionally, for every instance attribute access | instrumentation, total control (rare) |
| `__getattr__(self, name)` | only when default access failed with `AttributeError` | lazy/computed attrs, delegation |
| `__setattr__` / `__delattr__` | every assignment/deletion, instead of the normal mechanism | validation, read-only objects |

```python
class Proxy:
    def __init__(self, target):
        object.__setattr__(self, "_target", target)   # bypass our own __setattr__
    def __getattr__(self, name):                      # only for names not found normally
        return getattr(self._target, name)
    def __setattr__(self, name, value):
        setattr(self._target, name, value)

class Traced:
    def __getattribute__(self, name):
        print("get", name)
        return super().__getattribute__(name)         # never self.x here: recursion
```

## Gotchas
- Inside `__getattribute__`, always call the base class method (for example `object.__getattribute__(self, name)`) to reach attributes you need; `self.attr` recurses forever.
- `__getattr__` should return the value or raise `AttributeError`; the class `object` does not define it.
- If `__getattribute__` is defined and raises `AttributeError`, `__getattr__` is then called; otherwise it is not.
- Implicit special-method lookup (`len(x)`, `x + y`) may bypass `__getattribute__` (and `__getattr__`) and read the type, so a proxy must define those dunders on the class.
- For one computed attribute prefer a `property`.

## Verify
- [ ] `hasattr(obj, "missing")` is `False`, not an exception.
- [ ] A unit test covers an attribute named like an instance attribute set in `__init__` before `_target` exists.

## Checked

- 2026-11-03: checked against the CPython docs `reference/datamodel.rst` (customizing attribute access: `__getattr__`, `__getattribute__`, `__setattr__`, special method lookup).
- Removed: the claims about `copy`/`pickle` probing dunder names, the `__deepcopy__` guard recipe and `functools.cached_property`.

Method: documentation only; no commands were run.
