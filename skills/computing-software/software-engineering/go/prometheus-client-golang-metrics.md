---
id: computing-software.software-engineering.go.prometheus-client-golang-metrics
name: prometheus-client-golang-metrics
category: computing-software
field: software-engineering
product: go
tags: [go, go-logging-observability, go-prometheus, prometheus, metrics, histogram]
level: practitioner
status: docs-checked
description: "Expose Go application metrics with prometheus/client_golang: counters, histograms, labels, promhttp and promauto, avoiding cardinality blow-ups."
sources:
  - https://pkg.go.dev/github.com/prometheus/client_golang/prometheus
  - https://prometheus.io/docs/practices/naming/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus client_golang metrics

**Goal:** RED metrics (rate, errors, duration) for each handler, cheap to scrape.

```go
var (
    reqs = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "http_requests_total", Help: "Requests by method, route and status.",
    }, []string{"method", "route", "code"})
    lat = promauto.NewHistogramVec(prometheus.HistogramOpts{
        Name: "http_request_duration_seconds", Help: "Latency.",
        Buckets: prometheus.ExponentialBuckets(0.005, 2, 12), // 5ms..10s
    }, []string{"route"})
)

func instrument(route string, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        sw := &statusWriter{ResponseWriter: w, code: 200}
        next.ServeHTTP(sw, r)
        lat.WithLabelValues(route).Observe(time.Since(start).Seconds())
        reqs.WithLabelValues(r.Method, route, strconv.Itoa(sw.code)).Inc()
    })
}
mux.Handle("/metrics", promhttp.Handler())
```

`statusWriter` is your own `http.ResponseWriter` wrapper that records the status code. Use a bounded route name or pattern as the label, never the raw path. `promauto` constructors register with `prometheus.DefaultRegisterer` and panic if registration fails. The default registry comes with a Go runtime collector (`NewGoCollector`) and a process collector (`NewProcessCollector`); a custom registry (`NewRegistry`) does not unless you register them. Naming: counters end in `_total` and metrics use base units (seconds, bytes).

## Gotchas
- Keep label values bounded; every distinct label combination is a separate time series.
- `prometheus.DefBuckets` (`.005` to `10` seconds) are tailored to broadly measure network-service response time; define buckets for your use case, as `ExponentialBuckets` does here (it panics if `count` <= 0, `start` <= 0 or `factor` <= 1).
- Create `promauto` metrics once at package or startup level, since a failed registration panics.

## Verify
Scrape `/metrics` and confirm `http_request_duration_seconds_bucket` series appear.

## Checked
2026-11-03. Confirmed on pkg.go.dev for prometheus (CounterVec.WithLabelValues, DefBuckets, ExponentialBuckets, DefaultRegisterer with Go and process collectors), promauto (NewCounterVec, NewHistogramVec, panic on failed registration) and promhttp (`Handler`), and prometheus.io naming practices (`_total`, base units). Removed: `r.Pattern`/Go 1.23 claim, OOM statement, `WithLabelValues` panic and caching advice, internal-port advice, `curl`/`promtool` steps.
Method: documentation only; no commands were run.
