---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-rate-then-sum
name: promql-rate-then-sum
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [rate-then-sum, sum-then-rate-mistake, rate, aggregation, counter-resets, promql]
level: practitioner
status: verified
description: "Always apply rate()/increase() to raw counters before sum(); why sum-then-rate breaks on counter resets and how to rewrite subqueries that do it."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#rate", "https://prometheus.io/docs/practices/rules/", "https://prometheus.io/docs/prometheus/latest/querying/examples/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate then sum

prometheus.io: "When combining rate() with an aggregation operator (e.g. sum()) or a function aggregating over time (any function ending in _over_time), always take a rate() first, then aggregate. Otherwise rate() cannot detect counter resets when your target restarts."

## Right vs wrong
```promql
# right
sum by (job) (rate(http_requests_total[5m]))
# wrong: summed counter drops when one instance restarts; rate sees a "reset" and spikes
rate(sum by (job) (http_requests_total)[5m:])
# wrong in recording rules: recording the sum of raw counters, then rating the recorded series
record: job:http_requests_total:sum      # do not
expr: sum by (job) (http_requests_total)
```
Record rates instead: `job:http_requests:rate5m = sum by (job) (rate(http_requests_total[5m]))`.

## Why
Each instance's counter resets independently. `rate()` handles a reset per series (any decrease = reset, adds the pre-reset value). After `sum`, a reset in one series is a small decrease in the total, which `rate` misreads as a reset of the whole sum, producing a huge spike, or the decrease is hidden.

## Same rule for
- `increase()` then `sum`.
- Ratios: `sum(rate(errors[5m])) / sum(rate(requests[5m]))`, never `rate(sum(errors)) / ...`.
- Histograms: `sum by (le) (rate(x_bucket[5m]))` before `histogram_quantile`.
- `max_over_time(rate(x[5m])[1h:])` is fine (rate inside); `rate(max_over_time(...))` is not.

## Measured
Prometheus 3.15.0, one counter that resets from 50 to 0 and one that keeps climbing 10 per minute: `sum(rate(c[5m]))` stays at about 0.29/s, but `rate(sum(c)[5m:1m])` jumps to 4.67/s for every window that contains the reset (the small dip in the total is read as a full reset and the whole pre-reset total is added back).

## Gotchas
- Federating summed raw counters to a global server reintroduces the problem; federate rates.

## Verify
- [ ] No rule or panel contains `rate(sum(` or rates a recorded `:sum` counter (grep, or pint's `promql/rate` check, which reports `rate()` over `sum(counter)`).
