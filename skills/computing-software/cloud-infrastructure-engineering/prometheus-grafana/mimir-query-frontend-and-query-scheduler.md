---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.mimir-query-frontend-and-query-scheduler
name: mimir-query-frontend-and-query-scheduler
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [mimir, mimir-query-frontend, mimir-query-scheduler, query-sharding, results-cache, grafana-mimir]
level: advanced
status: docs-checked
description: "Configure Grafana Mimir's query-frontend and query-scheduler: splitting by interval, query sharding, results cache, per-tenant queue fairness, scheduler discovery and scaling."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/components/query-frontend/", "https://grafana.com/docs/mimir/latest/references/architecture/components/query-scheduler/", "https://grafana.com/docs/mimir/latest/references/architecture/query-sharding/", "https://grafana.com/docs/mimir/latest/configure/configuration-parameters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mimir query-frontend and query-scheduler

**Goal:** fast, fair PromQL on Mimir for many tenants and long ranges.

## Roles and query flow
- **Query-frontend**: stateless primary entry point for the read path. It splits and shards queries or serves them from
  the cache, then enqueues them into a query-scheduler. Run at least two replicas for availability.
- **Query-scheduler**: stateless; keeps an in-memory queue of queries and hands them to queriers. Moving the queue out
  of the frontend lets query-frontends scale, stops ingester-only queries being hurt by degraded store-gateways (and
  vice versa), and gives tenant fairness through a simple round-robin across tenants with active queries.
- **Querier**: picks queries from the scheduler, executes them and returns results via the query-frontend to the client.

## Splitting, caching, sharding
- Splitting: long-range queries are split and run in parallel; the default interval is 24h
  (`limits.split_queries_by_interval`, flag `-query-frontend.split-queries-by-interval`; use a multiple of 24h to suit
  blocks). It protects queriers from out-of-memory on multi-day queries.
- Results cache: backed by Memcached (`frontend.results_cache.backend: memcached`; `-query-frontend.results-cache.backend`
  defaults to empty). `-query-frontend.cache-results` (`cache_results`) defaults to `false`, so enable it. TTL default
  `results_cache_ttl` is 1w.
- Step alignment: `-query-frontend.align-queries-with-step` (per tenant `align_queries_with_step`, default `false`)
  improves cacheability but, per the docs, violates PromQL conformance.
- Query sharding: `-query-frontend.parallelize-shardable-queries` (default `true` in the reference);
  `-query-frontend.query-sharding-total-shards` default 16; `-query-frontend.query-sharding-max-sharded-queries`
  default 128. It applies to the query and query_range APIs only. Associative aggregations (sum, min, max, count, avg)
  shard; `absent`, `absent_over_time`, `histogram_quantile`, `sort`, `sort_desc` do not, though their inner parts may.
  Shard selectors appear as `__query_shard__="N_of_M"`.
- With time splitting on, the max-sharded-queries limit applies to time splits first and then shards (128 / 8 days = 16
  partial queries per day for an 8 day query).
- After enabling sharding, set the PromQL-engine parameters (`-querier.max-concurrent`, `-querier.timeout`,
  `-querier.max-samples`, `-querier.default-evaluation-interval`, `-querier.lookback-delta`) on the query-frontend too.
  The docs also recommend multiplying `-querier.max-query-parallelism` (default 14) by the total shard count.

## Scheduler discovery and sizing
```yaml
frontend:
  scheduler_address: query-scheduler-headless.mimir.svc:9095   # DNS mode; host:port, DNS name resolving to all schedulers
  log_queries_longer_than: 10s                                  # default 0s (disabled)
query_scheduler:
  max_outstanding_requests_per_tenant: 100                      # default shown; in-flight requests above this get HTTP 429
```
- DNS mode: `-query-frontend.scheduler-address` on frontends and `-querier.scheduler-address` on queriers.
- Ring mode: set `-query-scheduler.service-discovery-mode=ring` and the `-query-scheduler.ring.*` flags on the
  scheduler, frontend and querier. Migrate by moving schedulers onto the ring first, confirming they all appear on the
  scheduler ring status page, then switching frontends and queriers.
- Run two query-scheduler replicas for availability; add more only for very high throughput, and keep the replica count
  at or below `-querier.max-concurrent` (default 8).
- Query-frontend `/ready` returns 200 only after it connects to at least one scheduler: use it as the load balancer
  health check.

## Verify sharding
- The query-frontend query stats log field `sharded_queries` is 0 when a query is not shardable or sharding is off, and
  a multiple of the shard count otherwise.
- `cortex_frontend_query_sharding_rewrites_succeeded_total` over `cortex_frontend_query_sharding_rewrites_attempted_total`
  gives the sharded ratio; `cortex_frontend_sharded_queries_per_query` is a histogram of sub-queries per query.

## Checked

Checked 2026-11-08 against the Mimir query-frontend, query-scheduler and query-sharding pages and the configuration
parameters reference (keys, flags, defaults). Removed because the pages do not state them: the memcached address and
port examples, `query_sharding_*` per-tenant advice values, `max_total_query_length: 12000h` (default is 0s), a 7d TTL
(default is 1w), the 800 outstanding-requests value (default is 100), queue-length metric names for autoscaling,
HPA or KEDA advice, and the dashboard checklist.
Method: docs-only read of cited pages, 2026-11-08
