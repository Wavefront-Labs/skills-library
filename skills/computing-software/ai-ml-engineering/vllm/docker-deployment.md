---
id: computing-software.ai-ml-engineering.vllm.docker-deployment
name: docker-deployment
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [docker, vllm-openai, non-root, compile-cache, ipc-host]
level: practitioner
status: docs-checked
description: "Run vLLM with the vllm/vllm-openai image: cache volumes, recipe configs and the non-root user options."
sources:
  - https://docs.vllm.ai/en/latest/deployment/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run the OpenAI server image with persisted caches and, optionally, as a non-root user.

Persist the compile cache. Mounting the Hugging Face cache keeps weights, but each new container starts with an empty `VLLM_CACHE_ROOT` (default `~/.cache/vllm`) and recompiles. Mount a named volume:

```bash
docker run --rm --gpus all   -v ~/.cache/huggingface:/root/.cache/huggingface   -v vllm-cache:/root/.cache/vllm   -p 8000:8000   vllm/vllm-openai:latest meta-llama/Llama-3.1-8B-Instruct
```

Recipe config: mount `config.yaml` and `env.sh` read-only, add `--ipc=host`, `--entrypoint /bin/bash`, and run `-lc 'source /recipe/env.sh && exec vllm serve --config /recipe/config.yaml'`.

Non-root: the CUDA image runs as root for backward compatibility but is prepared for the built-in `vllm` user (UID 2000, GID 0): add `--user 2000:0`. Mount cache and model volumes at writable paths under that user's home directory instead of `/root`, and make the mounted directory writable by group 0.

Opt-in image target:

```bash
docker build --target vllm-openai-nonroot -t vllm-openai-nonroot:local -f docker/Dockerfile .
```

It also supports OpenShift-style arbitrary UIDs when the runtime UID belongs to group 0. In Kubernetes set the security context `runAsNonRoot: true`, `runAsUser` to the assigned UID, `runAsGroup: 0`, `fsGroup: 0`, and keep mounted paths group-0 writable.

## Checked

2026-11-03. Confirmed against the Docker deployment page (docs.vllm.ai/en/latest/): cache volume, recipe config mounting, non-root user, nonroot build target and OpenShift notes.

Method: documentation only; no commands were run.
