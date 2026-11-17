---
id: computing-software.software-engineering.python.context-managers-and-contextlib
name: context-managers-and-contextlib
category: computing-software
field: software-engineering
product: python
tags: [python, python-data-model, context-managers, contextlib, with-statement, exitstack, resource-cleanup]
level: practitioner
status: verified
description: "Manage resources with with-statements: writing __enter__/__exit__, @contextmanager, ExitStack for dynamic resources, suppress/closing, and async context managers."
sources:
  - https://docs.python.org/3/reference/datamodel.html#context-managers
  - https://docs.python.org/3/library/contextlib.html
  - https://peps.python.org/pep-0343/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context managers and contextlib

**Goal:** resources (files, locks, connections, temp state) are always released, including on exceptions.

## 1. @contextmanager for most cases
```python
from contextlib import contextmanager

@contextmanager
def transaction(conn):
    cur = conn.cursor()
    try:
        yield cur
    except BaseException:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        cur.close()
```
Exactly one `yield`. Code after `yield` must be in `try/finally` or it is skipped when the body raises.

## 2. Class form when you need state or reuse
```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False          # True would swallow the exception
```

## 3. Dynamic number of resources: ExitStack
```python
from contextlib import ExitStack
with ExitStack() as stack:
    files = [stack.enter_context(open(p)) for p in paths]
    stack.callback(log.info, "all closed")
    # if opening file 7 fails, files 1-6 are still closed
```
`stack.pop_all()` transfers ownership out (build resources, then hand them to an object that closes later).

## 4. Standard helpers
```python
from contextlib import suppress, closing, redirect_stdout, chdir, nullcontext
with suppress(FileNotFoundError): os.remove(tmp)
with closing(urlopen(url)) as resp: ...
with chdir(build_dir): ...              # 3.11+, not thread-safe
cm = lock if threaded else nullcontext()
with cm: ...
```
Multiple managers: `with (open(a) as fa, open(b) as fb):` (parenthesised, 3.10+).

## 5. Async
```python
from contextlib import asynccontextmanager
@asynccontextmanager
async def session():
    s = await connect()
    try:
        yield s
    finally:
        await s.close()
```
`AsyncExitStack` mirrors ExitStack.

## Gotchas
- `__exit__` returning a truthy value suppresses the exception; accidental `return self` hides bugs.
- `@contextmanager` objects are single-use; calling the decorated function again gives a fresh one, but reusing the same object raises (on 3.14.0 an `AttributeError`, not a clear message).
- Generators inside `with` used as decorators (`@transaction(conn)`) wrap each call; ContextDecorator semantics.
- `suppress` around a large block hides more than intended; keep it to one statement.

## Verify
- A test that raises inside the `with` body asserts cleanup ran (mock `close` called, lock released) and the original exception propagated.

## Checked
- Python 3.14.0: ran the cases; re-entering a spent `@contextmanager` object raised `AttributeError`; a `@contextmanager` object used as decorator ran enter/exit per call; `__exit__` returning self swallowed a `KeyError`; `contextlib.chdir` and `ExitStack` exist. Other helper snippets are standard library as documented at docs.python.org/3/library/contextlib.html.
