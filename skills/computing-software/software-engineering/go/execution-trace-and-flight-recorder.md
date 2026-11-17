---
id: computing-software.software-engineering.go.execution-trace-and-flight-recorder
name: execution-trace-and-flight-recorder
category: computing-software
field: software-engineering
product: go
tags: [go, go-benchmarks-profiling, go-flight-recorder, execution-trace, flight-recorder, runtime-trace]
level: advanced
status: docs-checked
description: "Capture Go execution traces on demand and with the Go 1.25 flight recorder to diagnose latency spikes and scheduler stalls."
sources:
  - https://go.dev/doc/diagnostics
  - https://pkg.go.dev/runtime/trace
  - https://go.dev/blog/flight-recorder
  - https://go.dev/blog/execution-traces-2024
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Execution trace and the flight recorder

**Goal:** explain a latency spike you cannot reproduce on demand.

The execution tracer collects scheduling, syscall, garbage collection and heap size events, visualised with `go tool trace`; the diagnostics page says it is for latency and utilization problems. The Go blog says tracing overhead was 10-20% CPU for many applications before Go 1.21, and is down to 1-2% for many applications since.

```go
f, _ := os.Create("trace.out")
trace.Start(f); defer trace.Stop()
ctx, task := trace.NewTask(ctx, "checkout"); defer task.End()
trace.WithRegion(ctx, "db", func() { query() })
```
```bash
go tool trace trace.out          # visualise the trace
```
`trace.Start` returns an error if tracing is already enabled.

**Flight recorder (Go 1.25, `trace.FlightRecorder`, added in go1.25.0)** keeps a moving window of trace data in memory so you can write it out only when something bad happens:

```go
fr := trace.NewFlightRecorder(trace.FlightRecorderConfig{MinAge: 5 * time.Second})
fr.Start()
if elapsed > slo { var b bytes.Buffer; fr.WriteTo(&b); save(b.Bytes()) }
```
`MinAge` is a lower bound on the age of an event in the window; the Go blog suggests about 2x the time window of the event you are debugging (10 s for a 5 s timeout). `MaxBytes` caps the buffered size but takes precedence over `MinAge` and does not guarantee memory stays below it. `WriteTo` allows one goroutine at a time and returns an error if the recorder is inactive. Only one `trace.Start` may be active at a time and currently only one flight recorder per program. Mark the Go version in your runbook: earlier releases do not have this API.

## Gotchas
- Volume: the blog says to expect a few MB of trace data per second of execution, about 10 MB/s for a busy service, so cap duration or use the flight recorder in long-running services.
- Run `go tool trace` on traces from the toolchain you are debugging; the 2024 blog notes `go tool trace` still loads the full trace into memory.

## Verify
Add a deliberate delay inside a region, take a trace, and confirm the region and the blocked goroutine appear in the viewer.

## Checked
2026-11-09. Confirmed on pkg.go.dev/runtime/trace (Start, FlightRecorder, MinAge, WriteTo, Stop), the Go 1.25 flight recorder blog, the 2024 execution traces blog and go.dev/doc/diagnostics. Removed: the claim that traces need the same major Go version, the net/http/pprof conflict, and the "tens of MB per second" figure (blog says a few to about 10 MB/s).
Method: documentation only; no commands were run.
