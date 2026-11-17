---
id: computing-software.software-engineering.go.execution-tracing-with-go-tool-trace
name: execution-tracing-with-go-tool-trace
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-tool-trace, runtime-trace, execution-tracer, flight-recorder, latency, scheduler]
level: advanced
status: verified
description: "Capture and read Go execution traces (runtime/trace, go test -trace, net/http/pprof) to find scheduler latency, blocking and GC pauses that CPU profiles miss."
sources: ["https://pkg.go.dev/runtime/trace", "https://pkg.go.dev/cmd/trace", "https://go.dev/blog/execution-traces-2024", "https://go.dev/doc/go1.25#runtimetracepkgruntimetrace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Execution tracing with go tool trace

**Goal:** explain latency that a CPU profile cannot: goroutines waiting to run, blocked on
syscalls, channels or locks, and GC stop-the-world pauses.

## When to reach for it
CPU profile shows low utilisation but requests are slow; tail latency spikes; parallel code does
not scale with cores. pprof tells you where CPU went, the trace tells you **when and why
goroutines were not running**.

## Capture
```bash
go test -trace=trace.out -run TestSlow ./pkg
curl -o trace.out 'http://localhost:6060/debug/pprof/trace?seconds=5'   # with net/http/pprof
```
In code:
```go
f, _ := os.Create("trace.out")
trace.Start(f)
defer trace.Stop()
```
Before Go 1.21 tracing cost 10-20% CPU for many programs; since 1.21 the blog reports 1-2% for many applications, so short traces in production
are reasonable (measure your own service). Keep traces short (seconds); files grow fast.

## Flight recorder (Go 1.25)
`trace.NewFlightRecorder` keeps the last few seconds of trace in memory; call `WriteTo` when
something bad happens (a slow request, a timeout) to capture the lead-up:
```go
fr := trace.NewFlightRecorder(trace.FlightRecorderConfig{MinAge: 5 * time.Second})
fr.Start()
// on anomaly:
var buf bytes.Buffer
fr.WriteTo(&buf)
```

## Annotate your own work
```go
ctx, task := trace.NewTask(ctx, "handleOrder")
defer task.End()
trace.WithRegion(ctx, "validate", func() { validate(o) })
trace.Log(ctx, "orderID", o.ID)
```
Tasks and regions appear in the "User-defined tasks/regions" views with latency histograms.

## Read
```bash
go tool trace trace.out         # opens a browser UI
go tool trace -pprof=sched trace.out > sched.pprof   # also: net, sync, syscall
go tool pprof -http=: sched.pprof
```
What to look at:
- **Goroutine analysis**: per-function breakdown of execution vs scheduler wait vs sync block vs
  syscall vs GC assist time.
- **Timeline (procs view)**: gaps on Ps mean idle CPU; long "GC" bars or STW markers.
- **Scheduler latency profile**: time runnable goroutines waited for a P - a sign of too few Ps
  (GOMAXPROCS throttling) or long non-preemptible work.
- **Synchronization blocking profile** (and the separate **Network blocking profile** and **Syscall profile** links): contended mutexes and channels.
- GC assist: goroutines forced to help the GC because allocation outpaces marking.

## Gotchas
- The trace format changed in Go 1.22; use the `go tool trace` from the same or newer Go version
  as the program that produced it.
- Very large traces make the UI slow; narrow with shorter captures or the flight recorder.
- For aggregated blocking over time, mutex and block profiles (`runtime.SetMutexProfileFraction`,
  `SetBlockProfileRate`) are cheaper than tracing.

## Verify
- [ ] The trace explains the observed latency (a specific wait category dominates).
- [ ] After the fix, the same capture shows reduced wait time for that category.

## Checked
2026-10-21 on Go 1.27.3 (Windows): `go test -trace`, `runtime/trace` Start/Stop, `NewTask`/`WithRegion`/`Log`, `trace.NewFlightRecorder(FlightRecorderConfig{MinAge})` Start/WriteTo (ran together with `trace.Start`) and an in-process `/debug/pprof/trace?seconds=1` fetch all produced traces that `go tool trace -pprof=sched|sync|net|syscall` read, and `go tool pprof -top` read the sync profile. The UI was not opened (it launches a browser); its menu labels were read from the toolchain source (`internal/trace/traceviewer/http.go`): Goroutine analysis, Network blocking profile, Synchronization blocking profile, Syscall profile, Scheduler latency profile, User-defined tasks/regions, Minimum mutator utilization. Overhead drop from 10-20% to 1-2% in Go 1.21 and the Go 1.22 format from https://go.dev/blog/execution-traces-2024.
