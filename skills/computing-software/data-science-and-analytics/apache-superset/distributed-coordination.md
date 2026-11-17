---
id: computing-software.data-science-and-analytics.apache-superset.distributed-coordination
name: distributed-coordination
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [distributed-coordination, redis, locks, sentinel, signal-ttl]
level: advanced
status: docs-checked
description: "Configure DISTRIBUTED_COORDINATION_CONFIG in Superset with Redis or Valkey: cache classes, TTL defaults, socket timeouts and the database fallback."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move Superset locking and notifications off the metadata database.

`DISTRIBUTED_COORDINATION_CONFIG` is Flask-Caching style config in `superset_config.py`. The page shows `CACHE_TYPE` `RedisCache` (with `CACHE_REDIS_HOST`, `CACHE_REDIS_PORT`, `CACHE_REDIS_DB`, optional `CACHE_REDIS_PASSWORD`) and `RedisSentinelCache` (`CACHE_REDIS_SENTINELS`, `CACHE_REDIS_SENTINEL_MASTER`, `CACHE_REDIS_SENTINEL_PASSWORD`). TLS uses `CACHE_REDIS_SSL`, `CACHE_REDIS_SSL_CERTFILE`, `CACHE_REDIS_SSL_KEYFILE`, `CACHE_REDIS_SSL_CA_CERTS`.

It needs Redis or Valkey specifically: it uses Streams, pub/sub and `SET NX EX`, which general Flask-Caching backends lack. Task completion and abort signals travel over Redis Streams, so waiters wake on a signal instead of polling the metadata database; stream entries persist, so a late or reconnecting waiter still receives the signal.

Defaults:
- `DISTRIBUTED_COORDINATION_SIGNAL_TTL`: seconds, default 24 hours (86400). Each signal stream keeps only its latest entry and gets this TTL.
- `DISTRIBUTED_LOCK_DEFAULT_TTL`: 30 seconds; locks expire to avoid deadlocks from crashed processes, and individual acquisitions can override it.
- Socket timeouts: none by default. Override with `CACHE_REDIS_SOCKET_TIMEOUT` and `CACHE_REDIS_SOCKET_CONNECT_TIMEOUT` (seconds); they also apply to Sentinel node and resolved master connections.

Without this config ("database-only mode"), locking uses the KeyValue table with periodic cleanup of expired entries and notifications use database polling. Redis is recommended for production for lower latency and reduced database load.

Related: the experimental, default-off `SEMANTIC_LAYER_CONTAINMENT_CACHE` needs `SEMANTIC_LAYERS`, a provider that explicitly delegates containment caching, a persistent shared `DATA_CACHE_CONFIG` and Redis-backed `DISTRIBUTED_COORDINATION_CONFIG` on every web and worker process. The default `NullCache` data backend disables containment. The reader fence uses identity format v4, so existing v3 entries become cold misses and need no manual deletion. Monitor `semantic_cache.containment.fence_reject` during forced-refresh testing. A nonempty, valid host `metadata_cache_token` is required; missing, empty or invalid tokens bypass containment and run the provider. Roll back by disabling the flag, restarting every process and confirming `semantic_cache.containment.enabled` is zero.

## Checked

Confirmed against the Superset cache configuration page: backend classes, Redis/Valkey requirement, defaults, timeout behaviour, database fallback and the containment cache requirements. Added the config key names, TLS and Sentinel options, and rollback step from the page.

Method: docs-only read of cited pages, 2026-11-08
