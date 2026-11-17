---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-series-churn-diagnosis
name: prometheus-series-churn-diagnosis
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, series-churn, churn-diagnosis, cardinality, tsdb-analyze, kubernetes, pod-churn]
level: advanced
status: verified
description: "Find and fix series churn in Prometheus: churn metrics, promtool tsdb analyze, the labels that rotate (pod, container id, version), and relabel fixes."
sources: ["https://prometheus.io/docs/prometheus/latest/command-line/promtool/", "https://www.robustperception.io/finding-churning-targets-in-prometheus-with-scrape_series_added/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing series churn

Churn = series created and abandoned quickly. Each new series costs index/memory in the head for up to
~3 h and stays in blocks until retention removes them; churn hurts even when "active series" looks stable.

## 1. Measure
```promql
rate(prometheus_tsdb_head_series_created_total[5m])       # new series/s
rate(prometheus_tsdb_head_series_removed_total[5m])       # GC'd at head compaction
# Which targets churn most (needs scrape_series_added, always exposed per target)
topk(10, sum by (job) (sum_over_time(scrape_series_added[1h])))
topk(10, sum_over_time(scrape_series_added[1h]))           # per instance
```
A steady-state service should add near-zero series per scrape after warm-up.

## 2. Find the rotating label
```bash
promtool tsdb analyze /prometheus/data                    # newest block
promtool tsdb analyze /prometheus/data <ULID> --limit=20
```
Read "Label pairs most involved in churning", "Label names most involved in churning", "Highest cardinality labels",
"Highest cardinality metric names" and "Most common label pairs" (the 3.15.1 headings). Then confirm:
```promql
count by (__name__) ({job="api"})                         # metric with most series
count(count by (pod) (up{job="api"}))                     # how many distinct pods in the window
```

## 3. Usual culprits and fixes
| Culprit | Fix |
|---|---|
| `pod`, `instance` rotate on every deploy/HPA scale | Normal; reduce by fewer, longer-lived pods or aggregate in recording rules and shorten raw retention |
| Per-container or per-image ID labels from container exporters | `metric_relabel_configs` `labeldrop` them (read your exporter's label list first) |
| Version/commit labels on every metric | Put them on one `build_info` metric, join with `group_left` |
| Request IDs, user IDs, URLs with IDs in labels | Fix instrumentation (route template, not raw path) |
| Short-lived CronJob/Job pods | Pushgateway or aggregate; drop per-pod labels |

## Verify
- [ ] `rate(prometheus_tsdb_head_series_created_total[1h])` drops after the fix.
- [ ] `promtool tsdb analyze` on a new block no longer lists the label in the top 5.
- [ ] Head memory falls back within one head-compaction cycle (~2-3 h).
