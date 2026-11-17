---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-tsdb-index-and-schema-v13-migration
name: loki-tsdb-index-and-schema-v13-migration
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tsdb-index, loki, schema-config, tsdb-shipper, boltdb-shipper, index-period, schema-v13]
level: practitioner
status: docs-checked
description: "Migrate Loki from boltdb-shipper to the TSDB index by adding a new schema_config period with schema v13 and a future start date."
sources: ["https://grafana.com/docs/loki/latest/operations/storage/tsdb/", "https://grafana.com/docs/loki/latest/configure/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use the TSDB index (recommended since Loki 2.8) instead of the deprecated boltdb-shipper.

Never edit an existing period; add a new entry whose `from` date is in the future, then roll the config out:
```yaml
schema_config:
  configs:
    - from: "2023-01-03"          # a date in the past (existing period)
      store: boltdb-shipper
      object_store: gcs
      schema: v12
      index:
        prefix: index_
        period: 24h
    - from: "2023-01-05"          # a date in the future when you deploy
      store: tsdb
      object_store: gcs
      schema: v13
      index:
        prefix: index_
        period: 24h
storage_config:
  tsdb_shipper:
    active_index_directory: /data/tsdb-index
    cache_location: /data/tsdb-cache
```
Use your own dates and your own `object_store`. Loki queries across schema boundaries transparently, reading old data with the old schema and writing new data with TSDB from the `from` date. Setting the new entry in the future lets the table manager prepare tables and keeps existing data from being read with the new schema.

In a microservices deployment with independent index gateways, `tsdb_shipper.index_gateway_client.server_address` points at the gateway (the docs use a `dns:///index-gateway.<namespace>.svc.cluster.local:9095` form).

Structured metadata needs `schema: v13` (chunk format V4) and the `tsdb` index; it is not supported with boltdb-shipper.

Gotchas
- Config entries should be treated as immutable for as long as you care about retention; changing an existing `from` entry risks reading old data with the wrong schema.
- Log deletion is supported on TSDB; BoltDB Shipper is deprecated and slated for removal in Loki 4.0.

## Verify
After the date passes, new data is written under the TSDB schema and queries spanning the boundary return data from both periods.

## Checked
2026-11-03. Confirmed against the Loki TSDB page, the storage page (schema upgrade procedure, immutability, recommended index) and the structured metadata and log deletion pages. Removed: specific example dates (2023-01-01, 2026-11-10), the "00:00 UTC aligned" rule, `compactor.working_directory` persistence claim, and the `loki_boltdb_shipper_*` / `loki_tsdb_*` metric claims.
Method: documentation only; no commands were run.
