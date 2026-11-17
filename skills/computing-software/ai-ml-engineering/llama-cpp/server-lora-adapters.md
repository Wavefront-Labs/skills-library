---
id: computing-software.ai-ml-engineering.llama-cpp.server-lora-adapters
name: server-lora-adapters
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, lora, lora-adapters, lora-scale, adapter-api]
level: advanced
status: docs-checked
description: "Load LoRA adapters at start-up and change their scale globally or per request through the server API."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LoRA adapters on the server

Load adapters at start with `--lora my_adapter_1.gguf --lora my_adapter_2.gguf` (the option table also says `--lora FNAME` accepts comma-separated values), or `--lora-scaled FNAME:SCALE,...`. By default all adapters load with scale 1. Add `--lora-init-without-apply` to load them without applying them (scale 0) and apply later via `POST /lora-adapters`.

`GET /lora-adapters` returns the loaded adapters:

```json
[{"id": 0, "path": "my_adapter_1.gguf", "scale": 0.0},
 {"id": 1, "path": "my_adapter_2.gguf", "scale": 0.0}]
```

`POST /lora-adapters` sets the global scales using the ids from the GET call:

```json
[{"id": 0, "scale": 0.2}, {"id": 1, "scale": 0.8}]
```

To disable an adapter, remove it from the list or set its scale to 0. A disabled adapter shows scale 0.

Per request, pass `lora` to `/completion`: `[{"id": 0, "scale": 0.5}, {"id": 1, "scale": 1.1}]`. Each object needs `id` and `scale`. An adapter not listed gets scale `0.0`. The global scale is overwritten by the request's `lora` field. Requests with different LoRA configurations are not batched together, which may degrade performance.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the llama.cpp server README option table, `GET/POST /lora-adapters` and the `/completion` `lora` option. Removed: claims that adapters must be GGUF, that adapters are not merged so mmap still works, and the `llama-export-lora` pointer; the page does not state them.
