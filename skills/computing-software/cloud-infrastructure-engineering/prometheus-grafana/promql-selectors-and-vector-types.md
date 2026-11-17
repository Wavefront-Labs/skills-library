---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-selectors-and-vector-types
name: promql-selectors-and-vector-types
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, promql, promql-selectors, label-matchers, instant-vector, range-vector, scalar, string, regex-matchers, negative-matchers, metric-name-matcher, lookback-delta, staleness, evaluation-time, step, duration-literals, promql-types, api-query, api-query-range, promtool-query, pca]
level: practitioner
status: docs-checked
description: "PromQL building blocks: the four result types, instant vs range selectors, matcher semantics and anchoring, lookback/staleness, durations, and query vs query_range."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/basics/", "https://prometheus.io/docs/prometheus/latest/querying/api/", "https://prometheus.io/docs/prometheus/latest/querying/examples/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PromQL selectors and vector types

**Goal:** write selectors that return exactly the series you mean, and know which
expression types feed which functions, so type errors and empty results stop surprising
you.

## 1. Four types, and what accepts what
| Type | Example | Produced by | Consumed by |
|---|---|---|---|
| instant vector | `up{job="api"}` | selector, most functions, aggregations | aggregations, binary ops, `abs()`, `histogram_quantile()`, panels |
| range vector | `up{job="api"}[5m]` | selector with `[d]`, subquery `expr[1h:1m]` | `rate()`, `increase()`, `*_over_time()`, `changes()`, `delta()` |
| scalar | `3`, `scalar(v)`, `time()` | literals, `scalar()`, `time()` | arithmetic with vectors, `vector(s)` |
| string | `"x"` | literals only | `label_replace()` args |
Range vectors cannot be graphed directly or aggregated; wrap them. `rate(x)` without `[d]`
is a type error; `sum(x[5m])` too.

## 2. Matchers
```promql
http_requests_total{job="api", method!="OPTIONS", path=~"/api/v[12]/.*", status!~"2..|3.."}
{__name__=~"job:.*:rate5m", cluster="prod"}       # metric name as a label
```
- `=~`/`!~` are **fully anchored** RE2: `=~"api"` matches only exactly `api`; use `.*api.*`.
- A selector must have at least one matcher that does not match the empty string
  (`{job=~".*"}` alone is rejected; `{job=~".+"}` is fine).
- `status=""` matches series **without** the label; `status!=""` requires it.
- Regex alternation is cheaper than several `or` clauses; still, a regex on a
  high-cardinality label touches every series of that metric.

## 3. Instant queries, lookback and staleness
- An instant vector at time *t* returns, per series, the **latest sample within the
  lookback window** (default 5m, `--query.lookback-delta`), unless a staleness marker
  sits between — then nothing. That is why a target that stopped 6 minutes ago vanishes
  and why `scrape_interval` > 5m breaks everything.
- A range vector `[5m]` is the samples from the last 5m up to *t*. `rate()` therefore needs ≥2 samples in the
  window: use at least `4 × scrape_interval` (`$__rate_interval` in Grafana).
- Durations: `ms, s, m, h, d, w, y` and combinations `1h30m`. Offsets and `@` are in
  `...prometheus-grafana.promql-query-patterns`.

## 4. query vs query_range
```bash
curl -s 'localhost:9090/api/v1/query' --data-urlencode 'query=sum(rate(http_requests_total[5m]))' --data-urlencode 'time=2026-10-15T10:00:00Z'
curl -s 'localhost:9090/api/v1/query_range' --data-urlencode 'query=sum(rate(http_requests_total[5m]))' \
  --data-urlencode 'start=2026-10-15T09:00:00Z' --data-urlencode 'end=2026-10-15T10:00:00Z' --data-urlencode 'step=60s'
promtool query instant http://localhost:9090 'up == 0'
promtool query range --start=-1h --step=1m http://localhost:9090 'rate(x[5m])'
```
- `query_range` is just an instant query evaluated at every `step` from start to end; each
  step is independent (so `rate(x[5m])` at step 60s re-reads overlapping windows; cost grows
  with `range/step × window`).
- Result `resultType` is `vector`/`matrix`/`scalar`/`string`; Grafana wants `matrix` for
  time series panels and `vector` for tables with `Format: Table` + instant.
- In Grafana, `max data points` and `min step` control the step.

## 5. Reading a result
```json
{"metric":{"__name__":"up","instance":"a:9100","job":"node"},"value":[1760522400.123,"1"]}
```
Values are strings; `NaN` and `+Inf` appear as such. An empty `result: []` is **success**
with no match — the most common "bug" is a label value typo or a matcher anchored too tightly.
Check with `count({__name__="metric"})` or the `/api/v1/series?match[]=` endpoint, then
`label_values` for the exact spelling.

## Gotchas
- `sum(up{job="api"}[5m])` → "expected type instant vector, got range vector".
- `rate(sum(x)[5m])` → error: a range selector needs a selector or subquery:
  `rate(sum(x)[5m:1m])` (subquery) or, better, `sum(rate(x[5m]))`.
- Comparison operators drop non-matching series unless `bool`; a graph of `up == 0` shows
  nothing when healthy, not a 0 line.

## Checked
2026-10-31. Confirmed on the PromQL basics page: duration units `ms s m h d w y`, `1h30m`, fully anchored regex matchers, the rule that a selector needs a matcher not matching the empty string, lookback semantics; command-line page: `--query.lookback-delta` default 5m. Removed: UTF-8 label-name note, left-open interval aside and the 11,000 point cap (not found in the fetched docs).
Method: documentation only; no commands were run.

## Verify
- [ ] Each selector in your dashboards returns the expected series count (`count(...)`) and no accidental `exported_*` labels.
- [ ] Every `rate()` window is ≥ 4 × the job's scrape interval.
- [ ] You can explain why an instant query at *t* returned a value with timestamp *t-3m*.
