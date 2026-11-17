---
id: computing-software.ai-ml-engineering.ray.serve-multiplexing
name: serve-multiplexing
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, model-multiplexing, serve-multiplexed, multiplexed-model-id, lru-models]
level: practitioner
status: docs-checked
description: "Serve many models from one Ray Serve replica pool with @serve.multiplexed, serve.get_multiplexed_model_id and LRU eviction."
sources:
  - https://docs.ray.io/en/latest/serve/model-multiplexing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model multiplexing

Use it for many models with the same input shape but different weights that are sparsely invoked.

```python
@serve.deployment(ray_actor_options={"num_gpus": 1})
class Multi:
    @serve.multiplexed(max_num_models_per_replica=3)      # LRU-evicts beyond 3
    async def get_model(self, model_id: str):
        return await load_model(model_id)                  # your own loader
    async def __call__(self, request):
        model_id = serve.get_multiplexed_model_id()       # read from the request header
        model = await self.get_model(model_id)
        return model(await request.json())
```
Client: send header `serve_multiplexed_model_id: <MODEL_ID>` with the HTTP request. From a handle: `handle.options(multiplexed_model_id="<MODEL_ID>").remote(x)`.

## Facts from the docs
- If more models than `max_num_models_per_replica` are loaded, Serve evicts the least recently used. Implement `__del__` on the model class to release resources when it is evicted.
- The router sends a request to a replica that already holds the model; if all such replicas are over-subscribed, it uses a new replica, which loads and caches the model. If none becomes available within a timeout, it falls back to default routing.
- `serve_multiplexed_model_id` is required in the header for multiplexed routing; without it the request is a normal one routed to a random replica.
- `serve.get_multiplexed_model_id()` works inside `@serve.batch` functions; all requests in a batch share the same model id.

## Verify
Send requests with more distinct IDs than `max_num_models_per_replica` and check deployment logs for loads and evictions.

## Checked
2026-11-03. Confirmed in Ray repo docs `serve/model-multiplexing.md`. Removed: advice to "del model" explicitly, autoscaling pairing advice, cold-load latency commentary and the S3 URL, the unfetched API page source.
Method: documentation only; no commands were run.
