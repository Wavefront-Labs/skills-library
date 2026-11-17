---
id: computing-software.cloud-infrastructure-engineering.thanos.store-index-cache-memcached
name: store-index-cache-memcached
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, memcached, index-cache, jump-hash]
level: advanced
status: docs-checked
description: "Use memcached as the Thanos Store index cache, including addressing rules, item size and the async circuit breaker."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store memcached index cache

Select memcached through `--index-cache.config-file` or `--index-cache.config`:

```yaml
type: MEMCACHED
config:
  addresses: ["dnssrvnoa+memcached.monitoring.svc:11211"]
  timeout: 500ms
  max_item_size: 1MiB
enabled_items: []
ttl: 24h
```

**Required:** `addresses`, resolved by the DNS service discovery provider. If your service supports auto-discovery (Amazon ElastiCache style), set `auto_discovery: true` and point at any one server.

**Sharding rule.** The client shards with a jump hash, so servers must not sit behind a load balancer, and scale-up or down must add or remove at the end of the list. In Kubernetes the docs suggest a StatefulSet, a headless service, and `dnssrvnoa+` discovery.

**Optional settings:** `timeout`, `max_idle_connections`, `max_async_concurrency`, `max_async_buffer_size`, `max_get_multi_concurrency` (0 is unlimited), `max_get_multi_batch_size` (0 is unlimited), `dns_provider_update_interval`, and `max_item_size`. Set `max_item_size` equal to the memcached `-I` flag (default 1MB) so Thanos does not waste round trips on oversized items.

**Circuit breaker** (`set_async_circuit_breaker_config`): states are closed, half-open and open. It opens when requests exceed `min_requests` and either `consecutive_failures` or `failure_percent` is hit; after `open_duration` (0 means 60 seconds) it lets `half_open_max_requests` through.

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
