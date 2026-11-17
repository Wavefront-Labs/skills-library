---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-mimir-operations
name: grafana-mimir-operations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, mimir, grafana-mimir, mimir-architecture, mimir-tenancy, multi-tenancy, x-scope-orgid, distributor, ingester, querier, query-frontend, query-scheduler, store-gateway, compactor, ruler, alertmanager-mimir, object-storage, per-tenant-limits, runtime-overrides, max-global-series-per-user, ha-deduplication, ha-tracker, zone-aware-replication, mimirtool, cortex, remote-write-receiver, long-term-storage]
level: advanced
status: docs-checked
description: "Operate Grafana Mimir: components, Helm, tenancy via X-Scope-OrgID, per-tenant limits and overrides, HA dedup of Prometheus pairs, rules via mimirtool, capacity signals."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/", "https://grafana.com/docs/mimir/latest/configure/about-tenant-ids/", "https://grafana.com/docs/mimir/latest/configure/configure-high-availability-deduplication/", "https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/", "https://grafana.com/docs/mimir/latest/set-up/helm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana Mimir operations

**Goal:** a multi-tenant metrics backend that takes remote_write from every Prometheus/
Alloy, dedupes HA pairs, enforces per-team limits, and serves global PromQL plus rules and
alerts, without any single Prometheus holding more than its hot window.

## 1. Architecture (same shape as Cortex/Loki/Tempo)
Write: **distributor** (validate, HA-dedupe, shard by series hash, replication factor 3) →
**ingester** (in-memory head + WAL, cuts 2h blocks, uploads to object storage).
Read: **query-frontend** (split, cache, queue) → **query-scheduler** → **querier**
(ingesters for the recent window, `query_ingesters_within`, default 13h; **store-gateway** for bucket blocks). **compactor** merges
blocks per tenant (split-and-merge for huge tenants), applies retention, dedupes HA
replicas vertically. **ruler** evaluates recording/alerting rules per tenant; **alertmanager**
(multi-tenant) routes them. Optional **overrides-exporter** exposes limits as metrics.
Deployment: `mimir-distributed` Helm chart (monolithic `-target=all` for small, read-write
mode, or microservices). Each series is held by RF ingesters (default replication factor 3), so
in-memory series are roughly active series × RF; size ingesters from your own measurements.

## 2. Tenancy
Every request needs `X-Scope-OrgID: <tenant>` (unless `multitenancy_enabled: false` →
tenant `anonymous`). Prometheus/Alloy set it as a remote_write header; Grafana data source
sets `httpHeaderName1: X-Scope-OrgID`. Tenant federation for queries:
`tenant_federation.enabled: true` and `X-Scope-OrgID: team-a|team-b`.
Tenant ids: ≤ 150 bytes or characters; only alphanumerics and `!` `-` `_` `.` `*` `'` `(` `)`; `.`, `..` and `__mimir_cluster` are not valid.

## 3. Limits and overrides (the core operational control)
```yaml
limits:                                   # example values, NOT the shipped defaults (see the configuration reference)
  max_global_series_per_user: 1500000
  max_global_series_per_metric: 0
  ingestion_rate: 100000                  # samples/s
  ingestion_burst_size: 200000
  max_label_names_per_series: 30
  max_label_value_length: 2048
  max_fetched_series_per_query: 100000
  max_fetched_chunks_per_query: 2000000
  max_query_parallelism: 32
  max_partial_query_length: 0
  max_total_query_length: 0
  compactor_blocks_retention_period: 90d
  out_of_order_time_window: 10m
  native_histograms_ingestion_enabled: true
  ruler_max_rules_per_rule_group: 50
  ruler_max_rule_groups_per_tenant: 200
runtime_config: { file: /etc/mimir/runtime.yaml, period: 10s }
```
```yaml
# runtime.yaml (hot-reloaded)
overrides:
  team-payments: { max_global_series_per_user: 5000000, ingestion_rate: 400000, compactor_blocks_retention_period: 400d }
  team-dev:      { max_global_series_per_user: 200000,  compactor_blocks_retention_period: 15d }
```
Discards are visible per tenant and reason:
`sum by (user, reason) (rate(cortex_discarded_samples_total[5m]))`
(the `reason` values map to the `err-mimir-*` entries in the Mimir runbooks).
Alert the tenant owner on it; raise limits deliberately with capacity in hand.

