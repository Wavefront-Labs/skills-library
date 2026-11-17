---
id: computing-software.software-engineering.python.metaclasses-and-init-subclass
name: metaclasses-and-init-subclass
category: computing-software
field: software-engineering
product: python
tags: [python, python-data-model, metaclasses, init-subclass, class-registration, set-name, dunder-methods]
level: practitioner
status: verified
description: "Customise class creation with __init_subclass__ and __set_name__ first, metaclasses only when needed: plugin registries, validation of subclasses, and conflicts."
sources:
  - https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
  - https://peps.python.org/pep-0487/
  - https://docs.python.org/3/reference/datamodel.html#metaclasses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metaclasses and __init_subclass__

**Goal:** run code when subclasses are defined (registration, validation, defaults) with the least magic possible.

## 1. __init_subclass__ covers most needs
```python
class Handler:
    registry: dict[str, type["Handler"]] = {}

    def __init_subclass__(cls, /, kind: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if kind is None:
            raise TypeError(f"{cls.__name__} must declare kind=")
        if kind in Handler.registry:
            raise TypeError(f"duplicate handler kind {kind!r}")
        Handler.registry[kind] = cls

class CsvHandler(Handler, kind="csv"): ...
class JsonHandler(Handler, kind="json"): ...
Handler.registry["csv"]   # CsvHandler
```
Class keyword arguments go to `__init_subclass__`. Always call `super().__init_subclass__(**kwargs)` for cooperative inheritance.

## 2. __set_name__ for attribute-aware descriptors
Called on each class attribute object when the class is created, with `(owner, name)`. Lets fields know their own names (ORM columns, validators) without a metaclass.

## 3. When a metaclass is actually needed
- Changing the namespace before the body runs (`__prepare__`, e.g. ordered or duplicate-detecting dict).
- Customising behaviour of the **class object** itself: `__call__` (instance caching/singletons), `__getitem__` on the class, `__instancecheck__`, operators on classes (Enum does this).
```python
class Singleton(type):
    _instances = {}
    def __call__(cls, *a, **kw):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*a, **kw)
        return cls._instances[cls]
class Config(metaclass=Singleton): ...
```
(A module-level instance is usually a better singleton.)

## 4. Order of class creation
1. Metaclass determined (most derived of bases' metaclasses).
2. `__prepare__` creates the namespace; body executes.
3. `type.__new__` builds the class, calling `__set_name__` on attributes, then the parent's `__init_subclass__`.
4. Class decorators run last (another non-metaclass option: `@register` decorator).

## Gotchas
- Metaclass conflict: `TypeError: metaclass conflict` when combining bases with unrelated metaclasses (e.g. ABCMeta and a Django model). Derive a combined metaclass or avoid one.
- `__init_subclass__` is not called for the class that defines it, only its subclasses.
- Registration on import means modules must be imported for registration to happen; use entry points for real plugins.
- Type checkers understand `__init_subclass__` keywords; most cannot see through custom metaclass `__call__`.

## Verify
- Defining a subclass without `kind=` raises `TypeError` at import, and `Handler.registry` lists every concrete handler after importing the package.

## Checked
- Python 3.14.0: registry example worked and both error paths raised the quoted `TypeError`s; recorded creation order was `__prepare__`, class body, metaclass `__new__`, `__set_name__`, `__init_subclass__`, class decorator; ABCMeta plus an unrelated metaclass raised "metaclass conflict"; the `Singleton.__call__` metaclass returned one instance. Django/ORM mention not run.
