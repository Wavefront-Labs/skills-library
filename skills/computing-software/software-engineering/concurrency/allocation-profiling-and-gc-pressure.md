---
id: computing-software.software-engineering.concurrency.allocation-profiling-and-gc-pressure
name: allocation-profiling-and-gc-pressure
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, profiling, performance, allocation-profiling, gc-pressure, async-profiler-alloc, pprof-allocs, memorydiagnoser, escape-analysis, allocation-rate]
level: advanced
status: draft
description: "Find and cut hot-path allocations that drive GC pauses and CPU: allocation profilers for JVM, Go, .NET, Node and Python, reading the results, and common fixes."
sources: ["https://github.com/async-profiler/async-profiler/blob/master/docs/ProfilingModes.md", "https://go.dev/doc/gc-guide", "https://pkg.go.dev/runtime/pprof", "https://benchmarkdotnet.org/articles/configs/diagnosers.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Allocation profiling and GC pressure

**Goal:** when GC time or allocation rate is high, find the code that allocates most
and reduce it, rather than tuning GC flags blindly.

## Is allocation the problem?
Signals: GC CPU > ~5-10%, frequent young-gen collections, p99 latency spikes aligned
with GC pauses, high allocation rate (MB/s) in runtime metrics (JFR, `GODEBUG=gctrace=1`,
`dotnet-counters` "Allocation Rate", Node `--trace-gc`).

## Allocation profilers
| Runtime | Tool |
|---|---|
| JVM | `asprof -e alloc -d 30 -f alloc.html <pid>` (async-profiler flame graph by allocated bytes); JFR `ObjectAllocationSample` events in JMC |
| Go | `go tool pprof -sample_index=alloc_space http://host/debug/pprof/allocs`; `go test -bench . -benchmem -memprofile mem.out`; `go build -gcflags=-m` shows escape analysis decisions |
| .NET | BenchmarkDotNet `[MemoryDiagnoser]` (bytes/op); `dotnet-trace collect --profile gc-verbose`; PerfView allocation stacks |
| Node | DevTools Memory "Allocation sampling"; `--heap-prof` |
| Python | `tracemalloc` snapshots grouped by line; `memray run` (native too) |
Profile under realistic load; look at the widest flame-graph frames by BYTES, not counts.

## Common hot-path fixes
- Reuse buffers: `sync.Pool` (Go), `ArrayPool<T>` (.NET), thread-local or pooled
  `StringBuilder`/`ByteBuffer`; reset before reuse.
- Avoid boxing: primitive collections (fastutil, Eclipse Collections), generic
  specialisation, `Span<T>`/value types.
- Pre-size collections (`make([]T, 0, n)`, `new ArrayList<>(n)`).
- Avoid intermediate strings: format into a buffer; log with lazy parameters
  (`log.debug("x={}", x)` not string concatenation).
- Stream instead of materialising whole payloads; parse JSON with streaming APIs.
- Go: keep values on the stack (avoid taking addresses that escape, interface
  conversions in hot loops); check with `-gcflags=-m`.
- Caching computed results (but bounded).

## Then tune GC if still needed
Go: `GOGC`/`GOMEMLIMIT`; JVM: heap size and collector (see jvm-garbage-collection-tuning);
.NET: server vs workstation GC, `GCConserveMemory`. Reducing allocation usually beats tuning.

## Verify
- [ ] Benchmark shows lower bytes/op and allocation rate; GC CPU and p99 improved under load.
- [ ] Pooled objects are reset; no data leaks between uses (tests).
