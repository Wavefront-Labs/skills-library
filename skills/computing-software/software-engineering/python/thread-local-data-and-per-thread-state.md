---
id: computing-software.software-engineering.python.thread-local-data-and-per-thread-state
name: thread-local-data-and-per-thread-state
category: computing-software
field: software-engineering
product: python
tags: [python, py-threading, thread-local-data, threading-local, connection-per-thread, thread-safety, contextvars]
level: practitioner
status: docs-checked
description: "Keep per-thread state such as DB connections with threading.local, initialise it lazily, clean it up, and know when contextvars or pools are the better tool."
sources: ["https://docs.python.org/3/library/threading.html#thread-local-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread-local data

```python
import threading, sqlite3

_local = threading.local()                      # one object, attributes are per thread

def conn():
    c = getattr(_local, "conn", None)
    if c is None:
        c = _local.conn = sqlite3.connect("app.db")   # one connection per thread
    return c
```
Each thread sees its own `_local.conn`; a new thread starts with no attributes.

## Subclass for defaults
```python
class Ctx(threading.local):
    def __init__(self, **kw):       # called each time the object is used in a separate thread
        self.depth = 0
```

## Cleanup
For resources, register cleanup in the thread's own target `finally`. In pools, workers live long: `ThreadPoolExecutor` takes an `initializer=` callable run at the start of each worker thread (if it raises, pending and future jobs fail with `BrokenThreadPool`), but it has no finalizer hook, so close at shutdown via a tracked list.

## Choosing
- asyncio code: use `contextvars`, since many tasks share one thread.
- Many short threads: per-thread connections churn. Prefer a connection pool object with a lock/queue.

## Gotchas
- Values set in one thread are invisible in other threads; a new thread starts with no attributes (the docs show a fresh thread seeing different data).
- Values read from a `local`, including its `__dict__`, belong to whichever thread was current when read, so do not save them across threads.
- Accumulating resources in thread locals of an unbounded number of threads leaks; cap the threads.

## Verify
- [ ] Test starts two threads, sets different values, and asserts isolation.
- [ ] Check `len(threading.enumerate())` stays bounded under load.

## Checked

- 2026-11-03: checked against the CPython docs `library/threading.rst` (thread-local data section) and `library/concurrent.futures.rst` (`ThreadPoolExecutor` `initializer`): per-thread attributes, subclassing `local` with `__init__` called per thread, cross-thread value caveat.
- Removed: free-threaded and fork/pickle remarks, `weakref.finalize` suggestion, per-thread `random.Random` advice, the claim about sqlite3 default thread sharing.

Method: documentation only; no commands were run.
