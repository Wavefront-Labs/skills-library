---
id: computing-software.cloud-infrastructure-engineering.thanos.store-index-cache-redis
name: store-index-cache-redis
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, redis-cache, index-cache, client-side-caching]
level: advanced
status: docs-checked
description: "Configure Redis as the Thanos Store index cache, with its defaults and client-side caching."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store Redis index cache

```yaml
type: REDIS
config:
  addr: "redis:6379"
  cache_size: 256MB
enabled_items: []
ttl: 24h
```

**Required:** `addr`.

**Defaults in the config reference**
- `dial_timeout: 5s`, `read_timeout: 3s`, `write_timeout: 3s`
- `max_get_multi_concurrency: 100`, `get_multi_batch_size: 100`
- `max_set_multi_concurrency: 100`, `set_multi_batch_size: 100`
- `max_async_buffer_size: 10000`, `max_async_concurrency: 20`
- circuit breaker: `half_open_max_requests: 10`, `open_duration: 5s`, `min_requests: 50`, `consecutive_failures: 5`, `failure_percent: 0.05`

**Fields.** `username` is only needed for Redis 6.0 and greater; `password`, `db`, and `master_name` (for Sentinel) are optional. `tls_enabled: true` plus `tls_config` (`ca_file`, `cert_file`, `key_file`, `server_name`, `insecure_skip_verify`, `min_version`) enables TLS; `cert_file` and `key_file` must be set together.

**Client-side caching.** `cache_size` sets the size of the in-memory client-side cache; it is enabled when non-zero. The docs highly recommend enabling it so the store does not repeatedly fetch the same keys from Redis.

`enabled_items` accepts `Postings`, `Series`, `ExpandedPostings`; `ttl` sets how long items live in Redis.

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
