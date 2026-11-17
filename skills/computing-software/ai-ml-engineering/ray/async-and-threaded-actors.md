---
id: computing-software.ai-ml-engineering.ray.async-and-threaded-actors
name: async-and-threaded-actors
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, async-actor, max-concurrency, concurrency-groups, threaded-actor]
level: practitioner
status: docs-checked
description: "Run concurrent Ray actor methods with async def, max_concurrency for threads, and concurrency groups to isolate method pools."
sources:
  - https://docs.ray.io/en/latest/ray-core/actors/async_api.html
  - https://docs.ray.io/en/latest/ray-core/actors/concurrency_group_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async and threaded actors

```python
@ray.remote
class AsyncFetcher:
    async def fetch(self, url):
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r: return await r.text()   # many calls interleave on one loop

a = AsyncFetcher.options(max_concurrency=100).remote()   # default 1000 for async actors
ray.get([a.fetch.remote(u) for u in urls])

@ray.remote(max_concurrency=8)      # threaded actor: sync methods on a thread pool
class Pool:
    def work(self, x): return heavy_io(x)

@ray.remote(concurrency_groups={"io": 4, "compute": 2})
class Mixed:
    @ray.method(concurrency_group="io")
    def read(self): ...
    @ray.method(concurrency_group="compute")
    def calc(self): ...
```

## Gotchas
- Ray runs an async actor's methods in a single event loop on one thread, and `await` is what switches between them; a method that blocks without awaiting stalls the others.
- Neither threaded nor async actors bypass the GIL; NumPy, PyTorch and similar libraries release it in C/C++ code.
- One `async def` method makes the whole actor async, not threaded.
- Do not call blocking `ray.get` or `ray.wait` inside an async method; `await` the object ref instead.
- The default concurrency group has a limit of 1000 for async actors and 1 otherwise; `max_concurrency` changes it.
- Ray does not support `async def` for remote tasks; wrap the coroutine in a sync function with `asyncio.run`.

## Verify
Fire 50 calls that each `await asyncio.sleep(1)` on an async actor; they should overlap rather than run one after another.

## Checked
2026-11-03: checked against the Ray docs source `core/actors/async-api.md` and `core/actors/concurrency-group-api.md`. Removed the unsourced `run_in_executor`, locking and sync-methods-on-the-loop claims.
Method: documentation only; no commands were run.
