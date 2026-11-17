---
id: computing-software.software-engineering.go.cpu-and-heap-profiling-with-pprof
name: cpu-and-heap-profiling-with-pprof
category: computing-software
field: software-engineering
product: go
tags: [go, go-benchmarks-profiling, go-pprof, pprof, cpu-profile, heap-profile]
level: practitioner
status: docs-checked
description: "Capture and read CPU and heap profiles in Go with net/http/pprof and go tool pprof (top, web)."
sources:
  - https://go.dev/doc/diagnostics
  - https://pkg.go.dev/net/http/pprof
  - https://go.dev/blog/pprof
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CPU and heap profiling with pprof

**Goal:** find where time and allocations go before optimising.

```bash
// live service: blank-import registers handlers on http.DefaultServeMux
import _ "net/http/pprof"
go func() { log.Println(http.ListenAndServe("localhost:6060", nil)) }()
```

```bash
go tool pprof http://localhost:6060/debug/pprof/heap
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30   # 30-second CPU profile
```

Inside `go tool pprof`, `top10` lists the top samples, `top5 -cum` sorts by cumulative time, and `web` draws the call graph (`web <func>` focuses on one function). Query parameters on the handlers: `debug=N` (0 binary, >0 text), `gc=N` (heap: run a GC first), `seconds=N` (cpu and trace: duration; allocs, block, goroutine, heap, mutex, threadcreate: return a delta profile). Block and mutex profiles are off until the program calls `runtime.SetBlockProfileRate` / `runtime.SetMutexProfileFraction`. The runtime profiles are cpu, heap, threadcreate, goroutine, block and mutex. If you do not use `DefaultServeMux`, register the handlers on your own mux. Profiling data can also be collected during tests via `go test`.

## Gotchas
- Serve the profiler on a loopback or otherwise private address only, as in the package example.
- Collect one profile at a time: collections can interfere with each other, and enabling some profiles (for example CPU) costs performance, so measure the overhead before using it in production.
- To debug optimised code, `go build -gcflags=all="-N -l"` disables optimisations such as inlining.
- A profile of an idle service shows nothing useful; generate load first.

## Verify
Re-profile after a change and compare the targeted function's cumulative share in `top5 -cum`.

## Checked
2026-11-03. Confirmed against pkg.go.dev/net/http/pprof (import, handler URLs, query parameters, SetBlockProfileRate/SetMutexProfileFraction), go.dev/doc/diagnostics (profile list, one profile at a time, overhead, `-gcflags=all="-N -l"`) and go.dev/blog/pprof (`top10`, `top5 -cum`, `web`). Removed: bench/memprofile flag combos, `-sample_index`, `-diff_base`, `peek`, inuse_space/alloc_space defaults, MemProfileRate and 512 KiB, 100 Hz, `default.pgo`, `benchstat`, `-gcflags=-l` (not on the cited pages).
Method: documentation only; no commands were run.
