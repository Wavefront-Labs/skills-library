---
id: computing-software.database-administration.time-series-databases.prometheus-cardinality-analysis
name: prometheus-cardinality-analysis
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-cardinality, prometheus-cardinality-analysis, prometheus]
level: practitioner
status: docs-checked
description: "Identify which metrics and labels create too many time series, using the TSDB status API and promtool tsdb analyze."
sources:
  - https://prometheus.io/docs/prometheus/latest/querying/api/
  - https://prometheus.io/docs/prometheus/latest/command-line/promtool/
  - https://prometheus.io/docs/practices/naming/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding high-cardinality series

**Goal:** Identify which metrics and labels create too many time series.

## Steps
- Cheapest first: `GET /api/v1/status/tsdb` (for example `curl http://localhost:9090/api/v1/status/tsdb`). It returns `headStats` (`numSeries`, `chunkCount`), `seriesCountByMetricName`, `labelValueCountByLabelName`, `memoryInBytesByLabelName` and `seriesCountByLabelValuePair`. The `limit` parameter defaults to 10 items per list (maximum 10000).
- Offline: `promtool tsdb analyze data/` analyzes churn, label pair cardinality and compaction efficiency; `--limit` sets items per list (default 20), `--match` restricts to one selector, and a block id argument picks a block (default is the last block).
- Heavy but flexible PromQL: `topk(10, count by (__name__)({__name__=~".+"}))` (scans every series; run sparingly).
- Per-label: `count(count by (path) (http_requests_total))` gives the distinct values of `path`.
- Typical culprits: user ids, email addresses, request ids, URL paths with ids, pod names with random suffixes, unbounded error strings. The naming guide says not to use labels for high-cardinality dimensions such as user IDs or email addresses, because every unique label combination is a new series.
- Fix at source, then drop with relabeling (see prometheus-relabel-drop-labels).

**Gotcha:** counting series alone can miss churn; `promtool tsdb analyze` reports churn explicitly.

## Verify
- `numSeries` in `headStats` flattens after the fix.
- The status API shows no label with an unexpected value count.

## Checked
2026-11-03. Confirmed against the Prometheus HTTP API page (TSDB Stats fields and limit), the promtool command-line page (`tsdb analyze` description, flags, arguments) and the metric naming page (high-cardinality labels). Removed: the `prometheus_tsdb_head_series_created_total` churn metric and the `prometheus_tsdb_head_series` verify metric (metric names not on a page read), and the "memory and index work for 2 hours" claim.
Method: documentation only; no commands were run.
