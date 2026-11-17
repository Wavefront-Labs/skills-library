---
id: computing-software.ai-ml-engineering.llama-cpp.server-parallel-slots-batching
name: server-parallel-slots-batching
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, parallel-slots, continuous-batching, kv-unified, n-parallel]
level: practitioner
status: docs-checked
description: "Configure concurrent requests with -np slots, continuous batching and the unified KV buffer."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parallel slots and continuous batching

llama-server decodes several requests at once, each in a slot.

- `-np, --parallel N`: number of slots. Default `-1` means auto (env `LLAMA_ARG_N_PARALLEL`).
- `-cb, --cont-batching` / `-nocb`: continuous (dynamic) batching, enabled by default.
- `-kvu, --kv-unified` / `-no-kvu`: one unified KV buffer shared by all sequences; enabled by default when the slot count is auto.
- `--kv-unified-per-slot N`: context limit per slot. When set without `-c`, the shared KV pool is sized to `n_parallel * N`.
- `-c, --ctx-size N`: total context (default 0, from the model).
- `-b, --batch-size` (logical, default 2048) and `-ub, --ubatch-size` (physical, default 512).
- `--threads-http N`: threads for HTTP handling (default -1).

`GET /props` shows `total_slots`; `GET /metrics` (with `--metrics`) reports `llamacpp:requests_processing` and `llamacpp:requests_deferred` so you can see queueing.

Requests that use different `lora` configurations are not batched together, which can reduce performance. Multimodal projector offload is controlled separately by `--mmproj-offload`.

Docker compose style via environment: `LLAMA_ARG_MODEL`, `LLAMA_ARG_CTX_SIZE=4096`, `LLAMA_ARG_N_PARALLEL=2`, `LLAMA_ARG_ENDPOINT_METRICS=1`, `LLAMA_ARG_PORT=8080`.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: -np, -cb, -kvu, --kv-unified-per-slot, -c, -b, -ub and --threads-http names and defaults; GET /props total_slots; the two /metrics gauges and the --metrics flag; the lora batching note; the compose environment variable names. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
