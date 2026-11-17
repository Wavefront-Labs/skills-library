---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-caching-and-query-performance
name: tempo-caching-and-query-performance
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tempo-caching, tempo, memcached, bloom-filter-cache, parquet-footer-cache, query-frontend-sharding, search-performance]
level: practitioner
status: docs-checked
description: "Speed up Tempo queries with cache roles in Memcached, query-frontend job settings and querier concurrency, and monitor cache hit ratio."
sources: ["https://grafana.com/docs/tempo/latest/operations/caching/", "https://grafana.com/docs/tempo/latest/operations/backend_search/", "https://grafana.com/docs/tempo/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: lower latency and object storage read cost.

Caches are configured under the top-level `cache:` block; every cache needs at least one unique role. Memcached and Redis (experimental) are supported.
```yaml
cache:
  caches:
    - roles: [bloom, parquet-footer, parquet-column-idx, parquet-offset-idx, trace-id-index]
      memcached:
        host: memcached.tempo.svc
        service: memcached-client
        timeout: 500ms          # default 100ms
    - roles: [parquet-page]     # very high volume, give it its own pool
      memcached:
        host: memcached-pages.tempo.svc
```
Roles: `bloom`, `trace-id-index`, `parquet-footer`, `parquet-column-idx`, `parquet-offset-idx`, `parquet-page` (caches most Parquet reads), `frontend-search`. `store_probability` (0 to 1) thins what is written.

Search tuning (the docs prefer scaling queriers horizontally and keeping about two query-frontend replicas, scaled vertically):
```yaml
query_frontend:
  max_outstanding_per_tenant: 2000   # beyond this a tenant gets HTTP 429
  search:
    concurrent_jobs: 1000            # default 1000
    target_bytes_per_job: 104857600  # default; docs suggest 100-200 MB
    default_result_limit: 20
  trace_by_id:
    query_shards: 50                 # deprecated, used when blocks_per_shard is 0
querier:
  max_concurrent_queries: 20         # default 20
```
Maximum jobs for one query is limited by `concurrent_jobs` and by `queriers * querier.max_concurrent_queries * query_frontend.max_batch_size`. The docs advise against changing `max_batch_size` from its default of 7 and say the default `max_retries` of 2 is good. Raising `concurrent_jobs` also needs a higher `max_outstanding_per_tenant`, or search requests fail with 429. All search needs vParquet block formats; dedicated attribute columns also speed up search.

Gotchas
- Memcached refuses new connections at its default limit of 1024; watch `tempo_memcache_request_duration_seconds_count` by `status_code`.
- The bloom cache working set is the total size of all bloom filters; shrink it with `storage.trace.cache_min_compaction_level` and `cache_max_block_age`, guided by `tempo-cli list cache-summary <tenant-id>`.
- Scale a cache when latency hits the cache timeout or evictions are high; lower-level caches (`bloom`, `parquet-page`, `parquet-footer`) should see high hit rates.

## Verify
Hit ratio per role: `sum(rate(tempodb_cache_requests_total{role="parquet-page",outcome="hit"}[5m])) / sum(rate(tempodb_cache_requests_total{role="parquet-page"}[5m]))`. `tempodb_cache_store_size_bytes` (by `role`) shows item sizes.

## Checked
2026-11-03. Confirmed against the Tempo caching page, the Tune search performance page and the configuration reference (cache block, query_frontend search defaults, storage.trace cache options) and tempo-cli list cache-summary. Removed: `prefer_self`, the "caching does not apply to recent ingester data" and time-bounded search claims, the curl metrics grep, and the `parquet-footer`-only role list (role set updated).
Method: documentation only; no commands were run.
