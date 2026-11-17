---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-migrate-from-prometheus
name: grafana-alloy-migrate-from-prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [migrate-prometheus, configformat-prometheus, bypass-errors, convert-report, rule-files, remote-read]
level: practitioner
status: docs-checked
description: "Migrate a Prometheus configuration to Alloy with alloy convert or run it directly with --config.format=prometheus, and know the unsupported sections."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/migrate/from-prometheus.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating from Prometheus to Alloy

Convert:
```shell
alloy convert --source-format=prometheus --output=/path/to/config.alloy /path/to/prometheus.yml
```
Add `--report=/path/to/report.txt` for a diagnostic report (for example "Converted scrape_configs job_name "prometheus" into a prometheus.scrape.prometheus component"). Problems go to stderr; `--bypass-errors` produces a best-effort result that may not behave like the original, so test it fully.

A scrape config with `static_configs` and `remote_write` becomes `prometheus.scrape "prometheus"` (targets, `forward_to`, `job_name`, `scrape_timeout`) and `prometheus.remote_write "default"` with the endpoint name, `basic_auth` and explicit `queue_config` (capacity 2500, max_shards 200, max_samples_per_send 500) and `metadata_config`.

## Try without converting
`alloy run --config.format=prometheus /path/to/prometheus.yml` converts in memory and loads directly. `--config.bypass-conversion-errors` also exists; do not use it in production.

## Limitations
- Not convertible: `rule_files`, `alerting`, `remote_read`, `storage`, `tracing`; other unsupported features are errors.
- Prometheus command-line flags (for example `--web.listen-address`) are not in the config file; check them.
- Meta-monitoring metrics have different names, so update alerts and dashboards.
- Logs differ, and Alloy exposes its own UI.

## Checked
2026-11-04: confirmed against the Migrate from Prometheus page. Removed: nothing.
Method: documentation only; no commands were run.
