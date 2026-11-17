---
id: computing-software.cloud-infrastructure-engineering.thanos.query-frontend-caching
name: query-frontend-caching
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query-frontend, results-cache, memcached, response-cache-config]
level: advanced
status: docs-checked
description: "Configure in-memory, memcached or redis results caching and know what Query Frontend refuses to cache."
sources: ["https://thanos.io/tip/components/query-frontend.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Query Frontend results caching

Enable with `--query-range.response-cache-config-file` (or inline `--query-range.response-cache-config`). If cached results are incomplete, the frontend computes the missing sub-queries and runs them in parallel downstream. Queries can optionally align to their step to improve cacheability. Compress cached results with `--cache-compression-type` (supported values `snappy` and empty, which disables compression; the default is empty).

```yaml
type: IN-MEMORY
config:
  max_size: 512MB
  max_size_items: 0
  validity: 0s
```

If neither `max_size` nor `max_size_items` is set, the cache is not created; setting one leaves the other unlimited. In-memory (fifo), memcached and redis caches are supported. For memcached and redis, `expiration` set to 0s means a default of 24 hours.

**Never cached**
- Requests with deduplication disabled (`dedup=false`).
- Requests that specify store matchers.
- Responses with header `Cache-Control=no-store`.
- Partial responses and responses with other warnings.

## Checked

2026-11-03. Confirmed against the Thanos Query Frontend page (components/query-frontend.md): splitting, retries, limits and defaults, cache behaviour and exclusions, downstream tripper advice (max_idle_conns_per_host 100; 10 - 20% latency), forward-header, sharding flags, --cache-compression-type. Fixed: cache backends wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
