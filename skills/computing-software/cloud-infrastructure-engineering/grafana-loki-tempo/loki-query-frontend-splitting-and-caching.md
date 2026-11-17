---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-query-frontend-splitting-and-caching
name: loki-query-frontend-splitting-and-caching
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-query-frontend, loki, query-scheduler, split-queries-by-interval, results-cache, parallelism, max-query-parallelism]
level: practitioner
status: docs-checked
description: "Configure the Loki query frontend to split queries by interval, cache results and control parallelism."
sources: ["https://grafana.com/docs/loki/latest/operations/caching/", "https://grafana.com/docs/loki/latest/configure/#limits_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: faster dashboards and bounded querier load.

```yaml
limits_config:
  split_queries_by_interval: 1h     # default
  max_query_parallelism: 32         # default
query_range:
  align_queries_with_step: true     # default false
  cache_results: true               # default false
  results_cache:
    cache:
      memcached_client:
        addresses: dns+memcached.loki.svc:11211
frontend:
  max_outstanding_per_tenant: 2048  # default
  compress_responses: true          # default
```
The query frontend splits a long range into per-interval subqueries run by queriers, and caches results. The `results_cache` is consulted by query frontends; incomplete cached results are completed by sub-queries to queriers.

Caches (from the caching page)
- `query_range.results_cache` covers metric and log queries. Five more query-type caches exist (`index_stats_results_cache`, `volume_results_cache`, `instant_metric_results_cache`, `series_results_cache`, `label_results_cache`), each enabled with its own `cache_*_results` flag. If one is enabled with an empty config it falls back to `results_cache`.
- The chunks cache is `chunk_store_config.chunk_cache_config`, consulted by queriers.
- Backends: Memcached (recommended for production, shared across replicas), Redis, or an in-process embedded cache. Configure one backend per cache; configuring both Memcached and Redis for the same cache stops Loki starting. With none configured, Loki enables the embedded cache for chunks and results caches.
- Index caching is not needed with TSDB.
- The docs recommend Memcached with at least three replicas; with the Helm chart set `chunksCache.enabled`, `resultsCache.enabled` and their `addresses`.

Gotchas
- Queriers need `frontend_worker.frontend_address` (or `scheduler_address`) to pull work from the frontend.
- `align_queries_with_step` is off by default.

## Verify
Run the same range query twice from Grafana pointed at the query frontend; the second run should be served partly from cache (inspect your cache metrics).

## Checked
2026-11-03. Confirmed against the Loki configuration reference (defaults, frontend and frontend_worker fields) and the "Configure caches" page. Removed: `max_query_length: 721h` (docs default is `30d1h`, now omitted), the 1h to 24h interval advice, the unaligned-step cache claim, the metric names `loki_query_frontend_queries_total` and `cortex_cache_hits`, and "point Grafana at the frontend" (not stated on the pages read).
Method: documentation only; no commands were run.
