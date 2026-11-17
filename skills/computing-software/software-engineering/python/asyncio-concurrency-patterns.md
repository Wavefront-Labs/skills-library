---
id: computing-software.software-engineering.python.asyncio-concurrency-patterns
name: asyncio-concurrency-patterns
category: computing-software
field: software-engineering
product: python
tags: [python, asyncio, concurrency, async-await, tasks, taskgroup, cancellation, structured-concurrency, event-loop, aiohttp, anyio, event-loop-blocking, gather, timeout, py-asyncio-core]
level: advanced
status: verified
description: "Structure concurrent I/O with asyncio: TaskGroup, cancellation propagation, timeouts, and keeping blocking calls off the event loop."
sources: ["Python docs - asyncio-task, asyncio-dev (Developing with asyncio)", "PEP 654 exception groups", "personal production experience with aiohttp services"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# asyncio concurrency patterns — structured concurrency without silent hangs

**Goal:** run many I/O-bound operations concurrently, cancel them cleanly as a group,
and never let one blocking call freeze the whole event loop.

## 1. Prefer TaskGroup over bare gather() (3.11+)
```python
async def fetch_all(urls):
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(u)) for u in urls]
    return [t.result() for t in tasks]
```
If one task raises, `TaskGroup` cancels every sibling and raises an `ExceptionGroup`
(PEP 654) — `asyncio.gather()` without `return_exceptions=True` leaves siblings running
as orphaned background tasks, a common source of "the request finished but CPU is still
spinning." On Python < 3.11, use the `anyio` or `trio`-style `asyncio.gather(*tasks,
return_exceptions=True)` and manually cancel+await the rest on error.

## 2. Cancellation is cooperative and can be swallowed
`task.cancel()` raises `asyncio.CancelledError` at the *next* await point inside the
task. Gotchas:
- `except Exception:` does NOT catch `CancelledError` (it subclasses `BaseException`
  since 3.8) — good, but a bare `except:` or `except BaseException:` that doesn't
  re-raise will silently eat the cancellation and the task never stops.
- A task that never awaits (tight CPU loop, or an await on a non-cancellable primitive)
  cannot be cancelled until it yields control.
- Always use `asyncio.timeout()` (3.11+) or `asyncio.wait_for()` around anything
  talking to the network — without it, a hung socket blocks forever regardless of your
  own deadlines.
```python
async with asyncio.timeout(5):
    resp = await session.get(url)
```

## 3. Never block the event loop
Any synchronous call that can take >1-10ms (CPU-bound work, `requests`, blocking file
I/O, `time.sleep`, `subprocess.run` without `asyncio.create_subprocess_exec`) stalls
*every* concurrent task, not just the caller. Fix:
```python
result = await asyncio.to_thread(cpu_bound_fn, arg)          # 3.9+, thread pool
result = await loop.run_in_executor(process_pool, cpu_fn, a) # CPU-heavy: real parallelism
```
`asyncio.to_thread` uses a thread, which helps for I/O-bound sync calls (GIL released)
but not CPU-bound ones — those need `run_in_executor` with a `ProcessPoolExecutor`.

## 4. Diagnosing a stalled loop
- `PYTHONASYNCIODEBUG=1` (or `asyncio.run(main(), debug=True)`) logs any callback that
  takes longer than 100ms and warns on non-awaited coroutines ("coroutine was never
  awaited" — usually a forgotten `await`).
- `asyncio.all_tasks()` lists every live task; a growing count across requests means
  tasks are leaking (fire-and-forget tasks must be stored and awaited/cancelled, or
  they can be silently garbage-collected mid-flight with a "Task was destroyed but it
  is pending" warning).

## 5. Fire-and-forget tasks need an owner
```python
background = set()
t = asyncio.create_task(job())
background.add(t)
t.add_done_callback(background.discard)
```
Without holding a reference, the task object can be GC'd before it completes.

## Gotchas
- Mixing `asyncio` loops across threads: each thread needs its own loop; never pass a
  loop-bound object (lock, queue) across threads without `run_coroutine_threadsafe`.
- `asyncio.Lock`/`Queue` are NOT thread-safe — they coordinate coroutines on one loop.
- Context managers that do I/O in `__aexit__` still run during cancellation cleanup —
  keep them fast or they delay shutdown.

## Verify
- [ ] Every concurrent fan-out uses `TaskGroup` (or `gather(..., return_exceptions=True)`
      with explicit cleanup), not bare `gather()` that can orphan tasks.
- [ ] Every network/DB await is wrapped in `asyncio.timeout()`.
- [ ] No sync call >10ms runs directly inside a coroutine — moved to `to_thread`/executor.
- [ ] `debug=True` run during dev shows no "never awaited" or slow-callback warnings.
- [ ] Background tasks are stored in a set and explicitly cancelled on shutdown.

Related: computing-software.software-engineering.python.packaging-with-pyproject,
computing-software.software-engineering.concurrency.profiling-before-optimising

## Checked
- Python 3.14.0 on Windows: `TaskGroup` cancelled the sibling and raised `ExceptionGroup` (caught by `except*`); bare `gather` raised at once while the sibling kept running and finished; `except BaseException` swallowed a cancel; `CancelledError` is a `BaseException`, not an `Exception`; four CPU jobs via `to_thread` took the same time as serial (0.32 s vs 0.32 s); `debug=True` logged a 0.2 s blocking call and a never-awaited coroutine with its creation traceback; `slow_callback_duration` is 0.1; a dropped `create_task` logged "Task was destroyed but it is pending" at loop close; `all_tasks()`/`print_stack()` worked. Weak-reference warning, to_thread GIL note and "primitives are not thread-safe" quoted from docs.python.org asyncio-task and asyncio-sync pages.
