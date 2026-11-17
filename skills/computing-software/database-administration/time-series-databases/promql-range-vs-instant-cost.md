---
id: computing-software.database-administration.time-series-databases.promql-range-vs-instant-cost
name: promql-range-vs-instant-cost
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-promql-cost, promql-range-vs-instant-cost, prometheus]
level: practitioner
status: docs-checked
description: "Measure and cut PromQL query cost with query stats, step width, query limits, the query log and recording rules."
sources:
  - https://prometheus.io/docs/prometheus/latest/querying/api/
  - https://prometheus.io/docs/prometheus/latest/command-line/prometheus/
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/prometheus/latest/feature_flags/
  - https://prometheus.io/docs/prometheus/latest/querying/functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query cost of range and instant selectors

**Goal:** Write PromQL that reads fewer samples and series.

## Steps
- Measure first: add `stats=all` to a query request (`/api/v1/query` or `/api/v1/query_range`). The response includes `totalQueryableSamples`, the number of samples loaded; for range-vector functions over multiple steps, each step counts the full window.
- `/api/v1/query_range` takes a `step` (resolution) parameter; a wider step means fewer evaluations.
- Select with specific label matchers, for example `http_requests_total{job="api"}` rather than a bare metric name. Selecting every series with `{__name__=~".+"}` matches all series.
- Combine `rate()` with aggregation in the documented order: take `rate()` first, then aggregate (`sum(rate(...))`), otherwise counter resets cannot be detected.
- Bound resources with `--query.max-samples` (default 50000000; queries loading more fail) and `--query.timeout` (default 2m).
- Log queries to a file with `query_log_file` in the global config to find heavy ones; reloading the config reopens the file.
- Move repeated expensive expressions into recording rules (see prometheus-recording-rules).

**Gotcha:** Every dashboard panel repeats its query on each refresh, so many panels over long ranges multiply load; use recording rules for them.

## Verify
- `totalQueryableSamples` drops after the change.
- Dashboard latency improves.

## Checked
2026-11-03. Confirmed against the HTTP API page (`stats`, `totalQueryableSamples`, `step`), the command-line page (`--query.max-samples`, `--query.timeout` defaults), the configuration reference (`query_log_file`), the feature flags page (per-step stats semantics) and the functions page (rate then aggregate). Removed: the regex-vs-equality speed claim, the "4 scrape intervals" window rule, `$__rate_interval` (a Grafana variable), the claim that topk/count over all series forces a full index scan, and the 50 panels / 5 s / 30 days example.
Method: documentation only; no commands were run.
