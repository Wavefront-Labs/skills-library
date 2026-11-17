---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-metrics-storage-retention
name: grafana-mimir-metrics-storage-retention
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [retention, compactor, object-storage, blocks-retention, deletion]
level: practitioner
status: docs-checked
description: "Shows how to configure Mimir object storage retention with compactor_blocks_retention_period, globally and per tenant, and notes the lack of per-series deletion."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-metrics-storage-retention/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Metrics storage retention

Mimir keeps metrics in object storage and by default never deletes them, so usage grows over time. The compactor enforces retention.

## Global

Set `-compactor.blocks-retention-period` or:

```yaml
limits:
  compactor_blocks_retention_period: 1y
```

## Per tenant

Use runtime configuration overrides:

```yaml
overrides:
  tenant1:
    compactor_blocks_retention_period: 1y
  tenant2:
    compactor_blocks_retention_period: 2y
  tenant3:
    compactor_blocks_retention_period: 0
```

A value of `0` disables retention for that tenant, so its data is never deleted.

## Limits

Per-series deletion and retention are not supported, nor is the Prometheus Delete series API. Retention deletes all metrics data older than the configured period.

## Checked

Confirmed the never-delete default, the compactor role, the global flag and YAML setting, the per-tenant overrides including 0 to disable and the lack of per-series deletion. Removed the note on the ingester TSDB retention period and shuffle-sharding because the page does not state it, and reworded the whole-blocks remark to the page's wording.

Method: docs-checked 2026-11-09 against the raw grafana/mimir docs page configure-metrics-storage-retention.md, read in full.
