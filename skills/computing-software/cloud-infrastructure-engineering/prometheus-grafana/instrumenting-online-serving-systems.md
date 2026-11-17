---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.instrumenting-online-serving-systems
name: instrumenting-online-serving-systems
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [online-serving-instrumentation, request-instrumentation, instrumentation, red-method, prometheus-best-practices]
level: practitioner
status: docs-checked
description: "Instrument an online-serving system per Prometheus guidance: queries, errors, latency and in-progress requests on client and server, with Go promhttp middleware and label limits."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://prometheus.io/docs/practices/histograms/", "https://prometheus.io/docs/practices/naming/", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus/promhttp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumenting online-serving systems

An online-serving system is one where a human or another system expects an immediate response (most database and HTTP
requests). The Prometheus instrumentation page says the key metrics are the number of performed queries, errors and latency;
in-progress requests can also be useful. Monitor both the client and the server side: if the two see different behaviour that is
useful for debugging, and a service with many clients cannot track them individually. Be consistent about counting queries when
they start or when they end; ending is suggested, since it lines up with the error and latency stats.

## Server side (Go, promhttp middleware)
`promhttp.InstrumentHandlerCounter` and `InstrumentHandlerDuration` wrap an `http.Handler`. The vector passed in may have
zero, one or two non-const, non-curried labels, and only `code` and `method` are allowed for those (the functions panic
otherwise); curried labels such as a route or handler name are injected with `MustCurryWith`. The duration is observed in
seconds. The package notes that partitioning histograms is expensive and should be used judiciously.
```go
inflight := promauto.NewGauge(prometheus.GaugeOpts{Name: "http_requests_in_flight"})
reqs := promauto.NewCounterVec(prometheus.CounterOpts{Name: "http_requests_total"}, []string{"code", "method", "route"})
dur := promauto.NewHistogramVec(prometheus.HistogramOpts{
    Name: "http_request_duration_seconds", NativeHistogramBucketFactor: 1.1}, []string{"method", "route"})
route := prometheus.Labels{"route": "/orders/{id}"}
h := promhttp.InstrumentHandlerInFlight(inflight,
    promhttp.InstrumentHandlerDuration(dur.MustCurryWith(route),
        promhttp.InstrumentHandlerCounter(reqs.MustCurryWith(route), handler)))
```
`NativeHistogramBucketFactor` (a field of `HistogramOpts`) is the Go option used in the histograms practices page's example (1.1).

## Client side
`promhttp.InstrumentRoundTripperCounter`, `InstrumentRoundTripperDuration` and `InstrumentRoundTripperInFlight` wrap an
`http.RoundTripper` for outbound calls.

## Rules
- Use one metric with a label rather than one metric per outcome: for example one `http_responses_total` with a `code` label,
  not one metric per status code; no part of a metric name should be procedurally generated.
- Every labelset is another time series with costs; keep label cardinality low and do not use raw paths as label values.
- For failures, increment a counter on each failure and also have a total-attempts metric so the failure ratio is easy to
  calculate.
- Export a default (such as 0) for any known label combination so series exist before the first request.
- Use base units (seconds) in names.
- To measure an SLO threshold with classic histograms, have a bucket boundary exactly at the threshold (the practices page
  uses 0.3 for 300 ms); native histograms avoid that constraint.

## Queries (illustrations)
```promql
sum by (route) (rate(http_requests_total{code=~"5.."}[5m])) / sum by (route) (rate(http_requests_total[5m]))
histogram_quantile(0.99, sum by (le, route) (rate(http_request_duration_seconds_bucket[5m])))   # classic histogram
```

## Verify
- [ ] Requests, errors and latency are exported on both the server and, for each dependency, the client side.
- [ ] The number of series stays flat as traffic varies.

## Checked
Checked 2026-11-07. Read in full: the Prometheus instrumentation practices page (online-serving, failures, labels, counter vs gauge, avoid missing
metrics) and the histograms practices page (read in full for another skill in this batch; used here for bucket and native-histogram guidance). From the
promhttp package page I read lines 60-185 (the middleware function list, InstrumentHandlerCounter and InstrumentHandlerDuration text and the example), not the whole page.
From the Go client page I confirmed MustCurryWith and the HistogramOpts NativeHistogramBucketFactor field by search. Naming: base-unit rule only. Corrected: the old example omitted
that these middleware allow only `code` and `method` as remaining labels; I reordered the label sets accordingly. Removed: the explicit bucket list, the
`status_class` idea, a separate `errors_total{reason}` metric, client metric names, the `curl | grep` verify step, and the promhttp InstrumentHandlerInFlight
signature was not read (it appears in the page's example only).
Method: documentation only; no commands were run.
