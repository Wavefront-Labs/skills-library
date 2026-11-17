---
id: computing-software.software-engineering.python.weakref-callbacks-and-finalizers
name: weakref-callbacks-and-finalizers
category: computing-software
field: software-engineering
product: python
tags: [python, py-memory, py-mem-weakref, weakref-callbacks, weakref, weakvaluedictionary, weakkeydictionary, weakset, finalize]
level: advanced
status: docs-checked
description: "Use weakref for caches, observers and cleanup: ref callbacks, WeakValueDictionary, WeakMethod, weakref.finalize versus __del__, and the limits of weak references."
sources: ["https://docs.python.org/3/library/weakref.html", "https://docs.python.org/3/library/weakref.html#weakref.WeakMethod"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# weakref callbacks and finalizers

A weak reference does not keep its referent alive; when the object is collected, the reference returns `None` and may call a callback.

```python
import weakref

class Resource: pass
r = Resource()
w = weakref.ref(r, lambda ref: print("collected"))   # callback receives the (now dead) weak reference
w() is r                                             # True while alive
del r                                                # callback runs when the object is about to be finalized
w() is None                                          # True

cache = weakref.WeakValueDictionary()                # entries vanish when values are no longer referenced elsewhere
cache["a"] = Resource()                              # needs a strong reference elsewhere to survive
registry = weakref.WeakSet()                         # observers: dead ones drop out automatically
keyed = weakref.WeakKeyDictionary()                  # per-object metadata without extending its life

class Listener:
    def handle(self): ...
m = weakref.WeakMethod(Listener().handle)            # bound methods are ephemeral: a plain weakref.ref cannot keep hold of one
```

## finalize: reliable cleanup
```python
class Conn:
    def __init__(self, sock):
        self.sock = sock
        self._fin = weakref.finalize(self, sock.close)   # runs when self is collected OR at interpreter exit (atexit=True default)
    def close(self): self._fin()                          # idempotent explicit close; calling a finalize runs it once
```
Prefer `weakref.finalize` (or context managers / `try`/`finally`) over `__del__`: a finalizer always survives until its object is collected, and remaining live finalizers are called at exit. Pass `finalize` only the specific functions and objects it needs rather than `self`, so the finalizer does not keep the object alive.

## Limits
- Not every type supports weak references: instances of `list` and `dict` do not directly, but a subclass does; `tuple` and `int` do not support them even when subclassed (CPython detail). Classes that define `__slots__` need `'__weakref__'` in the slots.
- Exceptions raised by a callback are noted on standard error and cannot be propagated (handled like `__del__` exceptions); keep callbacks tiny and exception-free.
- A finalizer created in a daemonic thread just as the program exits may not be called.

## Gotchas
- Entries disappear when no strong reference to the value (or key) exists any more, so use weak-value caches for memoising live objects, not for expensive-to-recompute data.
- A weak reference is hashable only if its referent is, and keeps its hash after the referent dies; if `hash` is first called after death it raises `TypeError`.

## Verify
- [ ] Test uses `gc.collect()` and asserts the weak reference is dead and the callback fired exactly once.
- [ ] The registry does not grow after repeated create/discard cycles.

## Checked

- 2026-11-03: checked against the CPython docs `library/weakref.rst`: `ref` callback semantics and exception handling, hashing, `WeakMethod`, `WeakValueDictionary`/`WeakKeyDictionary`/`WeakSet`, `finalize` behaviour at exit and alive/dead states, which types support weak references, `__slots__` and `'__weakref__'`.
- Fixed: the old text said `tuple` and `int` instances could be weakly referenced via subclasses; the docs say they cannot even when subclassed.
- Removed: PyPy and cycle-timing remarks, thread-of-callback claim, `lru_cache` advice, iteration-copy gotcha, tracemalloc/objgraph check, the datamodel `__del__` source (not read).

Method: documentation only; no commands were run.
