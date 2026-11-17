---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.initialising-label-values-to-avoid-missing-metrics
name: initialising-label-values-to-avoid-missing-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [initialize-label-values, avoid-missing-metrics, instrumentation, client-libraries, promql, counters]
level: practitioner
status: docs-checked
description: "Pre-initialise known label combinations of labelled metrics so the series exist from process start; client library calls for Go, Python and Java."
sources: ["https://prometheus.io/docs/practices/instrumentation/#avoid-missing-metrics", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus", "https://prometheus.github.io/client_python/instrumenting/labels/", "https://prometheus.github.io/client_java/api/io/prometheus/metrics/core/metrics/Counter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initialising label values (avoid missing metrics)

prometheus.io Instrumentation: "Time series that are not present until something happens are difficult to deal with, as the
usual simple operations are no longer sufficient to correctly handle them." The page's advice is to export a default value
such as 0 for any time series you know may exist in advance. Most client libraries (including Go, Java and Python)
export a 0 automatically for metrics with no labels, so this is only needed for metrics with labels.

## Code
Go (client_golang): `WithLabelValues` returns the child for those label values and creates it the first time that
combination is accessed, so touching each known combination at start-up exports it.
```go
var reqs = promauto.NewCounterVec(prometheus.CounterOpts{Name: "app_requests_total"}, []string{"method", "code"})
func init() {
    for _, m := range []string{"GET", "POST"} {
        for _, c := range []string{"2xx", "4xx", "5xx"} {
            reqs.WithLabelValues(m, c) // creates the child
        }
    }
}
```
Python: the client docs say metrics with labels are not initialized when declared, because the client cannot know what
values a label can have, and recommend initialising by calling `.labels()` alone.
```python
from prometheus_client import Counter
JOBS = Counter("app_jobs_total", "Jobs processed", ["result"])
for r in ("success", "failure"):
    JOBS.labels(result=r)  # touch to create the labelset
```
Java (client_java): the Counter API page lists `initLabelValues` among its inherited methods (next to `labelValues`, `remove`, `clear`);
check that page for its exact signature before use.

## Rules
- Only for bounded, known label values. Never pre-create per-user or per-path series (every labelset is a series).
- Label-less metrics need nothing.

## Verify
- [ ] After a fresh process start, the metrics endpoint shows each known label combination.

## Checked
Checked 2026-11-07. Read in full: the Prometheus instrumentation practices page (quote and default-0 advice from "Avoid missing
metrics"), the client_python Labels page (initialisation paragraph and example) and the client_python landing page. From the Go package page (171k characters, not read end to end) I read the WithLabelValues and
GetMetricWithLabelValues text and the promauto mention; from the client_java Counter API page I confirmed the method name
`initLabelValues` in the inherited-methods list only, with no description of its behaviour. Removed as not stated on the cited pages: the
rate()-needs-two-samples explanation, the claim that error ratios return no data, the "No data" dashboard remark, the
`or vector(0)` PromQL fallback, the preference for status classes, and the Java `counter.initLabelValues("success")` call form.
Method: documentation only; no commands were run.
