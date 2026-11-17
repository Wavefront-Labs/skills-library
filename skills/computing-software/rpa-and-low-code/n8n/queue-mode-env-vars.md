---
id: computing-software.rpa-and-low-code.n8n.queue-mode-env-vars
name: queue-mode-env-vars
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, queue-mode, redis, workers, multi-main, bull]
level: advanced
status: docs-checked
description: "Queue mode environment variables for n8n: Redis connection, worker lock and health-check settings, webhook response relay limits and multi-main leader keys."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/queue-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tune queue mode, where workers pull jobs from Redis for the best scalability.

## Core variables (default)
- `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS` (`false`): run manual executions on workers instead of main.
- `QUEUE_BULL_PREFIX`, `QUEUE_BULL_REDIS_DB` (0), `_HOST` (`localhost`), `_PORT` (6379), `_USERNAME` (needs Redis 6+; leave unset for older), `_PASSWORD`, `QUEUE_BULL_REDIS_TIMEOUT_THRESHOLD` (10000 ms), `QUEUE_BULL_REDIS_TLS` (false), `QUEUE_BULL_REDIS_DUALSTACK` (false).
- `QUEUE_BULL_REDIS_CLUSTER_NODES`: comma-separated `host:port` list. When set in queue mode (`EXECUTIONS_MODE = queue`) n8n creates a Redis Cluster client and ignores host and port.
- `QUEUE_HEALTH_CHECK_ACTIVE` (false) and `QUEUE_HEALTH_CHECK_PORT` (5678; change it on a port conflict when starting a worker).
- `QUEUE_WORKER_LOCK_DURATION` (60000 ms lease), `QUEUE_WORKER_LOCK_RENEW_TIME` (10000), `QUEUE_WORKER_STALLED_INTERVAL` (30000; 0 never checks).
- Deprecated: `QUEUE_WORKER_TIMEOUT` (use `N8N_GRACEFUL_SHUTDOWN_TIMEOUT`); `QUEUE_WORKER_MAX_STALLED_COUNT` has no effect since 2.0.

## Webhook responses
A worker returns a webhook response to main inside a queue message. `N8N_WEBHOOK_RESPONSE_RELAY_SIZE_MAX` (64 MiB) caps it; budget about 1.5 times that per in-flight response in Redis memory. `N8N_WEBHOOK_RESPONSE_RELAY_OFFLOAD_ENABLED` (false) stores larger bodies in binary data storage instead of failing the node; it needs a storing `N8N_DEFAULT_BINARY_DATA_MODE` (`filesystem`, `database`, `s3`, `azure`) readable by every instance, and every main and webhook instance on 2.34.0 or later before enabling it on workers.

## Multi-main (license required)
`N8N_MULTI_MAIN_SETUP_ENABLED` (false), `N8N_MULTI_MAIN_SETUP_KEY_TTL` (10 s leader key), `N8N_MULTI_MAIN_SETUP_CHECK_INTERVAL` (3 s).

## Checked
Method: docs-checked 2026-11-09 against the n8n "Queue mode environment variables" page (docs.n8n.io, read in full).
Nothing removed; every variable name, default and note matches the page.
