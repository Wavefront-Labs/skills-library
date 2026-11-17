---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.monitoring-mimir
name: monitoring-mimir
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [mimir-dashboards, mimir-mixin, mimir-metrics, mimir, self-monitoring]
level: practitioner
status: docs-checked
description: "Monitor Grafana Mimir: deploy mimir-mixin dashboards, alerts and recording rules, meta-monitoring scrape setup, and the core write/read/limit metrics to watch."
sources: ["https://grafana.com/docs/mimir/latest/manage/monitor-grafana-mimir/", "https://grafana.com/docs/mimir/latest/manage/monitor-grafana-mimir/installing-dashboards-and-alerts/", "https://github.com/grafana/mimir/tree/main/operations/mimir-mixin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring Mimir

## Mixin
Precompiled assets: `operations/mimir-mixin-compiled/` (`dashboards/`, `alerts.yaml`, `rules.yaml`); compiled with a default configuration, so custom label names need a build from source (`make build-mixin`, config in `operations/mimir-mixin/config.libsonnet`) or the Jsonnet mixin. Some dashboards need the recording rules. The mixin alerts exclude client-side 529 and 598 codes.
```bash
mimirtool rules load --address=$MIMIR --id=meta rules.yaml alerts.yaml   # into a meta-monitoring tenant
```
Or vendor the mixin with jsonnet-bundler (`jb install github.com/grafana/mimir/operations/mimir-mixin@main`) and override `_config`.

## Meta-monitoring
Send Mimir's own metrics/logs to a **separate** cluster or Grafana Cloud so an outage does not hide itself.
The dashboards and alerts require specific labels set when Prometheus or Alloy scrapes Mimir; check the label requirements on the Mimir monitoring page before wiring up scraping.

## Core metrics
| What | Metric |
|---|---|
| Discards | `cortex_discarded_samples_total{reason}` (reasons map to the `err-mimir-*` runbook entries) |
| Active series | `cortex_ingester_memory_series`, `cortex_ingester_active_series` per user |
| Store-gateway | `cortex_bucket_store_blocks_loaded` |

## Alerts worth paging on
MimirIngesterUnhealthy, MimirRequestErrors, MimirRequestLatency, MimirIngesterReachingSeriesLimit,
MimirCompactorNotRunningCompaction, MimirStoreGatewayTooManyFailedOperations. Each has an entry in the Mimir runbooks.

## Verify
Open the mixin Writes dashboard: every component row shows data; if empty, the scrape labels do not match what the mixin requires.

## Checked
- 2026-10-28. Confirmed against the Mimir "Installing dashboards and alerts" page (`operations/mimir-mixin-compiled/`, `make build-mixin`, `config.libsonnet`, `jb install`, 529 and 598 exclusion, required labels and recording rules), the runbooks page (alert names above; `err-mimir-*`) and the configuration reference (`cortex_ingester_*` metrics referenced there).
- Fixed: `MimirCompactorHasNotSuccessfullyRunCompaction` does not exist (the runbook alert is `MimirCompactorNotRunningCompaction`).
- Removed: the `-baremetal` variant, dashboard title list, Helm `metaMonitoring` value, exact label forms, and metric names not on the fetched pages.
Method: documentation only; no commands were run.
