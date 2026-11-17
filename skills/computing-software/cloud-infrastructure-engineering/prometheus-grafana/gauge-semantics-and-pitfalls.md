---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.gauge-semantics-and-pitfalls
name: gauge-semantics-and-pitfalls
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [gauge-semantics, gauge-pitfalls, data-model, metric-types, promql, prometheus]
level: practitioner
status: docs-checked
description: "Use gauges correctly: when a metric is a gauge rather than a counter, which PromQL functions suit gauges, timestamp gauges, and collect-time gauges."
sources: ["https://prometheus.io/docs/concepts/metric_types/#gauge", "https://prometheus.io/docs/practices/instrumentation/#counter-vs-gauge-summary-vs-histogram", "https://prometheus.io/docs/prometheus/latest/querying/functions/", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gauge semantics and pitfalls

A gauge is a single numerical value that can arbitrarily go up and down: measured values such as temperature or current
memory usage, and counts that can go down, such as concurrent requests. Rule of thumb: if the value can go down, it is a gauge.
Do not use a counter for a value that can decrease (for example, currently running processes).

## Functions that suit gauges
| Need | Use |
|---|---|
| Current level | the raw value; `last_over_time(x[5m])` returns the most recent sample in the interval |
| Smoothed level | `avg_over_time(x[5m])` |
| Peak in window | `max_over_time(x[1h])` (maximum of the float samples in the interval) |
| Change over window | `delta(x[2h])` (first to last value, extrapolated to the full range); `deriv(x[1h])` is the per-second derivative by simple linear regression |
| Forecast | `predict_linear(x[6h], 4*3600)` (seconds from now; documented as for gauges only) |

Never take a `rate()` of a gauge. `rate()` and `increase()` are counter functions: they adjust for breaks in monotonicity
(counter resets), which a gauge does not have.

## Pitfalls
- Events accumulated over time ("requests served") belong in a counter, read with `rate()`, not a gauge.
- A timestamp of when something happened is exported as a gauge holding the Unix timestamp; use `time() - my_timestamp_metric`
  for the time since. This needs no update logic and cannot get stuck. `time()` is the evaluation time of the expression.
- Exporting a duration as a gauge is acceptable only for a custom collector's collection time and for batch job durations,
  because those describe one scrape or push rather than many durations over time.

## Collect-time gauges
In the Go client, `NewGaugeFunc(opts, function)` makes a gauge whose value is determined at collect time by calling a
provided function, useful for values already held in memory.

## Verify
- [ ] No `rate(` or `increase(` is applied to a gauge in dashboards and rules.
- [ ] Every decreasing value is a gauge and every only-increasing event total is a counter.

## Checked
Checked 2026-11-07. Read in full: the Prometheus instrumentation practices page (the counter-vs-gauge, timestamps-not-time-since,
collectors and avoid-missing-metrics parts used here) and the metric types page (the counter and gauge sections that frame this skill; the page also
covers histogram and summary, which I read only far enough to confirm the counter and gauge text). From the functions page I read the
delta, deriv, predict_linear, rate, increase, time and `<aggregation>_over_time` entries (not the whole page). From the Go client page
I read the GaugeFunc type and NewGaugeFunc lines only. Removed as unconfirmed by these pages: the sampling-aliasing
example, the max-since-last-scrape gauge, the ratio and average-of-percentages advice, the "any decrease is a counter reset" phrasing, and the pint
suggestion in Verify. Added from the pages: the collector and batch duration exception.
Method: documentation only; no commands were run.
