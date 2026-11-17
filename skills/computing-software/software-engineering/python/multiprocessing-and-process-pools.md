---
id: computing-software.software-engineering.python.multiprocessing-and-process-pools
name: multiprocessing-and-process-pools
category: computing-software
field: software-engineering
product: python
tags: [python, python-concurrency, multiprocessing, processpoolexecutor, concurrent-futures, spawn, fork, pickling, cpu-bound, shared-memory]
level: practitioner
status: verified
description: "Use ProcessPoolExecutor and multiprocessing for CPU-bound Python: start methods, the __main__ guard, pickling limits, chunksize, shared memory and pool failures."
sources: ["https://docs.python.org/3/library/multiprocessing.html", "https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor", "https://docs.python.org/3/library/multiprocessing.shared_memory.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# multiprocessing and process pools

**Goal:** use every core for CPU-bound Python work (with the GIL build) without the
classic hangs, pickling errors and memory blowups.

## Default tool: ProcessPoolExecutor
```python
from concurrent.futures import ProcessPoolExecutor, as_completed

def score(path: str) -> float: ...          # must be importable at module top level

if __name__ == "__main__":                  # REQUIRED with spawn/forkserver
    with ProcessPoolExecutor(max_workers=os.process_cpu_count()) as ex:
        results = list(ex.map(score, paths, chunksize=64))
```
- `chunksize` batches tasks per IPC round-trip; with thousands of tiny tasks the
  default of 1 is dominated by pickling overhead.
- `as_completed(futures)` to handle results as they finish and catch per-task exceptions.
- `max_tasks_per_child=` (3.11+) recycles workers that leak memory; it is incompatible with the `fork` start method (default context becomes spawn).
- `os.process_cpu_count()` is 3.13+ (use `os.cpu_count()` before); on Windows `max_workers` must be <= 61. Measured: 20000 tiny tasks took 4.3 s at `chunksize=1` and 0.009 s at `chunksize=500`.

## Start methods
| Method | Default on | Notes |
|---|---|---|
| spawn | Windows, macOS | fresh interpreter, re-imports your module; needs `__main__` guard; slower start |
| fork | Linux and other POSIX except macOS, Python 3.13 and earlier only (not the default on any platform from 3.14) | copies the parent; unsafe with threads (locks held by other threads stay locked forever) |
| forkserver | Linux (POSIX with fd passing), Python 3.14 and later only; macOS and Windows stay on spawn | safer fork from a clean server process |

The defaults changed in 3.14 (checked against the 3.13 and 3.14 docs and on 3.14.8/Linux): 3.13 and earlier use fork on Linux, 3.14 uses forkserver. Code that relied on fork semantics (inheriting globals, unpicklable functions, nested functions) breaks on 3.14 unless it asks for fork. Set explicitly for reproducible behaviour: `mp_context=multiprocessing.get_context("spawn")`.
Forking a process that has threads (logging handlers, gRPC, DB drivers) is a common
source of random deadlocks in children.

## Pickling limits
Arguments, return values and the function are pickled. Lambdas, nested functions,
open files, locks, DB connections and generators cannot be sent. Pass paths/ids, open
resources inside the worker (use `initializer=` to open once per worker).

With spawn the failure looks different per case (Python 3.14, Windows): a lambda raises
`PicklingError` in the parent, a lock argument raises `TypeError: cannot pickle '_thread.lock'`,
a function defined inside another function raises `PicklingError ... local object`, but a
function defined at module level only under `if __name__ == "__main__":` pickles fine and
then the child fails to import it, so every future gets a confusing `BrokenProcessPool`.
Define workers at the top level of the module, outside the guard.

## Large data
- Do not send big arrays per task. Use `multiprocessing.shared_memory.SharedMemory`
  (or numpy over it) and send only the name/shape.
- With fork, read-only globals loaded before the pool are shared copy-on-write, but
  CPython refcounting touches objects and gradually copies pages.

## Failure modes
- A worker killed (OOM, segfault, `os._exit`) raises `BrokenProcessPool` for all pending futures
  (checked); later `submit` calls raise it too, so the pool must be recreated.
- Exceptions in workers are re-raised in the parent on `.result()`; with `map`, the
  first one stops iteration.
- Ctrl-C with pools can hang; use `with` blocks and `cancel_futures=True` on shutdown.

## When not to use it
I/O-bound work: threads or asyncio. Numeric work: numpy releases the GIL already.
Python 3.13t free-threaded builds may make threads viable for CPU work.

## Verify
- [ ] Runs on Windows/macOS (spawn) as well as Linux.
- [ ] Wall time scales with workers on a benchmark input; if not, IPC dominates (raise chunksize).
## Checked
Run on Windows with Python 3.14.0 (spawn is the only start method there): `ex.map` with chunksize, lambda/lock/local-function pickling errors, the missing `__main__` guard (`RuntimeError` about the bootstrapping phase), `initializer=`, `max_tasks_per_child` recycling workers, a killed worker giving `BrokenProcessPool` for pending and later futures, first exception re-raised by `map`, and `SharedMemory` passed by name. Fetched: the multiprocessing and concurrent.futures docs for the 3.14 default change (fork no longer default anywhere; forkserver default on Linux) and the `max_tasks_per_child` / fork incompatibility. Not run: fork and forkserver on Linux, Ctrl-C hangs, copy-on-write behaviour, free-threaded builds. Behaviour on Linux before 3.14 differs: fork makes a nested or guarded function appear to work.
Version check: 3.13 docs say fork is "currently the default on POSIX except macOS" and announce the change; 3.14 docs say fork is "no longer the default start method on any platform" and forkserver is the default on POSIX platforms that support fd passing. Run on 3.14.8/Linux: `get_start_method()` returned `forkserver`. 3.13 itself was not run.
Linux pass (Python 3.14.8 standalone musl build in a WSL2 busybox distro): default start method is `forkserver` (3.14 doc claim confirmed); a function defined only under the `__main__` guard still gives `BrokenProcessPool` under forkserver, but works with an explicit `fork` context; `max_tasks_per_child` with `fork` raises `ValueError` and with the default context uses spawn; killed-worker, lambda, lock, local-function and chunksize results (4.0 s vs 0.019 s) match Windows. Without the `__main__` guard the forkserver start fails with a `ConnectionResetError` instead of Windows' bootstrapping `RuntimeError`.
