---
id: computing-software.ai-ml-engineering.mlops.bentoml-and-fastapi-model-services
name: bentoml-and-fastapi-model-services
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-serving, bentoml, fastapi-model-serving, adaptive-batching, model-loading, inference-api]
level: practitioner
status: docs-checked
description: "Wrap models as HTTP services with BentoML (services, adaptive batching, depends) or FastAPI (lifespan loading, def versus async def endpoints)."
sources:
  - https://docs.bentoml.com/en/latest/build-with-bentoml/services.html
  - https://docs.bentoml.com/en/latest/get-started/adaptive-batching.html
  - https://fastapi.tiangolo.com/advanced/events/
  - https://fastapi.tiangolo.com/async/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BentoML and FastAPI model services

**Goal:** a simple HTTP inference service for one model, without a heavy serving platform.

## BentoML
```python
import bentoml
from typing import List
from transformers import pipeline

@bentoml.service
class Summarization:
    def __init__(self) -> None:
        self.pipeline = pipeline("summarization")     # load the model in the Service constructor

    @bentoml.api(batchable=True)                       # batching is disabled by default
    def summarize(self, texts: List[str]) -> List[str]:
        return [item["summary_text"] for item in self.pipeline(texts)]
```
- Services are the core building blocks; configuration fields (resources such as GPU, traffic such as timeout) are optional and set in `@bentoml.service(...)`. APIs can be synchronous functions or async coroutines.
- `bentoml.depends(OtherService)` lets one Service call another; the Service that runs inference collects requests from the intermediary Service and forms batches.

## Adaptive batching
Server-side dispatcher collects requests until the batch window or batch size is reached, then sends the batch to the model. The algorithm adjusts to recent traffic: bigger batches under load, lower latency when quiet.
- Batchable APIs take a type that can hold many requests, such as `List[str]` or `numpy.ndarray`, and accept only one parameter besides `bentoml.Context`. To pass several values, group them in a pydantic model and take `list[Model]`.
- Parameters: `batch_dim` (batch dimension for input and output), `max_batch_size` (cap on requests per batch; set by memory or GPU), `max_latency_ms` (upper bound on end-to-end batch delay; the dispatcher predicts processing time to respect it).
- The order of requests in a batch is not guaranteed, so do not rely on position beyond the returned list matching the input list.

## FastAPI
- Load models at startup with a lifespan handler (startup code before the `yield`, shutdown after); the events page describes startup logic as running before the application starts receiving requests, not at import time.
- A path operation declared with plain `def` is run in an external threadpool that is awaited; blocking or CPU-bound work inside an `async def` blocks the server.
- FastAPI has no built-in batching; use BentoML if you need adaptive batching.

## Checked
Method: docs-checked 2026-11-09 against the BentoML Services and Adaptive batching pages and the FastAPI Async and Lifespan Events pages (downloaded HTML, searched and read the sections above). Dropped the resources/traffic example values, bentoml build/containerize commands, uvicorn worker memory advice, readiness/liveness and image-pinning guidance, and the joblib FastAPI example, none of which were confirmed.
