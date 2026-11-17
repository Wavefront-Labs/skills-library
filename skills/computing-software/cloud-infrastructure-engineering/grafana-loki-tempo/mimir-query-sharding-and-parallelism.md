---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimir-query-sharding-and-parallelism
name: mimir-query-sharding-and-parallelism
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [query-sharding, mimir, query-frontend, split-queries-by-interval, results-cache, sharded-queries]
level: practitioner
status: docs-checked
description: "Speed up heavy PromQL in Mimir with query-frontend query sharding, interval splitting and the results cache, and verify sharding from query logs."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/query-sharding/", "https://grafana.com/docs/mimir/latest/references/architecture/components/query-frontend/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: faster dashboards on large series counts.

The query-frontend splits long-range queries by time (default interval 24 h, `-query-frontend.split-queries-by-interval`), then splits each shardable portion into `-query-frontend.query-sharding-total-shards` partial queries (each selects `__query_shard__="N_of_M"`) that run in parallel on queriers; the frontend aggregates the results. Sharding applies to the `query` and `query_range` APIs only.

Enable and tune:
```yaml
frontend:
  parallelize_shardable_queries: true
  cache_results: true
limits:
  query_sharding_total_shards: 16
  query_sharding_max_sharded_queries: 128
  split_queries_by_interval: 24h
```
The documented defaults are 16 total shards, 128 max sharded queries and `cache_results` false. The max-sharded-queries limit applies after time splitting (128 over 8 daily legs is 16 partial queries per day). The results cache is backed by Memcached (`frontend.results_cache`).

Shardable: associative aggregations (`sum`, `min`, `max`, `count`, `avg`, `topk`, `bottomk`). Not shardable: `absent`, `absent_over_time`, `histogram_quantile`, `sort`, `sort_desc`; the inner part of such a query may still shard (for example `histogram_quantile(0.99, sum by(le) (rate(m[1m])))`).

Gotchas
- Sharding raises load on queriers, ingesters, store-gateways and the chunk/index caches. The docs recommend multiplying `-querier.max-query-parallelism` by the shard count.
- After enabling it in microservices mode the query-frontend evaluates the aggregation, so set the PromQL engine flags there too: `-querier.max-concurrent`, `-querier.timeout`, `-querier.max-samples`, `-querier.default-evaluation-interval`, `-querier.lookback-delta`.
- Experimental cardinality estimation: `-query-frontend.query-sharding-target-series-per-shard` plus the `query-frontend.results-cache.*` flags; it only ever reduces the shard count.

## Verify
The query-frontend's query stats log has a `sharded_queries` field: `0` means not shardable or sharding disabled, a multiple of the shard count means sharding worked. Success ratio:
`sum(rate(cortex_frontend_query_sharding_rewrites_succeeded_total[$__rate_interval])) / sum(rate(cortex_frontend_query_sharding_rewrites_attempted_total[$__rate_interval]))`. `cortex_frontend_sharded_queries_per_query` shows sub-queries per query.

## Checked
2026-11-03. Confirmed against the Mimir query sharding page, query-frontend page and the configuration parameters reference (defaults). Removed: `max_total_query_length: 12000h`, the memcached address example, the `Server-Timing` header claim, the per-tenant override tip and the cache-key remark.
Method: documentation only; no commands were run.
