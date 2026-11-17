---
id: computing-software.database-administration.time-series-databases.prometheus-sample-limits
name: prometheus-sample-limits
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-cardinality, prometheus-sample-limits, prometheus]
level: practitioner
status: docs-checked
description: "Protect Prometheus from runaway targets with per-scrape sample, label and target limits, and measure headroom against them."
sources:
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/prometheus/latest/feature_flags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scrape limits

**Goal:** Protect Prometheus from runaway targets with scrape limits.

## Steps
- Per scrape config (and also available in `global`): `sample_limit`, `label_limit`, `label_name_length_limit`, `label_value_length_limit`, `target_limit`, and `body_size_limit` (experimental). All default to 0, meaning no limit.
  ```
  scrape_configs:
    - job_name: app
      sample_limit: <N>
      label_limit: <N>
  ```
- `sample_limit` counts samples after metric relabeling; if exceeded, the entire scrape is treated as failed. The same applies to `label_limit` (labels per sample) and the label name/value length limits (in bytes).
- `target_limit` marks targets as failed without scraping them when more unique targets than the limit exist after target relabeling (experimental).
- To measure headroom, enable extra scrape metrics (`extra_scrape_metrics` in config; the older `--enable-feature=extra-scrape-metrics` flag is deprecated) and query `scrape_samples_post_metric_relabeling / (scrape_sample_limit > 0)`.
- Choose a limit with margin above the normal sample count so growth shows up in that ratio before scrapes start failing.
- Pair with a size-based retention limit (see prometheus-retention-time-size).

**Gotcha:** Exceeding a limit fails the whole scrape rather than keeping part of the data, so a limit set too tight causes gaps.

## Verify
- A test target over its limit shows a failed scrape on the Targets page.
- Normal targets are unaffected.

## Checked
2026-11-03. Confirmed against the configuration reference (limit fields, defaults of 0, whole-scrape failure, global availability) and the feature flags page (extra scrape metrics, `scrape_sample_limit`, the division query). Resolved the "confirm" on global defaults. Removed: the 50000 and 30 example values, `scrape_samples_scraped`, `prometheus_target_scrapes_exceeded_sample_limit_total`, the "about 2 times" sizing ratio and the explicit `up=0` assertion (not on a page read).
Method: documentation only; no commands were run.
