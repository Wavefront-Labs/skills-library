---
id: computing-software.software-engineering.python.asyncio-queues-and-semaphores
name: asyncio-queues-and-semaphores
category: computing-software
field: software-engineering
product: python
tags: [python, asyncio-queue, asyncio-semaphore, bounded-concurrency, worker-pool, producer-consumer, asyncio]
level: practitioner
status: verified
description: "Bound asyncio concurrency: Semaphore around calls, Queue-based worker pools with join/task_done, backpressure via maxsize, and clean shutdown (Queue.shutdown in 3.13)."
sources: ["https://docs.python.org/3/library/asyncio-queue.html", "https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore", "https://docs.python.org/3/library/asyncio-task.html#task-groups"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# asyncio queues and semaphores

**Goal:** process thousands of items concurrently without opening thousands of sockets,
hitting rate limits or running out of memory.

## Pattern 1: semaphore around the expensive call
```python
import asyncio, httpx

async def fetch_all(urls, limit=20):
    sem = asyncio.Semaphore(limit)
    async with httpx.AsyncClient(timeout=10) as client:
        async def one(url):
            async with sem:                       # at most `limit` in flight
                r = await client.get(url)
                r.raise_for_status()
                return r.json()
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(one(u)) for u in urls]
    return [t.result() for t in tasks]
```
Simple, but creates one task per item up front (fine for thousands, not for millions or
unbounded streams).

## Pattern 2: queue + fixed workers (streams, backpressure)
```python
async def worker(name, q: asyncio.Queue, out: list):
    while True:
        item = await q.get()
        try:
            out.append(await process(item))
        except Exception:
            log.exception("item %r failed", item)
        finally:
            q.task_done()                      # always, or join() hangs forever

async def run(items, n_workers=10):
    q = asyncio.Queue(maxsize=100)             # producer blocks when full: backpressure
    out = []
    workers = [asyncio.create_task(worker(i, q, out)) for i in range(n_workers)]
    for it in items:
        await q.put(it)
    await q.join()                             # all items processed
    for w in workers: w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    return out
```
3.13+: `q.shutdown()` makes `get()` raise `QueueShutDown` once empty (items already queued are still returned, `put()` raises immediately), a cleaner stop than
cancelling. `PriorityQueue` and `LifoQueue` share the API.

## Rate limiting (per second, not concurrency)
Semaphore limits concurrency, not rate. For "max 10 requests/second" release permits on a
timer or use a token bucket (e.g. `aiolimiter.AsyncLimiter(10, 1)`).

## Gotchas
- asyncio primitives are not thread-safe; from other threads use
  `loop.call_soon_threadsafe(q.put_nowait, x)` or `asyncio.run_coroutine_threadsafe`.
- A worker raising out of the loop silently dies and the queue stalls; catch per item.
- `asyncio.gather(*1_000_000_coroutines)` schedules everything at once; use pattern 2.
- `BoundedSemaphore` raises if released more than acquired - catches bugs in manual acquire/release.

## Verify
- [ ] Peak concurrent connections (server logs or `len(sem._waiters)` in debug) never exceed the limit.
- [ ] Memory flat when feeding an unbounded generator (queue `maxsize` set).
## Checked
Run with Python 3.14.0 on Windows: semaphore of 5 over 50 TaskGroup tasks peaked at exactly 5 in flight; queue plus 3 workers drained 20 items with one failure logged and `gather(..., return_exceptions=True)` returning `CancelledError` for each cancelled worker; `join()` hangs without `task_done()`; `QueueShutDown` behaviour; `BoundedSemaphore` over-release raises `ValueError`; `call_soon_threadsafe(q.put_nowait, x)` from a thread wakes a waiting `get()`; a worker raising out of its loop ends silently and queued items stall. Not run: httpx fetches, `aiolimiter`, million-task memory claims, versions before 3.13 (`shutdown` absent).
Linux pass (Python 3.14.8 standalone musl build in a WSL2 busybox distro): every check above gave the same result as on Windows.
