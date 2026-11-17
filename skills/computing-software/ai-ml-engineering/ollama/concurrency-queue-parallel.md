---
id: computing-software.ai-ml-engineering.ollama.concurrency-queue-parallel
name: concurrency-queue-parallel
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [num-parallel, max-queue, max-loaded-models, concurrency, ollama-num-parallel]
level: advanced
status: docs-checked
description: "Size concurrency with OLLAMA_NUM_PARALLEL, OLLAMA_MAX_LOADED_MODELS and OLLAMA_MAX_QUEUE and read the memory cost."
sources:
  - https://docs.ollama.com/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve several requests or models at once without running out of memory.

Documented behaviour and defaults:

- `OLLAMA_MAX_LOADED_MODELS`: how many models can be loaded at once. Default is 3 times the number of GPUs, or 3 for CPU. If a new model would not fit, an idle one is unloaded first. On Windows with Radeon GPUs the default is 1 because of current limits.
- `OLLAMA_NUM_PARALLEL`: parallel requests per loaded model. Default is 1.
- `OLLAMA_MAX_QUEUE`: maximum queued requests when busy. Default 512. Beyond that the server returns HTTP 503 (overloaded).

Memory: required RAM scales by `OLLAMA_NUM_PARALLEL` times `OLLAMA_CONTEXT_LENGTH`, so doubling parallelism doubles the context allocation.

Example:

```
OLLAMA_NUM_PARALLEL=4 OLLAMA_MAX_LOADED_MODELS=2 ollama serve
```

Multi-GPU placement: when loading a model, Ollama loads it on a single GPU if it fits there, which the FAQ says reduces inter-GPU traffic; if it does not fit, it spreads across all GPUs.

Watch the result with `ollama ps`. A 429 or 503 from the API is described on the errors page (see the error handling skill).

## Checked

2026-11-03. `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_QUEUE` defaults, 503 on overload, Windows Radeon default and multi-GPU placement confirmed against the FAQ (docs.ollama.com/faq). Nothing removed.

Method: documentation only; no commands were run.
