---
id: computing-software.software-engineering.python.threadpoolexecutor-and-futures
name: threadpoolexecutor-and-futures
category: computing-software
field: software-engineering
product: python
tags: [python, py-threading, threadpoolexecutor-futures, concurrent-futures, as-completed, future, io-bound, thread-pool]
level: practitioner
status: docs-checked
description: "Run I/O-bound work in a ThreadPoolExecutor: submit/map, as_completed, Future exceptions and cancellation, max_workers default and clean shutdown."
sources: ["https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ThreadPoolExecutor and futures

```python
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_EXCEPTION
import urllib.request

def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return url, r.status

with ThreadPoolExecutor(max_workers=16, thread_name_prefix="fetch") as pool:
    futures = {pool.submit(fetch, u): u for u in urls}
    for fut in as_completed(futures, timeout=60):
        url = futures[fut]
        try:
            print(fut.result())            # re-raises the worker's exception here
        except Exception as exc:
            print("failed", url, exc)

    # ordered results; an exception surfaces when that item's result is read
    results = list(pool.map(fetch, urls, timeout=60))
```
Leaving the `with` block calls `shutdown(wait=True)`.

## Sizing
- Default `max_workers`: `min(32, os.cpu_count() + 4)` in 3.8-3.12; from 3.13 `min(32, (os.process_cpu_count() or 1) + 4)`. It suits I/O-bound work; for CPU-bound work use `ProcessPoolExecutor`.
- The docs recommend not using `ThreadPoolExecutor` for long-running tasks (see exit behaviour below).
- Bound concurrency toward a single remote service explicitly (rate limits) rather than relying on pool size.

## Futures API
`fut.done()`, `fut.cancel()` (only works if not started), `fut.add_done_callback(cb)`, `fut.exception()`, `wait(fs, return_when=FIRST_EXCEPTION)`.
Python 3.9+: `shutdown(cancel_futures=True)` cancels pending futures that have not started; running or finished ones are unaffected.

## Gotchas
- `timeout` on `as_completed`/`result()`/`map` raises `TimeoutError` after waiting; a call that is already running cannot be cancelled (`cancel()` returns False for it).
- All threads enqueued to a `ThreadPoolExecutor` are joined before the interpreter can exit, and that exit handler runs before any `atexit` handlers, so exceptions in the main thread must be caught and handled to signal threads to stop. Use `shutdown(wait=False, cancel_futures=True)` in that handler to drop queued work.
- Exceptions are swallowed if you never call `result()`/`exception()` or iterate `map`.
- Deadlock: the docs warn it can occur when a callable waits on the result of another future in the same executor (for example a task submitted from a worker with too few workers).
- Shared state needs locks or queues.
- `Executor.map` collects its iterables immediately; Python 3.14 adds `buffersize=...` to limit the number of submitted tasks whose results have not been yielded.

## Verify
- [ ] A failing task shows its exception in logs with the URL/context.
- [ ] Run with 1 worker and with N workers; results equal as sets.

## Checked

- 2026-11-03: checked against the CPython docs `library/concurrent.futures.rst`: `map` timeout and `buffersize` (3.14), `shutdown(wait, cancel_futures)` (3.9), default `max_workers` history (3.8 and 3.13), exit-time join ordering versus `atexit`, deadlock warning, `Future.cancel/exception/add_done_callback`, `wait(return_when=...)`, `as_completed(timeout)`.
- Removed: the free-threaded-build suggestion, the claim about atomic list appends and the unsupported "timeout does not stop the worker" phrasing.

Method: documentation only; no commands were run.
