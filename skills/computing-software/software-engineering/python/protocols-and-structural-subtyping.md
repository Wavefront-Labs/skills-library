---
id: computing-software.software-engineering.python.protocols-and-structural-subtyping
name: protocols-and-structural-subtyping
category: computing-software
field: software-engineering
product: python
tags: [python, python-typing, typing-protocol, structural-subtyping, duck-typing, runtime-checkable, abc, dependency-inversion]
level: practitioner
status: verified
description: "Type duck-typed Python with typing.Protocol: defining small protocols, callback protocols, runtime_checkable limits, and Protocol vs ABC choices."
sources: ["https://typing.python.org/en/latest/spec/protocol.html", "https://peps.python.org/pep-0544/", "https://mypy.readthedocs.io/en/stable/protocols.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocols and structural subtyping

**Goal:** describe "anything with a `.read()` method" in types without forcing callers
to inherit from your base class.

## Defining and using a protocol
```python
from typing import Protocol

class SupportsRead(Protocol):
    def read(self, n: int = -1, /) -> bytes: ...

def checksum(src: SupportsRead) -> str:
    return hashlib.sha256(src.read()).hexdigest()

checksum(open("f", "rb"))     # OK: BufferedReader has a compatible read
checksum(io.BytesIO(b"x"))    # OK, no inheritance needed
```
A class matches if it has every member with compatible signatures. The checker
verifies; nothing happens at runtime.

## Rules of thumb
- Keep protocols small (1-3 members) and define them where they are CONSUMED, like Go
  interfaces. Many tiny protocols beat one god-interface.
- Attributes: `name: str` in a protocol requires a settable attribute; use a read-only
  property (`@property def name(self) -> str: ...`) if implementers may use properties.
- Callback protocols express callables with keyword args or overloads that
  `Callable[...]` cannot:
  ```python
  class Handler(Protocol):
      def __call__(self, event: Event, *, retry: bool = False) -> None: ...
  ```
- Generic protocols: `class Repo[T](Protocol): def get(self, id: str) -> T | None: ...`
  (PEP 695 syntax, 3.12+), or `Protocol[T]` on older versions.
- Check stdlib first: `collections.abc` (Iterable, Mapping, Sized) and `typing`
  (SupportsInt, SupportsIndex) already define most common ones.

## runtime_checkable
`@runtime_checkable` allows `isinstance(x, SupportsRead)`, but it only checks that the
attribute NAMES exist, not signatures or types. It is also slow. Use it for coarse
dispatch only.

## Protocol vs ABC
| Need | Use |
|---|---|
| Accept third-party objects you don't control | Protocol |
| Share implementation (mixin methods) | ABC |
| Runtime enforcement that subclasses implement methods | ABC (`@abstractmethod` raises on instantiation) |
| Test doubles without inheritance | Protocol |

An explicit `class FileSource(SupportsRead):` is allowed and makes the checker verify
the implementation at definition time.

## Verify
- [ ] A fake class missing a member is rejected by mypy/pyright where it is passed in.
- [ ] No `isinstance` checks against protocols that rely on signature matching.

## Checked
- mypy (current pip release) on Python 3.14.0: `open(f,'rb')` and `BytesIO` accepted for `SupportsRead`; a `read(self) -> str` class and a class without `read` were rejected; `name: str` protocol rejected properties and frozen dataclasses ("expected settable variable") while the read-only `@property` protocol accepted both; the callback protocol rejected a function lacking `retry`; PEP 695 `Repo[T](Protocol)` and explicit subclassing checked; at runtime `isinstance` against a `@runtime_checkable` protocol returned True for a class with the wrong `read` signature and non-runtime protocols raise `TypeError`.
