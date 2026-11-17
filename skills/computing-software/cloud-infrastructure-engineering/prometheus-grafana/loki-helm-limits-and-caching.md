---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-helm-limits-and-caching
name: loki-helm-limits-and-caching
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki, loki-helm-chart, loki-helm-values, simple-scalable, loki-limits-config, ingestion-rate-limits, loki-caching, chunk-cache, results-cache, memcached]
level: advanced
status: docs-checked
description: "Deploy Loki with the grafana/loki Helm chart (simple scalable vs distributed), set limits_config for ingestion and queries, and enable chunk and results caches."
sources: ["https://grafana.com/docs/loki/latest/setup/install/helm/", "https://grafana.com/docs/loki/latest/configure/#limits_config", "https://grafana.com/docs/loki/latest/operations/caching/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki Helm, limits and caching

## Helm (grafana/loki)
```yaml
deploymentMode: SimpleScalable          # Monolithic (small; legacy name SingleBinary) | SimpleScalable (read/write/backend, being deprecated) | Distributed (microservices)
loki:
  auth_enabled: true                    # multi-tenant: clients must send X-Scope-OrgID
  schemaConfig: {configs: [{from: "<YYYY-MM-DD>", store: tsdb, object_store: s3, schema: v13, index: {prefix: index_, period: 24h}}]}
  storage:
    type: s3
    bucketNames: {chunks: loki-chunks, ruler: loki-ruler}
    s3: {region: eu-west-1}
  limits_config: {...}                  # below
write: {replicas: 3}
read: {replicas: 3}
backend: {replicas: 3}
chunksCache: {enabled: true, allocatedMemory: 8192}
resultsCache: {enabled: true}
serviceAccount: {annotations: {eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/loki}}
```
Simple scalable can scale close to a TB of logs per day and is being deprecated (removal planned with Loki 4.0); at larger scale, or for new installs, use Distributed for independent scaling of distributors, ingesters, queriers, query-frontend.

## limits_config
Example values, not defaults; check the Loki configuration reference for yours.
```yaml
limits_config:
  ingestion_rate_mb: 20                 # per tenant, per distributor-aggregated
  ingestion_burst_size_mb: 40
  per_stream_rate_limit: 5MB
  per_stream_rate_limit_burst: 15MB
  max_global_streams_per_user: 10000
  max_line_size: 256KB                  # truncate with max_line_size_truncate: true instead of reject
  reject_old_samples_max_age: 168h
  max_query_length: 721h
  max_query_parallelism: 32
  max_entries_limit_per_query: 5000
  split_queries_by_interval: 30m
  query_timeout: 2m
  volume_enabled: true
```
429 errors at clients = rate limits; `loki_discarded_samples_total{reason=...}` tells which
(`rate_limited`, `per_stream_rate_limit`, `stream_limit`, `line_too_long`, `greater_than_max_sample_age`).
Per-tenant overrides go in the runtime configuration file.

## Caching
- **Chunks cache** (memcached): avoids refetching chunks from object storage; biggest win for repeated queries.
- **Results cache**: query-frontend caches split query results (metric queries, also log queries if
  `cache_results`/`cache_index_stats_results`).
Watch cache hit rates in the Loki mixin dashboards.

## Verify
- [ ] `loki_discarded_samples_total` near zero after tuning; clients see no 429s.
- [ ] Dashboard reload of a 24 h query is much faster the second time (results cache hit).

## Checked
- 2026-10-28. Confirmed against the Loki Helm install pages (`deploymentMode` values, SingleBinary renamed Monolithic in community chart 12.0.0), the deployment modes page (SSD close to a TB per day, deprecated, removed in Loki 4.0), the request validation and rate limits page (`loki_discarded_samples_total` reasons `rate_limited`, `per_stream_rate_limit`, `stream_limit`, `line_too_long`, `greater_than_max_sample_age`), the caching page (`cache_results`, `cache_index_stats_results`) and the Helm values reference (`chunksCache.allocatedMemory`).
- Removed: the "few TB/day" figure, `tsdb_shipper.cache_location`, `loki_cache_hits / loki_cache_fetched_keys`, a fixed schema date and a real-looking AWS account id.
Method: documentation only; no commands were run.
