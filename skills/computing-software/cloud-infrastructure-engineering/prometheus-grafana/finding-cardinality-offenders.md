---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.finding-cardinality-offenders
name: finding-cardinality-offenders
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, cardinality, cardinality-analysis, top-series, tsdb-status-api, high-cardinality, mimir-cardinality-api]
level: practitioner
status: docs-checked
description: "Find which metrics, labels and targets drive Prometheus series count: TSDB status API, topk count queries, per-target scrape stats, and the Mimir cardinality endpoints."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-stats", "https://grafana.com/docs/mimir/latest/references/http-api/#label-names-cardinality", "https://www.robustperception.io/which-are-my-biggest-metrics/", "https://prometheus.io/docs/concepts/jobs_instances/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding cardinality offenders

## 1. Server-wide view (TSDB stats endpoint)
```bash
curl -s 'http://localhost:9090/api/v1/status/tsdb?limit=20' | jq '.data | {
  head: .headStats.numSeries,
  byMetric: .seriesCountByMetricName,
  byLabelValues: .labelValueCountByLabelName,
  byPair: .seriesCountByLabelValuePair }'
```
`limit` is the number of items returned per set of statistics: the default is 10 and the maximum is 10000.
The data section also carries `memoryInBytesByLabelName` (memory per label name, the summed length of its values).
The endpoint is new in Prometheus v2.14.

## 2. PromQL drill-down (touches every series, so relatively expensive: do not hammer the server)
```promql
topk(10, count by (__name__)({__name__=~".+"}))            # series per metric
topk(10, count by (__name__, job)({__name__=~".+"}))       # per metric and job
topk(10, count by (job)({__name__=~".+"}))                 # jobs with most series
topk(20, scrape_samples_post_metric_relabeling)            # per target
```
`scrape_samples_post_metric_relabeling{job, instance}` is the number of samples left after metric relabeling;
`scrape_series_added{job, instance}` is the approximate number of new series in a scrape (since v2.10).

## 3. Mimir
- `GET` or `POST` `<prometheus-http-prefix>/api/v1/cardinality/label_names` counts distinct label values per label name;
  `.../cardinality/label_values` needs `label_names[]` and returns series count per label value.
  Both take an optional `limit` (default 20, min 0, max 500).
- The endpoints are disabled by default; enable with the `-querier.cardinality-analysis-enabled` flag (or its YAML option).

## 4. Decide
For each top metric: is it used? Which label explodes? Then fix the instrumentation, or drop the label at scrape time
with a `labeldrop` relabel action (removes every label whose name matches the regex), or drop the metric.

## Verify
- [ ] Each of the top metrics from step 1 has a decision (keep, reduce, drop).
- [ ] `headStats.numSeries` from step 1 is lower after the change.

## Checked
Checked 2026-11-07. Read the relevant sections only (the HTTP API pages are too large to read end to end): the TSDB Stats section of the Prometheus HTTP API page (limit default 10 / max 10000, headStats,
seriesCountByMetricName, labelValueCountByLabelName, memoryInBytesByLabelName, v2.14 note; the prose names the last set
seriesCountByLabelPair but the example response and this skill use seriesCountByLabelValuePair), the Mimir HTTP API sections for label
names and label values cardinality (limit default 20 max 500, `-querier.cardinality-analysis-enabled`), the whole Robust Perception
post (the three topk queries), the jobs-and-instances page (scrape_* series) and the `labeldrop` line of the configuration page
(the 200k-line configuration page was searched for that action, not read end to end). Removed: the web UI Status menu claim,
the `count by (le)` and distinct-label-value queries, `sort_desc(scrape_series_added)`, the `cardinality_analysis_enabled: true` YAML
spelling, Grafana Cloud dashboards and Adaptive Metrics, mimirtool, the `prometheus_tsdb_head_series` check and the 20 %/day alert
threshold (none of these are on a cited page). Robust Perception is a maintainer blog, not official documentation.
Method: documentation only; no commands were run.
