---
id: computing-software.software-engineering.go.runtime-metrics-and-memstats
name: runtime-metrics-and-memstats
category: computing-software
field: software-engineering
product: go
tags: [go, go-runtime-gc, go-runtime-metrics, runtime-metrics, memstats]
level: practitioner
status: docs-checked
description: "Export Go runtime health with runtime/metrics (GC, heap, scheduler latency) and know how it differs from ReadMemStats."
sources:
  - https://pkg.go.dev/runtime/metrics
  - https://pkg.go.dev/runtime#MemStats
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# runtime/metrics and MemStats

**Goal:** a cheap, stable view of GC and scheduler behaviour for dashboards and alerts.

```go
samples := []metrics.Sample{
    {Name: "/gc/heap/live:bytes"},
    {Name: "/memory/classes/total:bytes"},
    {Name: "/sched/goroutines:goroutines"},
    {Name: "/sched/latencies:seconds"}, // histogram
}
metrics.Read(samples)
for _, s := range samples {
    switch s.Value.Kind() {
    case metrics.KindUint64: fmt.Println(s.Name, s.Value.Uint64())
    case metrics.KindFloat64Histogram: h := s.Value.Float64Histogram(); _ = h
    }
}
```

`metrics.All()` returns the descriptions of every supported metric (name, kind, description); the package docs encourage sampling the metrics from `All` to stay compatible across Go versions. A metric key is `path:unit`, and a metric's kind is guaranteed not to change (a changed kind gets a new key). Metrics may rarely be deprecated and removed. Read values by kind: `Value.Uint64()` panics unless the kind is `KindUint64` (likewise for the histogram accessor), so switch on `Kind()` as above.

Useful signals (each documented in the package): `/gc/heap/live:bytes` (heap occupied by live objects marked by the last GC), `/gc/cycles/total:gc-cycles`, `/memory/classes/total:bytes`, `/sched/goroutines:goroutines` (count of live goroutines), `/sched/latencies:seconds` (distribution of time goroutines spent runnable before running) and `/sync/mutex/wait/total:seconds`.

## Gotchas
- `runtime.ReadMemStats` fills a `MemStats` struct and is up to date as of the call, unlike a heap profile (a snapshot as of the last completed GC). The `runtime/metrics` package is described as the more general, stable interface.
- `MemStats.Sys` is the total bytes of memory obtained from the OS, not resident set size.

## Checked
2026-11-09. Confirmed on pkg.go.dev/runtime/metrics: the metric names listed above, `Read`, `All`, `Sample`, value kinds, key format, kind stability and the Uint64 panic on a wrong kind. Confirmed on pkg.go.dev/runtime#MemStats: `ReadMemStats` and `Sys`. Removed claims not on those pages: `ReadMemStats` stops the world, Prometheus/OpenTelemetry exporters, `GOMEMLIMIT` comparison, p99 starvation reading and the goroutine-leak signature.
Method: documentation only; no commands were run.

## Verify
Read the samples under load and confirm the values are sensible for your service (for example `/gc/heap/live:bytes` changing across GC cycles).
