---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.instrumenting-inner-loops-and-hot-paths
name: instrumenting-inner-loops-and-hot-paths
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [inner-loop-instrumentation, hot-path-metrics-cost, instrumentation, client-golang, performance]
level: advanced
status: docs-checked
description: "Instrument tight loops and hot paths without measurable overhead: limit metrics updated, cache child metrics instead of per-call label lookups, mind timing syscalls, benchmark."
sources: ["https://prometheus.io/docs/practices/instrumentation/#inner-loops", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumenting inner loops and hot paths

prometheus.io Instrumentation, "Inner loops": in general the extra resource cost of instrumentation is far outweighed by its
benefits. For code that is performance-critical or called more than 100k times a second inside a given process, take some
care over how many metrics you update. The page's figure: a Java counter takes 12-17ns to increment depending on
contention, and other languages will be similar.

## Techniques (from the page)
1. Limit the number of metrics incremented in the inner loop.
2. Avoid labels in the loop, or cache the result of the label lookup: the page names the return value of `With()` in Go and `labels()` in Java.
   In the Go client, `WithLabelValues` returns the child counter for a label combination, creating it on first access, so resolve it once outside the loop:
```go
okCounter := reqs.WithLabelValues("GET", "2xx") // lookup happens once here
for _, item := range batch {
    process(item)
    okCounter.Inc()
}
```
3. Beware metric updates involving time or durations: getting the time may involve a syscall.
4. For values you already track (a queue length, a pool size), a collect-time metric avoids updating on every operation:
   `NewGaugeFunc` in the Go client is a gauge whose value is determined at collect time by calling a provided function.
5. Benchmarks are the best way to determine the impact of any given change.

## Verify
- [ ] A benchmark of the hot path with and without the metric updates shows the cost you can accept.
- [ ] No label lookups (`WithLabelValues`, `labels()`) remain inside per-item loops.

## Checked
Checked 2026-11-07. Read in full: the Prometheus instrumentation practices page (the "Inner loops" section: the 100k per second guideline, the 12-17ns Java
figure, avoiding labels or caching the lookup, the time syscall warning, and benchmarks). From the Go client package page (171k
characters, not read end to end) I read the WithLabelValues, GetMetricWithLabelValues and GaugeFunc text. Corrected: the
old text quoted a "12-15ns" figure that the page does not contain (it says 12-17ns for a Java counter). Removed as not on the cited pages: batching with
`Add(n)`, sampling histogram observations, the string-formatting advice, the single-digit-ns and "several times slower" expectations,
the native histogram and Python client lock remarks, and the 1-2 percent threshold. The histograms practices page was dropped from sources.
Method: documentation only; no commands were run.
