---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.counter-semantics-and-resets
name: counter-semantics-and-resets
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, counter-semantics, counter-resets, rate, created-timestamp, data-model, pca]
level: practitioner
status: verified
description: "Use counters correctly: monotonic semantics, how rate/increase handle resets, the first-sample problem, created timestamps, and the mistakes that produce fake spikes."
sources: ["https://prometheus.io/docs/concepts/metric_types/#counter", "https://prometheus.io/docs/prometheus/latest/querying/functions/#rate", "https://prometheus.io/docs/practices/instrumentation/#avoid-missing-metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counter semantics and reset handling

## Rules
- A counter only goes up, or resets to 0 when the process restarts. Name it `*_total`.
- Never `set()` a counter to an absolute value from elsewhere unless it is itself monotonic (that's what
  exporters do with kernel counters: fine).
- Never decrement. Things that go down are gauges.
- Always query with `rate()`/`increase()`; the raw value is meaningless across restarts.

## How resets are handled
`rate`, `irate`, `increase` treat any decrease as a reset: for samples `100, 120, 5, 30` the raw increase is
`20 + 5 + 25 = 50` (it assumes the counter went 0->5 after the reset). `increase()` then extrapolates to the
window edges: a promtool test with those four samples 1m apart returned `66.67` for `increase(x[4m])` at the last sample.
- `resets(x[1h])` counts them; a high count on a supposedly stable process reveals crash loops.
- **Fake spike**: a counter that *isn't* monotonic (e.g. a gauge named `_total`, or two pods writing the same
  series via Pushgateway) looks like resets and produces huge rates.
- **Aggregate after rate**: `sum(rate(x[5m]))`, never `rate(sum(x)[5m])` (a single pod restart makes the
  sum drop, which rate reads as a reset of the whole sum). In a promtool test with two pods at 1 req/s, one
  restarting mid-window, `sum(rate(x[5m]))` gave `1.8` and `rate(sum(x)[5m:1m])` gave `2`.

## First-sample problem
A new series starting at 1 (first error ever) has no prior sample, so the jump from nothing to 1 is invisible to
`increase()`/`rate()` (a window holding one sample returns no result). Fixes:
- Initialise label combinations you know at startup to 0 (`counter.WithLabelValues("500").Add(0)`).
- Created timestamps: `--enable-feature=created-timestamp-zero-ingestion` inserts a synthetic 0 sample at the
  exposed `_created` time so the first increment counts. Run here against a Python client exposing OpenMetrics:
  with the flag the series started with a `0` sample and no `_created` series was stored; without it the first
  stored sample was already 9 and `http_requests_created` was stored as an ordinary series. Prometheus 3.15 also
  has `--enable-feature=st-storage` (start timestamps stored natively, see its feature-flags page).

## Gotchas
- `rate` over a window with only one sample returns nothing; window must cover >= 2 scrapes (use 4x).
- Counters in floats lose precision above 2^53; not an issue for practical counts.
- Pushgateway counters from batch jobs reset every run; use `push_time_seconds` and gauges for last-run values.

## Verify
- [ ] Every `_total` metric is queried via rate/increase in dashboards and rules.
- [ ] `resets(metric[1d])` matches known deploys/restarts.
- [ ] Known label values are pre-initialised so first errors show up.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), prometheus_client 0.26.0 on Python 3.14, client_golang 1.25.0 on Go 1.26.
- Reset handling and extrapolation: promtool `test rules` with series `100 120 5 30` (`resets()` = 1, `increase(x[4m])` at 3m = 66.67); one-sample `rate()` returned nothing.
- `sum(rate())` vs `rate(sum())`: two-pod promtool test (1.8 vs 2).
- Zero injection: Prometheus 3.15.1 with and without `created-timestamp-zero-ingestion` scraping a prometheus_client OpenMetrics target; `_created` stored only without the flag. Flag text from the 3.15 feature-flags page.
- `counter.WithLabelValues("500").Add(0)` compiled and registered one series (client_golang 1.25.0).
- Float precision: Python `float(2**53)+1 == float(2**53)` is True. Pushgateway 1.11.4 exposes `push_time_seconds` per group.
