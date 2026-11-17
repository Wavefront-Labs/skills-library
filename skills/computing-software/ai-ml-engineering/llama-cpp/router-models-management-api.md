---
id: computing-software.ai-ml-engineering.llama-cpp.router-models-management-api
name: router-models-management-api
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, models-api, model-load-unload, model-download, sse-events]
level: advanced
status: docs-checked
description: "Manage router models over HTTP: list, load, unload, download with SSE progress, and delete."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Router model management API

- `GET /models`: list models in the cache with a `status` object (`value` is one of unloaded, loading, loaded, sleeping, downloading, incomplete). `?reload=1` refreshes the list.
- `POST /models/load` with `{"model": "ggml-org/gemma-3-4b-it-GGUF:Q4_K_M"}` returns `{"success": true}`.
- `POST /models/unload` with the same body unloads it. Sending this for an active download pauses it; partial files are kept and the model is listed as "incomplete" until posted again.
- `GET /models/sse`: real-time events (`model_status`, `download_progress`, `model_remove`, `model_memory`, `models_reload`).
- `POST /models`: start a non-blocking download.
- `DELETE /models?model={name}`: delete a cached model; to cancel a download and drop its files, use this too.

Download procedure:

1. `POST /models` with `{"model": "...", "sidecars": ["mmproj", "mtp"]}`. Sidecar kinds are `mmproj` and the draft heads `mtp`, `dflash`, `eagle3`, `dspark`; the default is `["mmproj"]`.
2. Subscribe to `/models/sse` and wait for `download_finished` or `download_failed`.
3. Call `GET /models` to refresh the list.

A failed validation returns HTTP 400 "model validation failed, unable to download".

Delete rules: only cached models can be deleted, not models in a preset. Add `&sidecar={kind}` to remove one sidecar while keeping the model (the model must not be running). A successful delete emits the SSE event `model_remove`. Files another cached quant of the repo still loads are kept.

`--models-memory-margin N` (MiB of device memory to keep free per device) also unloads least-recently-used idle models until a new one fits. Measurements appear in the `memory` field of each model in `GET /models` (`status`: unmeasured, measuring, measured, failed) and as `model_memory` SSE events.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the llama.cpp server README sections for the router mode `/models` endpoints, Memory-based unloading and the option table. Reworded the `memory` field claim to what the page states.
