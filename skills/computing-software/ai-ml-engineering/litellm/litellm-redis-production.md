---
id: computing-software.ai-ml-engineering.litellm.litellm-redis-production
name: litellm-redis-production
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, redis, redis-transaction-buffer, router-settings]
level: practitioner
status: docs-checked
description: "Configure Redis for multiple LiteLLM instances and enable the transaction buffer at very high traffic."
sources:
  - https://docs.litellm.ai/docs/proxy/prod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run Redis (7.0 or newer) as soon as you run more than one proxy instance. It shares rate limit counters, router state and the response cache; without it each instance enforces limits independently.

```
router_settings:
  routing_strategy: simple-shuffle   # default, recommended
  redis_host: os.environ/REDIS_HOST
  redis_port: os.environ/REDIS_PORT
  redis_password: os.environ/REDIS_PASSWORD
litellm_settings:
  cache: True
  cache_params:
    type: redis
    host: os.environ/REDIS_HOST
    port: os.environ/REDIS_PORT
    password: os.environ/REDIS_PASSWORD
```

Keep simple-shuffle for high traffic; usage-based routing adds Redis lookups to the request path.

Redis transaction buffer: at roughly 1000+ requests per second, or 10+ instances, spend tracking becomes a database bottleneck because every instance issues UPDATE/UPSERT statements against the same key, user and team rows. Buffer them in Redis:

```
general_settings:
  use_redis_transaction_buffer: true
```

Monitor with the Prometheus metrics `litellm_pod_lock_manager_size` (which pod holds the flush lock) and the gauges `litellm_in_memory_spend_update_queue_size` and `litellm_redis_spend_update_queue_size` (spend updates waiting).

Also from the prod page: bound database connections with `database_connection_pool_limit` sized as MAX_DB_CONNECTIONS / (instances x workers), default 10. With an autoscaler, the instance count in that formula is maxReplicas, not the pods running today.

## Checked

2026-11-03. Confirmed on the LiteLLM production page (docs.litellm.ai/docs/proxy/prod): Redis 7.0 or newer, the router_settings and cache_params Redis keys, simple-shuffle as the default for high traffic, use_redis_transaction_buffer at roughly 1000+ requests per second or 10+ instances, the three Prometheus metric names, and maxReplicas as the instance count in the pool formula.

Method: documentation only; no commands were run.