## 4. HA deduplication of Prometheus pairs
```yaml
limits: { accept_ha_samples: true, ha_cluster_label: cluster, ha_replica_label: prometheus_replica }
distributor: { ha_tracker: { enable_ha_tracker: true, kvstore: { store: memberlist }, ha_tracker_failover_timeout: 30s } }
```
Both replicas send; the distributor elects one `prometheus_replica` per `cluster` and drops
the other. The elected replica's
HA label is stripped on ingest. Requires the two Prometheus to have **identical** external labels except the replica.

## 5. Rules and alerting with mimirtool
```bash
export MIMIR_ADDRESS=https://mimir.internal MIMIR_TENANT_ID=team-payments MIMIR_API_KEY=...
mimirtool rules lint rules.yaml
mimirtool rules check rules.yaml                 # best-practice lint (naming, aggregation)
mimirtool rules sync rules.yaml --namespaces=payments        # diff + apply
mimirtool rules list ; mimirtool rules print
mimirtool alertmanager load alertmanager.yaml template1.tmpl   # per-tenant AM config
mimirtool alertmanager verify
mimirtool analyze grafana --address=https://grafana --key=<SERVICE_ACCOUNT_TOKEN>   # which metrics dashboards use
mimirtool analyze prometheus --address=$MIMIR_ADDRESS --id=$MIMIR_TENANT_ID --grafana-metrics-file=metrics-in-grafana.json   # used vs unused series
mimirtool backfill --address=$MIMIR_ADDRESS --id=$MIMIR_TENANT_ID ./blocks/*   # import TSDB blocks
mimirtool remote-read export --address=<SOURCE_URL> --remote-read-path=/api/v1/read --selector='up' --tsdb-path=./local-tsdb
```
Rule files are Prometheus format; the ruler evaluates each group against the tenant's data
(`ruler.query_frontend.address` for frontend-routed evaluation on big rules).

## 6. Capacity signals
```promql
sum by (user) (cortex_ingester_active_series)
cortex_ingester_memory_series
cortex_bucket_store_blocks_loaded
cortex_query_scheduler_queue_length
```
Use the Mimir mixin dashboards and
its alerts (`MimirIngesterUnhealthy`, `MimirCompactorNotRunningCompaction`…; the runbooks page lists each alert).

## Gotchas
- Scaling ingesters **down** requires the "shutdown and flush" procedure (`/ingester/prepare-shutdown`
  then scale; or rollout-operator) or you lose un-uploaded data; zone-aware replication
  makes rolling restarts safer.
- `max_global_series_per_user` counts series across all ingesters ÷ RF; a tenant sending
  high-churn pod labels hits it while "active series" dashboards look low.
- Queries that hit `max_fetched_chunks_per_query` fail with an error; fix the query or raise the limit per tenant.
- Store-gateway needs enough disk for index-headers and memcached for chunks/index caching; without caches, long-range queries hammer the bucket.
- Changing `ha_cluster_label` semantics or Prometheus external labels mid-stream creates
  duplicate series with and without the old labels.

## Verify
- [ ] `curl -H 'X-Scope-OrgID: team-payments' mimir/prometheus/api/v1/query?query=up` returns the tenant's targets, and without the header is rejected.
- [ ] Killing one Prometheus replica shows zero gaps in a Mimir-backed panel and ingestion from the surviving replica continues.
- [ ] `cortex_discarded_samples_total` is 0 for production tenants or each reason has an owner.
- [ ] `mimirtool rules sync` from CI is the only way rules change; `rules list` matches git.

## Checked
- 2026-10-28. Confirmed against the Mimir configuration reference (limits names and defaults, `ha_tracker.enable_ha_tracker`, `accept_ha_samples`, `ha_cluster_label`/`ha_replica_label`, `query_ingesters_within` 13h, `max_partial_query_length`), About tenant IDs (150 limit, allowed characters, invalid ids), the HTTP API page (`/ingester/prepare-shutdown`), the mimirtool page (`--address`, `--id`, `--key`, `remote-read export --tsdb-path`, `rules sync --namespaces`) and the runbooks page (`MimirIngesterUnhealthy`, `MimirCompactorNotRunningCompaction`, `err-mimir-*`).
- Fixed: the wrong tenant-id character class, mimirtool flags that do not exist (`--prometheus-address`, `--remote-read-address`, `--from`, `--to`), the invented alert `MimirCompactorHasNotSuccessfullyRunCompaction`, `max_query_length`, the 12h ingester window, and sample limits presented as defaults.
- Removed: sizing figures, discard reason names, and metric names and dashboard titles not on the fetched pages.
Method: documentation only; no commands were run.
