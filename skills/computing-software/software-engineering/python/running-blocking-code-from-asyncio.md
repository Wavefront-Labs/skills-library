---
id: computing-software.software-engineering.python.running-blocking-code-from-asyncio
name: running-blocking-code-from-asyncio
category: computing-software
field: software-engineering
product: python
tags: [python, asyncio-to-thread, run-in-executor, blocking-io, event-loop-blocking, asyncio, processpoolexecutor]
level: practitioner
status: verified
description: "Call blocking libraries from async code without stalling the loop: asyncio.to_thread, run_in_executor with thread or process pools, sizing them, and spotting accidental blocking."
sources: ["https://docs.python.org/3/library/asyncio-task.html#running-in-threads", "https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor", "https://docs.python.org/3/library/asyncio-dev.html#running-blocking-code"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Running blocking code from asyncio

**Goal:** use sync libraries (boto3, psycopg2, PIL, requests) inside an asyncio app
without freezing every other request.

## The problem
The event loop runs one callback at a time. `time.sleep(1)`, `requests.get()`, a large
`json.loads` or CPU-heavy work inside `async def` blocks *all* tasks for that duration.

## I/O-bound blocking calls: threads
```python
import asyncio
data = await asyncio.to_thread(s3.get_object, Bucket=b, Key=k)    # 3.9+
```
`to_thread` uses the loop's default `ThreadPoolExecutor` and copies contextvars (so
request IDs in logging context survive). Default pool size is
`min(32, os.cpu_count() + 4)` (3.13+ uses `os.process_cpu_count()`; 16 on a 12-thread machine, checked); many concurrent blocking calls queue behind it. Set a
dedicated pool when needed:
```python
from concurrent.futures import ThreadPoolExecutor
loop = asyncio.get_running_loop()
loop.set_default_executor(ThreadPoolExecutor(max_workers=64))
# or per call:
db_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="db")
row = await loop.run_in_executor(db_pool, cursor_fetch, sql)       # no kwargs: use functools.partial
```

## CPU-bound work: processes
Threads don't help CPU-bound pure Python because of the GIL (except on free-threaded builds).
```python
from concurrent.futures import ProcessPoolExecutor
from functools import partial
cpu_pool = ProcessPoolExecutor(max_workers=4)     # create once at startup, reuse
thumb = await loop.run_in_executor(cpu_pool, partial(make_thumbnail, img_bytes, size=256))
```
Arguments and results are pickled: pass bytes/paths, not open files or clients. Define the
function at module top level.

## Prefer native async libraries
`httpx`/`aiohttp` over `requests`, `asyncpg`/`psycopg` (3, async) over psycopg2,
`aiofiles` is still threads underneath. Thread offloading is the bridge, not the target.

## Finding accidental blocking
```python
asyncio.run(main(), debug=True)        # logs "Executing <Task ...> took 0.153 seconds"
loop.slow_callback_duration = 0.05
```
Or `PYTHONASYNCIODEBUG=1`. In production, measure event-loop lag (schedule a callback
every 100 ms and record the delay).

## Gotchas
- Cancelling the awaiting task does not stop the thread; the blocking call runs to
  completion. Give the sync call its own timeout.
- Thread pool threads don't see a running event loop; calling async code from them needs
  `asyncio.run_coroutine_threadsafe(coro, loop)`.
- Shut pools down on exit (`pool.shutdown(wait=True, cancel_futures=True)`).

## Verify
- [ ] asyncio debug mode shows no slow-callback warnings under load.
- [ ] Latency of a cheap endpoint stays flat while heavy blocking requests run.
## Checked
Run with Python 3.14.0 on Windows: `to_thread` copies contextvars into the worker; default executor `_max_workers` equals `min(32, process_cpu_count + 4)`; `run_in_executor(pool, f, 1, b=2)` raises `TypeError` and `functools.partial` works; cancelling the awaiting task leaves the thread running to completion; a worker thread has no running loop (`get_running_loop` raises) and `run_coroutine_threadsafe(...).result()` works; debug mode logs `Executing <Task ...> took 0.2 seconds` for a blocking `time.sleep` (checked with `slow_callback_duration=0.05`). Not run: boto3/psycopg2, `ProcessPoolExecutor` from the loop (covered in the multiprocessing skill), production lag measurement.
Linux pass (Python 3.14.8 standalone musl build in a WSL2 busybox distro): every check above gave the same result as on Windows.
