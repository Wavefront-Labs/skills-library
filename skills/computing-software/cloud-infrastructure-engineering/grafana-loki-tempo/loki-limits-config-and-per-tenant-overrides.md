---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-limits-config-and-per-tenant-overrides
name: loki-limits-config-and-per-tenant-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-limits, loki, limits_config, runtime-overrides, ingestion-rate, max-streams, per-tenant-limits]
level: practitioner
status: docs-checked
description: "Tune Loki limits_config and per-tenant runtime overrides for ingestion rate, streams, query range and line size."
sources: ["https://grafana.com/docs/loki/latest/configure/#limits_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: protect the cluster from noisy tenants while giving large tenants room.

Documented defaults in `limits_config` (latest docs; check your release):
- `ingestion_rate_mb: 4` and `ingestion_burst_size_mb: 6` (the rate counts log line size plus structured metadata size).
- `ingestion_rate_strategy: global`.
- `max_line_size: 256KB`, `max_label_names_per_series: 15`.
- `max_streams_per_user: 0` (disabled) and `max_global_streams_per_user: 5000`.
- `max_query_series: 500`, `max_query_parallelism: 32`, `max_query_length: 30d1h`, `max_query_lookback: 0s`.
- `retention_period: 0s`, `reject_old_samples: true`, `reject_old_samples_max_age: 1w`.

Per-tenant overrides live in a runtime file that Loki reloads without a restart:
```yaml
runtime_config:
  file: /etc/loki/runtime.yaml
  period: 10s
```
```yaml
# runtime.yaml
overrides:
  tenant-a:
    ingestion_rate_mb: 40
    max_global_streams_per_user: 50000
```
`runtime_config.period` defaults to 10s. Values in `limits_config` are the defaults that the `overrides` section replaces per tenant.

Gotchas
- `ingestion_rate_strategy: global` divides the limit across distributor replicas (it needs the distributors to form their own ring). `local` applies the limit per distributor, so the effective rate is N times higher with N replicas.
- `ingestion_burst_size_mb` is enforced by the per-distributor limiter even with `global`; set it at least to the largest push request you expect.
- `max_global_streams_per_user` becomes a dynamic per-ingester limit based on the replication factor and healthy ingester count.
- Raise a limit carefully, or reduce label cardinality instead.

## Verify
```
curl -s http://loki:3100/config
```
The `/config` endpoint returns the running configuration.

## Checked
2026-11-03. Confirmed against the Loki configuration reference (limits_config, runtime_config, ruler blocks) and the HTTP API reference (`GET /config`). Corrected: defaults in the old example (ingestion rate 8/16 MB, 10000 streams, 30d lookback, 744h retention) were wrong, and `ingestion_rate_strategy` default is `global`, not `local`. Removed: the `/runtime_config` endpoint, unverified error message strings, and the `grep` verify line.
Method: documentation only; no commands were run.
