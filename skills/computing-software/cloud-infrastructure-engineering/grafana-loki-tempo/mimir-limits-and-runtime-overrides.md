---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimir-limits-and-runtime-overrides
name: mimir-limits-and-runtime-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [mimir-limits, mimir, max-global-series-per-user, ingestion-rate, runtime-config, per-tenant-limits]
level: practitioner
status: docs-checked
description: "Set Mimir default limits for series, ingestion rate and queries, and override them per tenant through the runtime configuration file."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-runtime-configuration/", "https://grafana.com/docs/mimir/latest/configure/configuration-parameters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop one tenant from harming others and tailor large tenants.

Defaults live in the `limits` block; the documented defaults for these keys are `ingestion_rate` 10000, `ingestion_burst_size` 200000, `max_global_series_per_user` 150000 (series per tenant across the cluster before replication, 0 disables), `max_label_names_per_series` 30, `max_label_value_length` 2048, `max_fetched_chunks_per_query` 2000000. `compactor_blocks_retention_period` (default 0s) and `out_of_order_time_window` (default 0s) are off unless set.
```yaml
limits:
  ingestion_rate: 25000
  max_global_series_per_user: 300000
  out_of_order_time_window: 5m
runtime_config:
  file: /etc/mimir/runtime.yaml
```
```yaml
# runtime.yaml
overrides:
  tenant1:
    ingestion_rate: 50000
  tenant2:
    max_global_series_per_user: 1000000
```
Runtime config: `-runtime-config.file=<path>,<path>` (several files merge left to right; a `.gz` extension is decompressed), reloaded every 10 s by default (`-runtime-config.reload-period`). Runtime values take precedence over CLI flags. Any limit in the `limits` block can be overridden per tenant; tenants or keys not overridden inherit the defaults. On Kubernetes mount the file from a ConfigMap.

Per-process limits are separate: `ingester_limits` (for example `max_ingestion_rate`, `max_series`, `max_tenants`, `max_inflight_push_requests`) and `distributor_limits` (`max_ingestion_rate`, `max_inflight_push_requests`, `max_inflight_push_requests_bytes`) in the runtime file override `ingester.instance_limits` and `distributor.instance_limits`.

Errors are explained in the runbooks under IDs such as `err-mimir-max-series-per-user`, `err-mimir-tenant-max-ingestion-rate` and `err-mimir-sample-out-of-order`. Discarded samples are counted in `cortex_discarded_samples_total`.

Gotcha: raising limits hides cardinality problems; find the cause first.

## Verify
`GET /runtime_config` shows the effective runtime configuration; `GET /runtime_config?mode=diff` shows only non-default values.

## Checked
2026-11-03. Confirmed against the Mimir runtime configuration page, the configuration parameters reference (each default above) and the runbooks (error IDs, discarded-samples metric). Removed: the dead `configure-tenant-limits` source, the `cortex_ingester_active_series` metric, `mimirtool analyze` advice, the OOM remark on global limits, and the `compactor_blocks_retention_period: 90d` and `curl | head` examples (defaults are shown instead).
Method: documentation only; no commands were run.
