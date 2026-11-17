---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.limit-count-redis-policy
name: limit-count-redis-policy
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, limit-count, redis, redis-cluster, redis-sentinel, policy, rate-limiting]
level: advanced
status: docs-checked
description: "Share APISIX limit-count counters across gateway nodes using the redis, redis-cluster or redis-sentinel policy, with required fields, defaults and sync_interval."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/limit-count.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# limit-count Redis policy

`policy` defaults to `local` (counters per gateway instance). Use `redis`, `redis-cluster` or `redis-sentinel` for a shared quota.

Required per policy:
- `redis`: `redis_host`.
- `redis-cluster`: `redis_cluster_nodes` (at least one address) and `redis_cluster_name`.
- `redis-sentinel`: `redis_sentinels` (items with `host` and `port`) and `redis_master_name`.

Defaults:
- `redis_port` 6379, `redis_database` 0.
- `redis_timeout` 1000 ms; `redis_keepalive_pool` 100 (redis and redis-cluster).
- `redis_keepalive_timeout` 10000 ms (60000 for sentinel).
- `redis_ssl`, `redis_ssl_verify`: false (redis policy only); `redis_server_name` defaults to `redis_host`.
- `redis_role` for sentinel: `master` (or `slave`).
- `redis_password` and `sentinel_password` are stored encrypted.

`sync_interval` (Redis policies only, APISIX 3.18.0 and later): -1 or at least 0.1, and it must be less than a numeric `time_window`. It batches counter syncing instead of calling Redis per request.

Example fragment:

```json
{"limit-count":{"count":100,"time_window":60,"policy":"redis","redis_host":"<REDIS_HOST>","redis_password":"<REDIS_PASSWORD>"}}
```

If the backend fails, the plugin returns 500 unless `allow_degradation` is true, in which case requests pass without limiting.

## Checked

2026-11-04. Confirmed against the APISIX limit-count plugin page: required attributes per policy, port, database, timeout, keepalive pool and timeout defaults (including 60000 for sentinel), redis_ssl and redis_server_name, redis_role, encrypted password fields, sync_interval range and its 3.18.0 gate. Added the version gate.

Method: documentation only; no commands were run.
