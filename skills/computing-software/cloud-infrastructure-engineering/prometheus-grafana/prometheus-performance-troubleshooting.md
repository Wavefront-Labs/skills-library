---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-performance-troubleshooting
name: prometheus-performance-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, prometheus-troubleshooting, prometheus-memory, slow-queries, query-log, query-timeout, max-samples, max-concurrency, lookback-delta, oom, head-series, churn, tsdb-status, promtool-tsdb-analyze, pprof, rule-evaluation-slow, missed-evaluations, scrape-pool-exhaustion, query-limits, pca]
level: advanced
status: docs-checked
description: "Diagnose a struggling Prometheus: series cardinality via the TSDB status API, slow queries via the query log and limit flags, rule concurrency and compaction disk headroom."
sources: ["https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://prometheus.io/docs/guides/query-log/", "https://prometheus.io/docs/prometheus/latest/storage/", "https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-stats"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Prometheus performance troubleshooting

**Goal:** when Prometheus is slow, OOMing or missing evaluations, find the single cause
(series, churn, query, rule or disk) using built-in signals.

## 1. Memory and series
- Memory scales with active series and the query working set. Measure bytes per series on your
  own server (resident memory divided by head series, both from Prometheus's own `/metrics`)
  rather than trusting a rule of thumb. If the server cannot hold its series, shard or cut cardinality.
- `GET /api/v1/status/tsdb` (also shown on the TSDB status page in the UI) returns
  `seriesCountByMetricName`, `labelValueCountByLabelName`, `memoryInBytesByLabelName` and
  `seriesCountByLabelPair`. The `limit` parameter defaults to 10 items per set; the maximum is
  10000. This finds the one metric or label (for example a request-id label) driving cardinality.
- Churn means labels change every scrape (pod restarts, timestamps in labels): new series keep
  appearing while the total stays flat. Fix at the source with `metric_relabel_configs` drops and
  a per-job `sample_limit`.
- Kubernetes OOMKills show as restarts; leave memory headroom over steady-state use because
  compaction and large queries spike.

## 2. Slow or expensive queries
Enable the query log in `prometheus.yml` and reload (POST to `/-/reload` when started with
`--web.enable-lifecycle`, otherwise send SIGHUP on non-Windows):
```yaml
global:
  query_log_file: /prometheus/query.log
```
Each line is JSON with `params` (the query, start, end and step) and `stats` (internal engine
timers such as `timings.evalTotalTime`), so you can find which dashboard or user is heavy. The
metric `prometheus_engine_query_log_enabled` is 1 when the log is on. Remove `query_log_file` and
reload to disable it.

Guard-rail flags, with the defaults on the command-line page:
- `--query.timeout` (2m): maximum time a query may take before being aborted.
- `--query.max-concurrency` (20): queries executed concurrently.
- `--query.max-samples` (50000000): queries fail if they try to load more samples into memory.
- `--query.lookback-delta` (5m): maximum lookback for retrieving metrics during evaluation.
Typical offenders: very long `rate()` ranges, regex matchers on `__name__`, high-cardinality joins,
`topk` over unaggregated series, dashboards refreshing every few seconds. Precompute with recording
rules.

## 3. Rules
- `--rules.max-concurrent-evals` (default 4) is the global concurrency limit for independent
  rules that can run concurrently; when set, `--query.max-concurrency` may need adjusting too.
- Split heavy rule groups or precompute intermediate recording rules.

## 4. Disk and compaction
- Blocks are written about every two hours and compacted in the background into larger blocks
  spanning up to 10% of the retention time or 31 days, whichever is smaller. Source and compacted
  blocks coexist on disk, so on-disk size can briefly exceed `storage.tsdb.retention.size`.
- The storage page recommends setting the retention size to at most 80-85% of the allocated disk
  so compactions have the remaining 15-20% as buffer.
- WAL compression is enabled by default (flag `--storage.tsdb.wal-compression`).
- Expired block cleanup is a background job and may take up to two hours.

## Verify
- [ ] You can name the top metrics by series count and the largest label from the TSDB status API without guessing.
- [ ] No query hits `--query.max-samples` or the timeout after your change.
- [ ] Retention size leaves the compaction buffer the storage page recommends.

## Checked
2026-11-01. Confirmed on the Prometheus command-line page: query.timeout 2m, query.max-concurrency 20,
query.max-samples 50000000, query.lookback-delta 5m, rules.max-concurrent-evals 4 and its note,
web.enable-lifecycle. Confirmed on the query-log guide: query_log_file, reload by HTTP or SIGHUP,
params/stats fields, evalTotalTime, prometheus_engine_query_log_enabled. Confirmed on the HTTP API
page: the TSDB stats endpoint, its four statistics, default limit 10, maximum 10000. Confirmed on the
storage page: two-hour blocks, compaction span, 80-85% retention advice, WAL compression, cleanup delay.
Removed: the self-monitoring metric names other than the query-log one, the promtool tsdb analyze and
list commands, pprof recipes, the 2 h head-churn claim, scrape-limit metric names, Kubernetes probe
advice, the hashmod sharding advice and the Mimir/Thanos recommendation, since no fetched page states them.
Method: documentation only; no commands were run.
