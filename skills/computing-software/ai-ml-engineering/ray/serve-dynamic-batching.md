---
id: computing-software.ai-ml-engineering.ray.serve-dynamic-batching
name: serve-dynamic-batching
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, serve-batch, dynamic-batching, max-batch-size, batch-wait-timeout]
level: practitioner
status: docs-checked
description: "Batch requests in Ray Serve with the @serve.batch decorator (max_batch_size, batch_wait_timeout_s, batch_size_fn) to raise GPU throughput."
sources:
  - https://docs.ray.io/en/latest/serve/advanced-guides/dyn-req-batch.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic request batching

```python
from ray import serve
from typing import List

@serve.deployment
class Embedder:
    def __init__(self): self.m = load()            # load() is your own loader
    @serve.batch(max_batch_size=32, batch_wait_timeout_s=0.02)
    async def embed(self, texts: List[str]) -> List[list]:
        return self.m.encode(texts).tolist()        # one result per input, same order
    async def __call__(self, request):
        text = (await request.json())["text"]
        return await self.embed(text)               # each caller passes ONE item
```

## Rules from the docs
- The decorated method must be `async` (batching runs on the asyncio event loop), take a list of its original input types and return a list of equal length so Serve can split the output back to the requests.
- `max_batch_size` default 10; `batch_wait_timeout_s` default 0.01 (10 ms): once the first request arrives Serve waits for a full batch until the timeout, then sends whatever it has.
- `batch_size_fn` (optional) computes an effective batch size from the list (default `len(batch)`), for example total tokens. Then set `max_batch_size` in that metric.
- Reconfigure at runtime with `set_batch_wait_timeout_s` and `set_max_batch_size`.
- Streaming: decorate an async generator that takes a list and, each iteration, yields an iterable of outputs the same length as the batch; pass a `StopIteration` object for an input that has finished.
- Guidance: `max_batch_size` ideally a power of 2; large sizes cost memory and add latency to the first requests. Keep `batch_wait_timeout_s` well below the latency budget left after model time. In chained batched models, make downstream batch sizes multiples or divisors of upstream ones.

## Verify
Log `len(texts)` inside `embed`; under load it should approach `max_batch_size`.

## Checked
2026-11-03. Confirmed in Ray repo docs `serve/advanced-guides/dyn-req-batch.md`. Removed (not in the docs): "5-50 ms is typical", the `max_ongoing_requests` relation, exception and per-replica behaviour claims.
Method: documentation only; no commands were run.
