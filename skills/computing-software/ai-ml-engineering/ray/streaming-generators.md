---
id: computing-software.ai-ml-engineering.ray.streaming-generators
name: streaming-generators
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, streaming-generator, objectrefgenerator, num-returns-streaming, dynamic-generator]
level: practitioner
status: docs-checked
description: "Stream results from Ray tasks and actors as they are produced using generator functions and ObjectRefGenerator with backpressure."
sources:
  - https://docs.ray.io/en/latest/ray-core/ray-generator.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.ObjectRefGenerator.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming generators

```python
@ray.remote
def read_chunks(path):
    for i, chunk in enumerate(read(path)):
        yield chunk                          # each yield becomes its own ObjectRef immediately

gen = read_chunks.remote("big.parquet")     # ObjectRefGenerator
for ref in gen:                              # blocks per item, in order
    process(ray.get(ref))
# async: async for ref in gen:
```
Backpressure: the private task option `_generator_backpressure_num_objects` sets the maximum number of generated but unconsumed objects (`-1` disables it); it is not supported for async generators. Ray eagerly runs a generator task to completion otherwise, whether or not the caller polls.

Generators work in actor and non-actor tasks and with regular, threaded and async actors.

## Gotchas
- `num_returns="dynamic"` is the deprecated dynamic generator API (a `DynamicObjectRefGenerator` through one `ObjectRef`); use the streaming API in new code.
- On failure, `next(gen)` returns a ref that holds the exception and `ray.get` raises it; for an application exception it arrives in order, after the earlier yields.
- You can pass an `ObjectRefGenerator` to `ray.wait` (ready when its next item is available) but not to `ray.get`; `gen.completed()` returns a ref that resolves when the task ends.
- Refs you never consume are garbage-collected when the generator is.
- Not supported: `throw`/`send`/`close`, `return` in the generator, passing the generator to another task or actor, Ray Client. `ObjectRefGenerator` is not thread-safe.

## Verify
Producer prints timestamps per yield and consumer prints per receive; receives must start before the producer finishes.

## Checked
2026-11-03: checked against the Ray docs source `core/ray-generator.md`, `core/internals/streaming-generator.md` and the task options in `python/ray/remote_function.py`. Removed the unconfirmed "dropping the generator cancels production" claim and the `num_returns="streaming"` claim, and the "confirm param name" marker.
Method: documentation only; no commands were run.
