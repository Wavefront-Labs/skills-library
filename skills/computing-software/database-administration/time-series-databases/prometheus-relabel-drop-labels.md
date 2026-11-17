---
id: computing-software.database-administration.time-series-databases.prometheus-relabel-drop-labels
name: prometheus-relabel-drop-labels
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-cardinality, prometheus-relabel-drop-labels, prometheus]
level: practitioner
status: docs-checked
description: "Reduce cardinality with metric_relabel_configs: drop, keep, labeldrop and labelkeep, plus write_relabel_configs for remote write."
sources:
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/prometheus/latest/command-line/promtool/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relabeling to drop labels and series

**Goal:** Reduce cardinality with relabeling and metric_relabel_configs.

## Steps
```
metric_relabel_configs:
  - source_labels: [__name__]
    regex: "http_request_duration_seconds_bucket"
    action: drop
  - regex: "some_label|another_label"
    action: labeldrop
```
- `relabel_configs` rewrite targets before the scrape; `metric_relabel_configs` apply to samples as the last step before ingestion, and do not apply to automatically generated series such as `up`.
- `drop` removes entries whose concatenated `source_labels` match `regex`; `keep` removes those that do not match, so `keep` on an allow-list of metric names suits noisy exporters.
- `labeldrop` removes every label whose name matches `regex`; `labelkeep` removes every label that does not match. Ensure the series are still uniquely labeled afterwards.
- `regex` is RE2 and fully anchored (use `.*x.*` to un-anchor).
- `write_relabel_configs` is applied to samples before they are sent to a remote write endpoint, after external labels.
- Check config syntax with `promtool check config prometheus.yml`; `promtool check service-discovery <config> <job>` shows target relabeling results.

**Gotcha:** Dropping a distinguishing label can leave two series with identical labels, causing duplicate-sample problems and lost data.

## Verify
- Series count falls as predicted (`/api/v1/status/tsdb`).
- The Targets page shows no new scrape errors.

## Checked
2026-11-03. Confirmed against the Prometheus configuration reference (metric_relabel_configs, relabel actions, regex anchoring, write_relabel_configs) and the promtool page (`check config`, `check service-discovery`). Removed: the `pod_template_hash`/`controller_revision_hash` example (replaced by placeholders), the `prometheus_target_scrapes_sample_duplicate_timestamp_total` metric and the exact error string (not on a page read).
Method: documentation only; no commands were run.
