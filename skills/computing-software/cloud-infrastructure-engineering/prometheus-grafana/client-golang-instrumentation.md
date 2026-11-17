---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.client-golang-instrumentation
name: client-golang-instrumentation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, client-golang-usage, promauto, go-collector, custom-collector-implementation, collect-callback, exemplar-instrumentation, client-exemplars, golang, promhttp]
level: practitioner
status: docs-checked
description: "Instrument Go services with client_golang: promauto vs custom registries, runtime collectors, promhttp handler, writing a custom Collector, and attaching exemplars."
sources: ["https://pkg.go.dev/github.com/prometheus/client_golang/prometheus", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus/promhttp", "https://prometheus.io/docs/guides/go-application/", "https://prometheus.io/docs/prometheus/latest/feature_flags/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client_golang instrumentation

## Registry and handler
The Prometheus Go guide uses its own registry, registers the Go and process collectors on it, and serves it with `promhttp.HandlerFor`:
```go
reg := prometheus.NewRegistry()
reg.MustRegister(
    collectors.NewGoCollector(),
    collectors.NewProcessCollector(collectors.ProcessCollectorOpts{}),
)
http.Handle("/metrics", promhttp.HandlerFor(reg, promhttp.HandlerOpts{}))
```
- `promhttp.Handler()` serves `prometheus.DefaultGatherer` and is already instrumented; `HandlerFor` is for a custom registry or non-default `HandlerOpts` and is not instrumented (wrap with `InstrumentMetricHandler` to get `promhttp_metric_handler_requests_total` and `promhttp_metric_handler_requests_in_flight`).
- The `prometheus.NewGoCollector` / `NewProcessCollector` constructors are marked deprecated on pkg.go.dev; the guide uses the `collectors` package versions.
- `MustRegister` panics on a registration error; `Register` returns it. Re-registering an equal collector returns an `AlreadyRegisteredError`.
- `HandlerOpts` has `ErrorHandling`, `ErrorLog`, `Registry` (adds `promhttp_metric_handler_errors_total`), `MaxRequestsInFlight` (503 above the limit), `Timeout` (503 on timeout, but gathering keeps running in the background) and `EnableOpenMetrics`.

## Your own metrics with promauto
The guide registers metrics on a registry you pass in, using `promauto.With(reg)`, which creates and registers in one call:
```go
type metrics struct{ opsProcessed prometheus.Counter }

func newMetrics(reg prometheus.Registerer) *metrics {
    return &metrics{
        opsProcessed: promauto.With(reg).NewCounter(prometheus.CounterOpts{
            Name: "myapp_processed_ops_total",
            Help: "The total number of processed events",
        }),
    }
}
```
Vectors: `NewCounterVec(opts, []string{"code","method"})`, `NewHistogramVec` (default buckets `prometheus.DefBuckets`, tailored to network-service response times in seconds, so usually set your own). `WithLabelValues(...)` panics on a wrong number of label values; `GetMetricWithLabelValues` returns an error instead. Keep the returned child for hot paths instead of looking it up each time.

## HTTP middleware
`promhttp.InstrumentHandlerDuration(obsVec, next)`, `InstrumentHandlerCounter`, `InstrumentHandlerInFlight`, `InstrumentHandlerRequestSize` and `InstrumentHandlerResponseSize`. The vector may have only `code` and/or `method` as non-curried labels (it panics otherwise); curry other labels in with `MustCurryWith(prometheus.Labels{"handler": "push"})`. Partitioning histograms is expensive, so use it judiciously. Client side: `InstrumentRoundTripperCounter`, `...Duration`, `...InFlight`, `...Trace`. Use `WithLabelFromCtx` / `WithLabelFromRequest` for extra labels, and sanitise external input to avoid cardinality blowups (the page's own warning).

## Exemplars
- A histogram observer implements `prometheus.ExemplarObserver`: `ObserveWithExemplar(value, prometheus.Labels{"trace_id": id})`. Counters implement `ExemplarAdder.AddWithExemplar`. It panics on invalid labels or more than 128 runes of labels in total; nil labels keep the existing exemplar.
- In middleware, `promhttp.WithExemplarFromContext(fn)` / `WithExemplarFromRequest(fn)` add exemplars to counters and histograms; if `fn` returns nil, no exemplar is added.
- Exemplars are only transmitted via OpenMetrics, so set `EnableOpenMetrics: true` in `HandlerOpts`. Side effect from the page: `quantile` and `le` label values are formatted with a trailing `.0` if they look like integers, which changes series identity on the server.
- Prometheus stores them only with `--enable-feature=exemplar-storage` (fixed-size in-memory circular buffer; size set by the `storage/exemplars` config block).

## Custom Collector (values computed at scrape time)
A `Collector` has `Describe(chan<- *Desc)` and `Collect(chan<- Metric)`. Build descriptors with `prometheus.NewDesc(fqName, help, variableLabels, constLabels)` and emit throw-away metrics from `Collect` with `prometheus.MustNewConstMetric(desc, prometheus.GaugeValue, value, labelValues...)`.
- Both methods may be called concurrently and must be concurrency safe; blocking in `Collect` slows rendering of all registered metrics.
- A collector whose `Describe` sends no descriptor is "unchecked": no registration-time checks and no re-registration check.
- For a single value computed on scrape use `prometheus.NewGaugeFunc(opts, func() float64)`; the function must be safe for concurrent calls.

## Verify
- [ ] `curl http://localhost:2112/metrics` shows your metric with `# HELP` and `# TYPE` lines (the guide's check).
- [ ] With `EnableOpenMetrics: true`, request the endpoint with an OpenMetrics `Accept` header and confirm exemplars appear on histogram bucket lines.

## Checked
Date: 2026-11-07. Read in full: the Prometheus "Instrumenting a Go application" guide, the promhttp package page on pkg.go.dev (v1.25.0 doc: handler functions, `HandlerOpts` fields, middleware docs, options) and the Prometheus feature-flags page (Exemplars storage section). The `prometheus` package page on pkg.go.dev is about 170 KB and was NOT read end to end: I searched it and read the `Collector` interface, `Registerer.Register`, `ExemplarObserver`/`ExemplarAdder`, `NewGaugeFunc`, `NewConstMetric`, `DefBuckets` and `WithLabelValues`/`GetMetricWithLabelValues` entries. Trims: removed `collectors.WithGoCollectorRuntimeMetrics` options (the `collectors` package page was not fetched), the `trace.SpanContextFromContext` OpenTelemetry snippet (not on these pages), the "< 1 s Collect" rule, the exact `duplicate metrics collector registration attempted` panic text, `testutil` helpers, pre-initialising label combinations, and the `grep`/`promtool check metrics` verify steps. Corrected: the draft used `NewGoCollector` from the `prometheus` package; the page lists those as deprecated and the guide uses `collectors`.
Method: documentation only; no commands were run.
