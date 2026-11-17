---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-architecture-storage-and-ruler
name: loki-architecture-storage-and-ruler
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, loki, loki-architecture, simple-scalable, microservices-mode, monolithic-mode, distributor, ingester, querier, query-frontend, query-scheduler, compactor, index-gateway, tsdb-index, object-storage, loki-storage, loki-retention, loki-compactor, retention-period, per-tenant-limits, loki-ruler, log-alerts, loki-alerting, helm-loki, multi-tenancy]
level: advanced
status: docs-checked
description: "Operate Grafana Loki: deployment modes, TSDB index on object storage, compactor retention, per-tenant limits, and the ruler for log-based alerts."
sources: ["https://grafana.com/docs/loki/latest/get-started/architecture/", "https://grafana.com/docs/loki/latest/get-started/deployment-modes/", "https://grafana.com/docs/loki/latest/operations/storage/retention/", "https://grafana.com/docs/loki/latest/alert/", "https://grafana.com/docs/loki/latest/configure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki architecture, storage, retention and ruler

**Goal:** a Loki that ingests your log volume cheaply (index only labels, chunks in object
storage), keeps data as long as policy says, and alerts from logs where metrics cannot.

## 1. Components and modes
Write path: **distributor** (validate, rate-limit, hash by stream) → **ingester** (build
chunks in memory + WAL, flush to object storage) ; **compactor** (compact index, apply
retention). Read path: **query-frontend** (split by time, cache, queue) → **query-scheduler**
→ **querier** (ingesters for recent + storage for old) ; **index-gateway** serves TSDB
index files; **ruler** evaluates alert/recording rules.

| Mode | Processes | Fits |
|---|---|---|
| Monolithic (`-target=all`) | one binary | dev, ≤ ~20 GB/day, can scale to a few replicas with shared storage |
| Simple scalable (`-target=write|read|backend`) | 3 deployments: write (distributor+ingester), read (query-frontend+querier), backend (compactor, ruler, index-gateway, scheduler) | can scale close to a TB of logs per day; being deprecated and removed with Loki 4.0 (the Helm chart default today) |
| Microservices | every component separate | very large / strict isolation |
Simple scalable needs a gateway (nginx in the chart) routing `/loki/api/v1/push` to write
and `/loki/api/v1/query*` to read.

## 2. Storage config (TSDB index, object store)
```yaml
schema_config:
  configs:
    - from: "<YYYY-MM-DD>"
      store: tsdb
      object_store: s3
      schema: v13
      index: { prefix: index_, period: 24h }
storage_config:
  tsdb_shipper: { active_index_directory: /loki/tsdb-index, cache_location: /loki/tsdb-cache }
  aws: { s3: s3://eu-west-1/loki-chunks, s3forcepathstyle: false }   # or gcs:, azure:, filesystem: (dev only)
compactor:
  working_directory: /loki/compactor
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150
  delete_request_store: s3
limits_config:
  retention_period: 744h                     # 31d global
  retention_stream:
    - selector: '{namespace="dev"}'
      priority: 1
      period: 168h
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  max_streams_per_user: 0                    # 0 = unlimited; set per tenant in overrides
  max_line_size: 256KB
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  max_query_series: 500
  max_query_parallelism: 32
  split_queries_by_interval: 30m
  volume_enabled: true
  allow_structured_metadata: true
overrides:                                   # per-tenant (runtime config file reloaded live)
  team-noisy: { ingestion_rate_mb: 30, retention_period: 168h }
```
- Schema changes are **append-only with a future `from` date**; never edit an old entry.
- Retention is enforced only by the **compactor** with `retention_enabled: true`; exactly
  one compactor runs. Object-store lifecycle rules are a backstop, not the mechanism.
- Chunks: `chunk_idle_period`, `max_chunk_age` (ingester) control flush; the WAL
  (`ingester.wal.enabled`) protects unflushed data — give ingesters a PVC.
- Multi-tenancy: `auth_enabled: true` and every request carries `X-Scope-OrgID`; a single
  tenant is `fake` when auth is off.

## 3. Helm quick path
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install loki grafana/loki -n logging -f values.yaml
# values.yaml: deploymentMode: SimpleScalable ; loki.storage.type: s3 + bucketNames ; loki.schemaConfig ; write.replicas: 3 ; read.replicas: 2 ; backend.replicas: 2 ; gateway.enabled: true ; loki.auth_enabled: false (single tenant)
```
Add `minio.enabled: true` only for a lab (the built-in MinIO subchart is deprecated). Size ingesters from your own stream counts and byte rates.

## 4. Ruler: alerts and recording rules from logs
```yaml
ruler:
  storage: { type: local, local: { directory: /etc/loki/rules } }   # or s3/gcs; rules under <dir>/<tenant>/*.yaml
  rule_path: /tmp/loki-rules
  alertmanager_url: http://alertmanager:9093
  enable_api: true
  ring: { kvstore: { store: memberlist } }
  remote_write: { enabled: true, client: { url: http://mimir/api/v1/push } }   # recording rules → metrics
```
```yaml
# /etc/loki/rules/fake/app.yaml
groups:
  - name: app
    interval: 1m
    rules:
      - alert: HighErrorLogRate
        expr: sum by (namespace, app) (rate({namespace="prod"} |= "level=error" [5m])) > 5
        for: 10m
        labels: { severity: ticket }
        annotations: { summary: "{{ $labels.app }} logs > 5 errors/s" }
      - record: namespace_app:log_errors:rate5m
        expr: sum by (namespace, app) (rate({namespace="prod"} | logfmt | level="error" [5m]))
```
Manage via `lokitool rules` / `cortextool rules load`, the ruler API, or Grafana's
data-source-managed rule editor. Keep rules cheap: metric queries over labels + line
filters, short windows; the ruler re-runs them every interval.

## 5. Operate
Metric: `loki_discarded_samples_total{reason}` (reasons such as `rate_limited`, `stream_limit`, `line_too_long`, `greater_than_max_sample_age`; see the request validation page).
Delete requests need `deletion_mode` set to `filter-and-delete` (a `limits_config` option, default `filter-and-delete`; the compactor-level setting is deprecated).

## Gotchas
- Out-of-order entries: `unordered_writes` (in `limits_config`) defaults to true; check client clocks if entries are still rejected.
- Retention shorter than `reject_old_samples_max_age` lets you ingest data that is deleted next cycle.
- Filesystem storage with several replicas silently splits data.
- Queriers OOM on `{job="x"}` over 30 days without a line filter: enforce `max_query_length`,
  `max_query_series`, and teach LogQL users to filter.

## Verify
- [ ] `curl -G gateway/loki/api/v1/query --data-urlencode 'query=sum(count_over_time({job=~".+"}[5m]))'` returns non-zero after shipping starts.
- [ ] Logs older than `retention_period` disappear within `retention_delete_delay` + compaction interval; bucket size plateaus.
- [ ] `loki_discarded_samples_total` ≈ 0 in steady state, or the reasons are known.
- [ ] A ruler alert appears in Alertmanager and a recording rule shows up in Mimir.

## Checked
- 2026-10-28. Confirmed against the Loki deployment modes page (20GB per day monolithic, SSD close to a TB per day, deprecation and Loki 4.0 removal, `write`/`read`/`backend` contents, gateway), the retention page (`retention_enabled`, `compaction_interval`, `retention_delete_delay`, `retention_delete_worker_count`, `delete_request_store`, `working_directory`), the alerting page (`rule_path`, `enable_api`, `remote_write`, `lokitool`/`cortextool`) and the `limits_config` reference (`unordered_writes` default true, `max_query_series` 500, `max_streams_per_user` 0, `max_line_size` 256KB, `volume_enabled`, `allow_structured_metadata`, `deletion_mode`).
- Fixed: the SSD scale claim ("several TB/day") and the compactor-level `deletion_mode` (now per-tenant limits).
- Removed: the memory sizing formula, metric families not on the fetched pages, endpoint list, the chart replicas guard remark and a fixed schema date.
Method: documentation only; no commands were run.
