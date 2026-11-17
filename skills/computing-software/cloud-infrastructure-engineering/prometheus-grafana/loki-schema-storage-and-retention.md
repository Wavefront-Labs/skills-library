---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-schema-storage-and-retention
name: loki-schema-storage-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki, schema-config, period-config, tsdb-shipper, loki-object-storage-config, s3-config-loki, compactor-retention-config, per-stream-retention, retention-stream, loki-retention, loki-compactor]
level: advanced
status: gated
description: "Configure Loki schema periods (tsdb, v13), object storage for S3/GCS/Azure, and compactor-based retention including per-tenant and per-stream rules, plus safe schema upgrades."
sources: ["https://grafana.com/docs/loki/latest/configure/storage/", "https://grafana.com/docs/loki/latest/operations/storage/schema/", "https://grafana.com/docs/loki/latest/operations/storage/retention/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki schema, storage and retention

## schema_config
```yaml
schema_config:
  configs:
    - from: 2024-04-01          # existing period, never edit
      store: tsdb
      object_store: s3
      schema: v13
      index: {prefix: index_, period: 24h}
    - from: 2026-11-01          # new period: always a FUTURE date (UTC), added before that day
      store: tsdb
      object_store: s3
      schema: v13
      index: {prefix: loki_index_, period: 24h}
```
- Changing store/schema = add a new period starting tomorrow or later; old data stays readable with the old period.
- `tsdb` + `v13` is required for structured metadata and OTLP ingestion; `boltdb-shipper` is deprecated and being removed in Loki 4.0 (tested: schema v12 fails start-up with a `CONFIG ERROR` naming v13).
- Index period must be 24h for tsdb (tested: 168h fails with `tsdb must always have periodic config for index set to 24h`). A new install needs its first `from` in the past; only an added period needs a future `from`, and Loki treats it as 00:00 UTC.

## Storage
```yaml
common:
  storage:
    s3:
      bucketnames: loki-chunks
      region: eu-west-1
      # credentials via IRSA; or access_key_id/secret_access_key
storage_config:
  tsdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/index_cache
```
GCS: `gcs: {bucket_name: ...}`; Azure: `azure: {account_name, container_name, use_federated_token: true}`.
Use separate buckets for chunks and ruler; lifecycle rules must NOT delete objects that Loki's retention still
expects (let the compactor delete) (gated: unconfirmed, source is paywalled or blocked): no object store was available.

## Retention (compactor)
```yaml
compactor:
  working_directory: /loki/compactor
  retention_enabled: true
  retention_delete_delay: 2h
  delete_request_store: s3          # required with retention in recent versions
limits_config:
  retention_period: 30d             # global default (0 = keep forever)
  retention_stream:
    - selector: '{namespace="dev"}'
      priority: 1
      period: 7d
    - selector: '{app="audit"}'
      priority: 2
      period: 400d
# per-tenant overrides in runtime config: overrides.<tenant>.retention_period
```
Run exactly one compactor instance. The highest `priority` number among matching `retention_stream` rules wins (equal priority: the shorter period); per-tenant rules override the global list. Each `retention_stream` `period` must be at least 24h (tested: 12h fails with `retention period must be >= 24h`), and retention needs the 24h index period.

## Deletes
Log deletion API (`/loki/api/v1/delete?query={...}&start=&end=`) is registered only when the compactor has `retention_enabled: true`, and the tenant's `deletion_mode` (`disabled`, `filter-only`, `filter-and-delete`; default `filter-and-delete`) must allow it; `allow_deletes` is deprecated. Used for PII removal.

## Verify
- [ ] `/config` shows the intended periods; queries across the period boundary return data.
- [ ] Bucket size stabilises after retention_period + delete delay; `loki_compactor_*` metrics show runs.

## Checked
Ran Loki 3.7.9 `-verify-config` on the page's schema, compactor and `retention_stream` blocks (valid with filesystem, S3, GCS and Azure `common.storage` forms and `delete_request_store` set to the matching backend), and on variants that fail: no `delete_request_store` with retention on, period 168h, schema v12 (structured metadata), `from` dates out of order, 12h stream retention, and `common.storage` with more than one backend (rejected). `compactor.shared_store` is rejected. Read the v3.7.9 docs source: operations/storage/schema (future `from`, 00:00 UTC, boltdb-shipper removal in 4.0), operations/storage/retention (singleton compactor, priority rule, 24h minimum, `retention_delete_delay` 2h, `delete_request_store` required), operations/storage/logs-deletion (`deletion_mode`, endpoints only with retention enabled). The object-store lifecycle-rule advice is gated as marked (no cloud account).
