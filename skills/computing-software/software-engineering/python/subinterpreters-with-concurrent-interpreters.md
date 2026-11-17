---
id: computing-software.software-engineering.python.subinterpreters-with-concurrent-interpreters
name: subinterpreters-with-concurrent-interpreters
category: computing-software
field: software-engineering
product: python
tags: [python, py-multiproc, concurrent-interpreters, subinterpreters, interpreterpoolexecutor, pep-734, pep-684, python-314]
level: advanced
status: docs-checked
description: "Python 3.14 multiple interpreters: concurrent.interpreters, InterpreterPoolExecutor, per-interpreter GIL, sharing data between interpreters and extension module limits."
sources: ["https://docs.python.org/3.14/library/concurrent.interpreters.html", "https://docs.python.org/3.14/library/concurrent.futures.html#interpreterpoolexecutor", "https://peps.python.org/pep-0734/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subinterpreters (Python 3.14)

**Version note:** `concurrent.interpreters` is new in **Python 3.14** (PEP 734; the docs say interpreters have been isolated enough not to share the GIL since 3.12, PEP 684). Interpreters are isolated by default and provide no concurrency on their own; combine them with threads for multi-core parallelism. They are similar to processes but have in-process efficiency like threads. Not available on WASI.

```python
from concurrent import interpreters
from concurrent.futures import InterpreterPoolExecutor

interp = interpreters.create()
interp.exec('print("spam!")')              # run source in the current thread
res = interp.call(run, 'spam!')            # run a function in the interpreter, current thread
t = interp.call_in_thread(run, 'spam!')    # run in a new thread
t.join()
interp.close()

with InterpreterPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(cpu_task, range(8))))   # each worker thread runs its own interpreter
```

`InterpreterPoolExecutor` is a `ThreadPoolExecutor` subclass where each worker thread has its own interpreter and its own GIL, giving true multi-core parallelism. Its `initializer` and `initargs` run in the worker's interpreter and are pickled on the way in; `map` ignores `chunksize`.

## Sharing data
- Most objects are copied with pickle when sent to another interpreter, so mutable objects do not stay in sync. Nearly all immutable builtins are shared or copied efficiently: `None`, `bool`, `bytes`, `str`, `int`, `float`, `tuple` of supported objects.
- The few types that share mutable data are `memoryview` (objects with the buffer protocol) and `Queue`. `interpreters.create_queue(maxsize=0)` makes a cross-interpreter queue; `maxsize <= 0` means unbounded. It implements `queue.Queue` methods except `task_done()`, `join()` and `shutdown()`.
- `interp.prepare_main(ns=None, **kwargs)` binds objects in the interpreter's `__main__`. `exec()`, `eval()` and functions not tied to a module use the interpreter's `__main__` as globals.
- An object that cannot be sent raises `NotShareableError` (a `TypeError`).

## Gotchas
- Not all PyPI packages support multiple interpreters yet; see the docs page "Isolating Extension Modules". Extension modules can break isolation, so do not use interpreters where they must not see each other's data (security-sensitive cases).
- An uncaught exception in code run with `exec()` is raised as `interpreters.ExecutionFailed` (an `InterpreterError`) with an `excinfo` snapshot; per PEP 734, exceptions from `Interpreter.call()` are raised directly in the caller.
- The API is new; re-check the docs on newer Python versions.

## Verify
- [ ] Benchmark against `ProcessPoolExecutor` on your real workload before adopting.
- [ ] Import every dependency inside a fresh interpreter in CI to detect incompatibilities early.

## Checked
2026-11-09. Confirmed against the Python 3.14 `concurrent.interpreters` and `InterpreterPoolExecutor` docs and PEP 734 (API names, isolation and GIL statements, shareable types, Queue, exceptions, initializer pickling, chunksize, WASI). Removed: lower start-up cost and memory claims, the free-threaded/asyncio choice table, the exact `ImportError` message, NumPy support remarks, and `os.environ`/`signal`/`fork` notes, which these pages do not state. PEP 734 was read only for the sections quoted.
Method: documentation only; no commands were run.
