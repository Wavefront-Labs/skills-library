---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.entity-cache-settings
name: entity-cache-settings
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, db-cache-ttl, db-update-frequency, mem-cache-size, kong-conf, caching]
level: advanced
status: docs-checked
description: "kong.conf settings that govern Kong's in-memory entity cache and database polling: mem_cache_size, db_cache_ttl, db_update_frequency, db_resurrect_ttl and the /cache endpoints."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/traditional-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entity cache settings

Nodes cache Services, Routes, Consumers, plugins, credentials and database misses in memory.

| Setting | Default | Meaning |
|---|---|---|
| `mem_cache_size` | `128m` | size of each of the two shared memory caches |
| `db_cache_ttl` | `0` | TTL in seconds for cached entities; `0` means never expire |
| `db_cache_neg_ttl` | falls back to `db_cache_ttl` | TTL for cached misses |
| `db_update_frequency` | `5` | seconds between polls for entity changes |
| `db_update_propagation` | `0` | extra delay for replicas in other datacentres; set to the maximum replication lag with PostgreSQL read replicas |
| `db_resurrect_ttl` | `30` | seconds stale entities stay usable if refresh fails |
| `db_cache_warmup_entities` | `services` | entities preloaded at startup |

Because nodes poll, a change made on one node reaches the others only after their next poll: a cluster is eventually consistent. A single node sees its own changes immediately.

Cache Admin API (the `/cache` endpoint):
- `/cache/{key}`: inspect a cached value
- `/cache/{key}`: purge a cached value
- `/cache`: purge the node's whole cache

Purging a warm cache on a busy node can cause a cache stampede.

## Checked

2026-11-04. Confirmed against the Traditional mode page and kong.conf.default: cached entity types, the defaults and meanings in the table, eventual consistency, single-node immediacy, the `/cache` paths and the stampede warning. Removed the HTTP verbs for the `/cache` endpoints, which the page does not state.
Method: documentation only; no commands were run.
