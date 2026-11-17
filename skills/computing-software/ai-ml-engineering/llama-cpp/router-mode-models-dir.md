---
id: computing-software.ai-ml-engineering.llama-cpp.router-mode-models-dir
name: router-mode-models-dir
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, router-mode, models-dir, models-max, model-routing]
level: advanced
status: docs-checked
description: "Run llama-server in router mode to load and unload several models and route requests by model name."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Router mode

Start `llama-server` with no model to get a router that forwards each request to a model instance it spawns.

Model sources:

1. The cache (controlled by `LLAMA_CACHE`); add models with `llama-server -hf <user>/<model>[:quant]`, then restart the server.
2. A directory: `--models-dir /path/to/models`.
3. A preset file: `--models-preset /path/to/presets.ini`.

Directory layout: single files sit directly in the folder. Multimodal models need a subfolder holding the model and an `mmproj*.gguf` file (the file name must start with `mmproj`). Multi-shard models go in a subfolder with all shards.

Routing:

- POST endpoints use the `"model"` field in the JSON body.
- GET endpoints (`/props`, `/metrics`) use the `model` query parameter, URL-encoded.
- `/v1/realtime` also uses the `model` query parameter.

Flags:

- `--models-max N`: models loaded at once, default 4; `0` is unlimited. Least recently used models are evicted.
- `--no-models-autoload`: stop automatic loading; `?autoload=true|false` overrides per request.
- `--models-memory-margin N`: MiB of device memory to keep free.

Default arguments given to the router, for example `-ctx 8192 -np 2`, are inherited by instances, as are environment variables. Host, port, API key, HF repo and alias are controlled by the router.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: router start, model sources, directory layout and the mmproj naming rule, routing by model field and query parameter, --models-max default 4, autoload flags, --models-memory-margin, inherited arguments and the router-controlled options. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
