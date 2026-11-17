---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.choosing-rate-irate-increase-and-window
name: choosing-rate-irate-increase-and-window
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, rate, irate, increase, rate-extrapolation, non-integer-increase, irate-vs-rate, spiky-counters, rate-interval-sizing, scrape-interval-multiple, rate-interval]
level: practitioner
status: verified
description: "Pick between rate, irate and increase; understand extrapolation (why increase returns 2.4 for integer counters) and size windows with $__rate_interval."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#rate", "https://grafana.com/blog/2020/09/28/new-in-grafana-7.2-__rate_interval-for-prometheus-rate-queries-that-just-work/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rate vs irate vs increase, and window sizing

| Function | Computes | Use for |
|---|---|---|
| `rate(x[w])` | per-second average increase over w, extrapolated to window edges | alerts, recording rules, most graphs |
| `irate(x[w])` | per-second rate from the **last two** samples in w | zoomed-in volatile graphs only |
| `increase(x[w])` | `rate(x[w]) * w_seconds` | "how many in the last hour" tables/stats |

## Extrapolation (why increase isn't an integer)
Samples rarely sit exactly at window edges. `rate`/`increase` take the slope between the first and last
sample in the window and extrapolate to the window boundaries when the first/last sample is within 1.1 times the average
sample interval of the edge, otherwise by half an interval, and never below zero for a counter (`extrapolatedRate` in
`promql/functions.go`). So a counter that went 10 -> 12 within a 5 m window sampled every minute showed `increase = 2.5`. This is by design;
round in display, don't "fix" it with `delta` (which is for gauges and mishandles resets).

## irate pitfalls
- Looks only at the last 2 samples, so on a graph with step > scrape interval it **skips** most data and
  shows random spikes or misses them entirely.
- Never use in alerts or recording rules (flaps on single scrapes).

## Window sizing
- Minimum: the window must contain >= 2 samples; robust: >= 4 scrape intervals.
- Grafana `$__rate_interval` = max(4 x scrape interval, `$__interval` + scrape interval): always enough
  samples and never skipping data between steps. Set the data source's "Scrape interval" to your real
  scrape interval or it assumes 15 s.
- `rate(x[$__interval])` breaks at short zooms (window < 2 samples -> gaps).

## Order of operations
`sum by (job) (rate(x[5m]))`: rate first, then aggregate. Never `rate(sum(...))`; it requires a subquery
and turns individual counter resets into fake drops.

## Verify
- [ ] No `irate` in rule files: `grep -r irate rules/` empty.
- [ ] Grafana rate panels use `$__rate_interval`; no gaps when zooming to 5 minutes.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26.
- promtool tests: series `10 10 10 12 12 12` at 1m steps: `increase(a[5m])` at 5m = 2.5; `irate(cnt[5m])` over `0 1 2 ... 10` at 1m = 0.01667 (last two samples); `delta(cnt[5m])` = 5; one-sample `rate()` returned nothing; `increase(x[4m])` on `100 120 5 30` returned 66.67 (extrapolated from a raw increase of 50).
- Extrapolation rule: `extrapolatedRate` in prometheus `promql/functions.go` (1.1 x average interval threshold, half-interval fallback, zero point for counters).
- `$__rate_interval = max($__interval + scrape interval, 4 * scrape interval)`, Min step precedence and the 15 s default scrape interval: Grafana blog post on `$__rate_interval` quoting the Grafana documentation, and the Grafana Prometheus data-source configuration page (default 15s).
- `sum(rate())` ordering and the `rate(sum())` problem: see `counter-semantics-and-resets` (promtool test).
