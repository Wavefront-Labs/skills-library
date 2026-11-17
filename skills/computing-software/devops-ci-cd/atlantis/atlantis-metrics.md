---
id: computing-software.devops-ci-cd.atlantis.atlantis-metrics
name: atlantis-metrics
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [metrics, prometheus, statsd, observability, monitoring]
level: intro
status: docs-checked
description: "Expose Atlantis operation metrics through Prometheus or Statsd and know which counters matter."
sources: ["https://www.runatlantis.io/docs/stats"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis metrics

Atlantis exposes metrics for each operation: errors, successes and latencies. Duration metrics (`*_time`) are in seconds; counters are unitless. Backends are Statsd and Prometheus, configured under `metrics` in the server-side config.

```yaml
metrics:
  prometheus:
    endpoint: "/metrics"
```

For Statsd set `statsd.host` and `statsd.port` (both required); for Prometheus set `prometheus.endpoint`.

View everything with `curl localhost:4141/metrics`. Output is trimmed in the docs and the set can change between releases as metrics are added or deprecated.

Key counters:
- `atlantis_cmd_autoplan_execution_error` and `atlantis_cmd_autoplan_execution_success`: autoplan results.
- `atlantis_cmd_comment_plan_execution_error`: failures of manual `atlantis plan` comments.
- `atlantis_cmd_comment_apply_execution_error` and `atlantis_cmd_comment_apply_execution_success`: apply results.
- Builder metrics such as `atlantis_cmd_autoplan_builder_execution_success` and `_time` summaries (with `_sum` and `_count`).

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Metrics/Stats, Server Side Repo Config (Metrics). Removed or fixed: generic closing alerting tips.

Method: documentation only; no commands were run.
