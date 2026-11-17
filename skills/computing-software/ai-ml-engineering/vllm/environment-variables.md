---
id: computing-software.ai-ml-engineering.vllm.environment-variables
name: environment-variables
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [env-vars, environment-variables, vllm-port, kubernetes]
level: practitioner
status: docs-checked
description: "Understand vLLM environment variables, the VLLM_PORT and VLLM_HOST_IP trap and the Kubernetes service naming clash."
sources:
  - https://docs.vllm.ai/en/latest/configuration/env_vars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure vLLM through environment variables without hitting the documented traps.

Most vLLM-specific variables are prefixed `VLLM_`. A handful of standard names are also read directly when set: `CUDA_VISIBLE_DEVICES`, `MAX_JOBS`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_ENDPOINT_URL`, `DO_NOT_TRACK` and `NO_COLOR`. The complete list is on the Environment Variables page of the docs.

Trap 1: `VLLM_PORT` and `VLLM_HOST_IP` set the port and IP for vLLM's internal usage. They are not the API server's address. Starting the server with `--host $VLLM_HOST_IP` and `--port $VLLM_PORT` will not work; use `--host` and `--port` with their own values.

Trap 2 (Kubernetes): do not name the Kubernetes Service `vllm`. Kubernetes injects environment variables for each service using the capitalised service name as a prefix (for example `VLLM_PORT`), which can then conflict with vLLM's own variables.

Other variables documented elsewhere in the docs:
- `VLLM_CACHE_ROOT` is the root directory for vLLM cache files (default `~/.cache/vllm` unless `XDG_CACHE_HOME` is set).
- `VLLM_FORCE_AOT_LOAD=1` forces AOT-compiled models to load from disk; a load failure is a hard error (ignored when `VLLM_USE_AOT_COMPILE` is disabled).
- `VLLM_API_KEY` is the API key for the vLLM API server.
- `VLLM_CPU_KVCACHE_SPACE` sets CPU-backend KV cache in GiB (default 0, no override).
- `CUDA_VISIBLE_DEVICES` selects GPUs; prefer it over calling CUDA functions before creating `LLM`.

## Checked

2026-11-03. Confirmed against the Environment Variables page (docs.vllm.ai/en/latest/): the VLLM_PORT/VLLM_HOST_IP warning, the Kubernetes service-name warning, standard names read directly, cache root and AOT variables. Reworded VLLM_CACHE_ROOT, VLLM_FORCE_AOT_LOAD and VLLM_API_KEY to what the page states; removed the unconfirmed claim that the list is built from a named source file.

Method: documentation only; no commands were run.
