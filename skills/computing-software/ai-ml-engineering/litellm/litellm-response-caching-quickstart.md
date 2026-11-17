---
id: computing-software.ai-ml-engineering.litellm.litellm-response-caching-quickstart
name: litellm-response-caching-quickstart
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, caching, cache-params, cache-ping]
level: intro
status: docs-checked
description: "Enable response caching in the proxy with cache: True, choose a backend with cache_params.type, and test it with /cache/ping."
sources:
  - https://docs.litellm.ai/docs/proxy/caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse LLM responses to save cost and latency. This is response caching, not provider prompt caching.

Backends (`cache_params.type`): `redis` (also Valkey, ElastiCache, Memorystore), `redis-semantic`, `valkey-semantic`, `qdrant-semantic`, `s3`, `gcs`, `local` (in memory), `disk`.

Redis is the right default beyond a single worker. An in-memory cache lives inside one worker, so four workers keep four caches and the hit rate drops roughly by the worker count.

Exact-match caches (redis, s3, gcs, local, disk) key on a hash of the whole request, so any change is a miss. Semantic caches embed the prompt and serve the closest match above a threshold; they suit single-shot prompts and go badly wrong on agentic traffic.

Quick start:

```
litellm_settings:
  cache: True   # defaults to a redis cache
```

```
REDIS_URL='redis://username:password@hostname:port/database'
# or
REDIS_HOST='...'
REDIS_PORT='...'
REDIS_PASSWORD='...'
```

Send the same request twice. The second response is served from the cache and carries an `x-litellm-cache-key` header, which you can pass to /cache/delete.

With `cache: True` and no `supported_call_types`, caching covers /chat/completions, /completions, /embeddings, /audio/transcriptions, /rerank, /v1/responses and /v1/messages. On /v1/responses each turn is its own entry, because a request with `previous_response_id` has a different key.

Local options:

```
litellm_settings:
  cache: True
  cache_params:
    type: disk
    disk_cache_dir: /tmp/litellm-cache   # default ./.litellm_cache
```

Neither `local` nor `disk` is shared between workers or replicas; use them for development.

Verify: `/cache/ping` returns `"status": "healthy"`, the cache_type and `"set_cache_response": "success"`. The cache client's per-command timeout is `cache_params.socket_timeout` (default 5 s), not REDIS_SOCKET_TIMEOUT.

## Checked

2026-11-03. Confirmed on the caching page (docs.litellm.ai/docs/proxy/caching): backend types, per-worker in-memory caches, exact-match versus semantic caches, cache: True defaulting to Redis, x-litellm-cache-key, the default supported call types, previous_response_id behaviour, disk_cache_dir, /cache/ping output and the socket_timeout default of 5 s.

Method: documentation only; no commands were run.
