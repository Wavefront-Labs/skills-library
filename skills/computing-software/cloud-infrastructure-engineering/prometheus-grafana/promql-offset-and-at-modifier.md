---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-offset-and-at-modifier
name: promql-offset-and-at-modifier
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, offset, at-modifier, offset-comparison, week-over-week, at-modifier-usage, start-end-modifiers]
level: practitioner
status: verified
description: "Compare against the past with offset (week-over-week ratios, negative offsets) and pin evaluation time with @ <ts>, @ start() and @ end() for stable top-N and baselines."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/basics/#offset-modifier", "https://prometheus.io/docs/prometheus/latest/querying/basics/#modifier"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# offset and @ modifiers

## offset
Shifts the selector's evaluation time into the past; applies to the selector it follows.
```promql
# Week-over-week traffic ratio
sum(rate(http_requests_total[5m])) / sum(rate(http_requests_total[5m] offset 1w))
# Alert when today's traffic is < 50% of the same time last week (and last week had real traffic)
(sum(rate(http_requests_total[10m])) / sum(rate(http_requests_total[10m] offset 1w)) < 0.5)
  and sum(rate(http_requests_total[10m] offset 1w)) > 10
# Average of several past weeks as baseline (smoother)
(sum(rate(x[5m] offset 1w)) + sum(rate(x[5m] offset 2w)) + sum(rate(x[5m] offset 3w))) / 3
```
- Syntax: `metric{...}[5m] offset 1w` (offset after the range); for subqueries `(...)[1h:5m] offset 1d`.
- Negative offsets look forward (`offset -1h`); stable since 2.33.0 and no flag is needed in 3.x; only useful for backfilled data.
- Holidays and deploys make WoW alerts noisy; combine with absolute guards.

## @ modifier
Evaluates the selector at a fixed time regardless of the query's evaluation time.
```promql
http_requests_total @ 1697400000                            # value at a unix timestamp
rate(http_requests_total[5m] @ end())                       # value at the end of the query range
topk(5, sum by (pod) (rate(x[5m] @ end())))                 # stable top-N set for a whole graph
x / (x @ start())                                            # growth relative to the start of the range
```
- `start()` and `end()` are the range query's start/end (for instant queries, both = evaluation time).
- Combine with offset: `x @ end() offset 1d` = one day before the end time.
- In rules, `@` pins forever, rarely what you want; use it in dashboards and ad-hoc analysis.

## Checked
On Prometheus 3.15.0: a negative offset needed no flag (the `promql-negative-offset` and `promql-at-modifier` flags were removed in 3.0; both were promoted to stable in 2.33.0); `ht @ end() offset 10m` returned the value 10 minutes before the evaluation time; `x / (x @ start())` over a range started at 1 and grew; `max_over_time((ht)[10m:1m] offset 10m)` and `rate(ht[5m] @ end())` parse and run.

## Verify
- [ ] WoW panels show ~1.0 on normal days.
- [ ] Top-N panels using `@ end()` keep the same series when panning within the range.
