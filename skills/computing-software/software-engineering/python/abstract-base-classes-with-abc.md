---
id: computing-software.software-engineering.python.abstract-base-classes-with-abc
name: abstract-base-classes-with-abc
category: computing-software
field: software-engineering
product: python
tags: [python, py-classes, abstract-base-classes, abc, abstractmethod, register, interfaces]
level: practitioner
status: docs-checked
description: "Define interfaces with abc.ABC and @abstractmethod, abstract properties, virtual subclass registration and __subclasshook__, and avoid metaclass conflicts."
sources: ["https://docs.python.org/3/library/abc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Abstract base classes with abc

**Goal:** enforce that subclasses implement an interface, at instantiation time.

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def read(self, key: str) -> bytes: ...

    @property
    @abstractmethod
    def name(self) -> str: ...          # @property outermost, @abstractmethod innermost

    def exists(self, key):              # concrete method shared by all
        try: self.read(key); return True
        except KeyError: return False

class Mem(Storage):
    name = "mem"
    def read(self, key): return b""

Storage()      # TypeError: abstract class cannot be instantiated until all abstract methods are overridden
```

## Features
- `Storage.register(Foreign)` registers a "virtual subclass": `issubclass`/`isinstance` become true without inheritance. `abstractmethod` only affects regular subclasses, not registered virtual ones. Since 3.3 `register` returns the subclass, so it works as a class decorator.
- `__subclasshook__` (a class method) customizes `issubclass` without calling `register` for every class; it returns `True`, `False` or `NotImplemented`.
- `inspect.isabstract(cls)` returns True for an abstract base class.
- Abstract classmethods/staticmethods/properties: `abstractmethod` must be the innermost decorator, with `@classmethod`, `@staticmethod` or `@property` above it.


## Gotchas
- A class whose metaclass derives from `ABCMeta` cannot be instantiated unless all its abstract methods and properties are overridden.
- Abstract methods can be called with the normal `super()` mechanisms, so they may have a body.
- The type of `ABC` is still `ABCMeta`, so inheriting from `ABC` alongside classes with a different metaclass may lead to metaclass conflicts; passing `metaclass=ABCMeta` directly is the documented alternative to inheriting from `ABC`.
- To add or change abstract methods after class creation, use `abc.update_abstractmethods`.

## Verify
- [ ] A test instantiates an incomplete subclass and asserts `TypeError`.
- [ ] Registered virtual subclasses are checked by hand, since `register` does not verify methods.

## Checked

- 2026-11-03: checked against the CPython docs `library/abc.rst` (`ABC`, `ABCMeta.register`, `__subclasshook__`, `abstractmethod` innermost rule, virtual subclasses, `update_abstractmethods`) and `library/inspect.rst` (`isabstract`).
- Removed: the exact `Can't instantiate abstract class` message, `__abstractmethods__`, the Protocol comparison, Django, isinstance speed and mypy/pyright claims (not in these pages).

Method: documentation only; no commands were run.
