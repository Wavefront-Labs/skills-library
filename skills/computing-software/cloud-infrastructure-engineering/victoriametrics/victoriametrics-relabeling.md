---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-relabeling
name: victoriametrics-relabeling
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [relabeling, metric-relabel-configs, replace-all, graphite-relabel, if-selector, debug-relabeling]
level: advanced
status: docs-checked
description: "Use VictoriaMetrics relabeling actions, the if selector and the debug UIs at service discovery, scrape and remote write stages."
sources: ["https://docs.victoriametrics.com/victoriametrics/relabeling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics relabeling

Relabeling runs at three stages: service discovery (`relabel_configs`, drops or edits targets), scraping (`metric_relabel_configs`, per scraped metric) and remote write (`-remoteWrite.relabelConfig`, `-remoteWrite.urlRelabelConfig`).

Prometheus-compatible actions: `drop`, `keep`, `labeldrop`, `labelkeep`, `labelmap`. VictoriaMetrics additions: `replace_all`, `labelmap_all`, `keep_if_equal`, `drop_if_equal`, `keep_if_contains`, `drop_if_contains`, `keep_metrics`, `drop_metrics`, and `graphite`.

Options: `if` takes a series selector or list (matches if any does), for example `if: '{job=~"web-.*", environment!="staging"}'`. `replacement` supports `{{label_name}}` templating. A list `regex` is joined with `|`. `separator` defaults to `;`.

```yaml
metric_relabel_configs:
  - action: labeldrop
    if: 'node_cpu_seconds_total{mode="idle"}'
    regex: "cpu|mode"
- action: graphite
  match: "*.*.*.total"
  labels:
    __name__: "${3}_total"
    job: "$1"
```

Rules: `regex` must match the whole label name or value, not a substring. Labels starting with `__` are removed after relabeling, so use them for temporary labels. Do not remove `instance` and `job`; dropping too many labels can create duplicate series.

Debugging: `/targets` and `/service-discovery` offer step-by-step relabeling views, vmagent serves `/metric-relabel-debug`, and `/remotewrite-relabel-config` and `/remotewrite-url-relabel-config` (v1.129.0+) show the active remote write configs.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
