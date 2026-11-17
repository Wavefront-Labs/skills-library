---
id: computing-software.cloud-infrastructure-engineering.thanos.store-index-cache-in-memory
name: store-index-cache-in-memory
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, index-cache, in-memory-cache, index-cache-size]
level: practitioner
status: docs-checked
description: "Configure the default in-memory index cache for postings and series lookups in Thanos Store Gateway."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store in-memory index cache

The index cache speeds up postings and series lookups from block indexes. Three types exist: in-memory (the default), memcached and redis.

Size the default cache with a flag:

```
thanos store --index-cache-size=250MB ...
```

`--index-cache-size` is ignored if `--index-cache.config` or `--index-cache.config-file` is given. The config form is:

```yaml
type: IN-MEMORY
config:
  max_size: 250MB
  max_item_size: 125MB
enabled_items: []
ttl: 0s
```

All settings are optional.
- `max_size`: overall maximum bytes; needs a unit such as `250MB`.
- `max_item_size`: maximum size of a single item.
- `enabled_items`: choose what to cache; supported values are `Postings`, `Series` and `ExpandedPostings`. Empty means all are cached.
- `ttl`: does nothing for the in-memory cache.

Related flags from the same page: `--chunk-pool-size` (default 2GB) bounds bytes reserved for reusing chunk buffers, and `--store.grpc.series-max-concurrency` (default 20) bounds concurrent Series calls.

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
