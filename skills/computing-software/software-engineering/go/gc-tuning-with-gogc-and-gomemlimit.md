---
id: computing-software.software-engineering.go.gc-tuning-with-gogc-and-gomemlimit
name: gc-tuning-with-gogc-and-gomemlimit
category: computing-software
field: software-engineering
product: go
tags: [go, golang, gomemlimit, gogc, garbage-collector, gctrace, containers, memory-tuning, gomaxprocs, go-runtime-gc, go-gomemlimit, go-gomaxprocs]
level: advanced
status: gated
description: "Tune the Go garbage collector with GOGC and GOMEMLIMIT for containers, read gctrace output, and avoid OOM kills and GC death spirals."
sources: ["https://go.dev/doc/gc-guide", "https://pkg.go.dev/runtime/debug#SetMemoryLimit", "https://pkg.go.dev/runtime#hdr-Environment_Variables", "https://go.dev/doc/go1.25#container-aware-gomaxprocs"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GC tuning with GOGC and GOMEMLIMIT

**Goal:** trade memory for CPU deliberately, and keep a Go service inside its container memory
limit without OOM kills.

## The two knobs
- **GOGC** (default 100): the next GC triggers when the live heap has grown by GOGC% since the
  last mark. GOGC=200 halves GC frequency and roughly doubles peak heap overhead; GOGC=50 does the
  opposite. `GOGC=off` disables proportional GC (only sensible together with GOMEMLIMIT).
- **GOMEMLIMIT** (Go 1.19+): a soft limit on total Go-runtime memory (heap, stacks, runtime
  metadata, not cgo or mmapped files). As usage nears it, the GC runs more often regardless of GOGC.
  Units: `GOMEMLIMIT=900MiB` (suffixes are B, KiB, MiB, GiB, TiB; `900MB` or `1G` abort the program at start). Runtime: `debug.SetMemoryLimit(n)`, `debug.SetGCPercent(n)`.

## Container recipe
```yaml
resources: { limits: { memory: 1Gi, cpu: "2" } }
env:
  - { name: GOMEMLIMIT, value: "900MiB" }   # ~90% of the limit, leave room for non-Go memory
```
- Optional higher-throughput variant: `GOGC=off` + GOMEMLIMIT - the heap grows freely until the
  limit then GC kicks in. Only for services whose live heap is well below the limit; otherwise it
  degrades into constant GC.
- The limit is soft: if the live heap genuinely exceeds it, the runtime caps GC CPU at about 50%
  to avoid a total death spiral and lets memory grow, and a container's OOM killer then acts (gated: unconfirmed, source is paywalled or blocked). GOMEMLIMIT=
  does not fix leaks.
- Libraries such as `github.com/KimMachineGun/automemlimit` set GOMEMLIMIT from the cgroup limit.
- CPU: Go 1.25 makes GOMAXPROCS container-aware (respects the cgroup CPU limit) when the go.mod
  `go` line is 1.25+, and `GODEBUG=containermaxprocs=0` or setting GOMAXPROCS turns it off (gated: unconfirmed, source is paywalled or blocked). On older versions use `go.uber.org/automaxprocs`, otherwise GOMAXPROCS equals
  the host core count and the container gets CPU-throttled.

## Observe before tuning
```bash
GODEBUG=gctrace=1 ./app 2>&1 | head
# gc 42 @12.3s 2%: 0.02+3.1+0.03 ms clock, ... 180->182->95 MB, 190 MB goal, ... 8 P
```
Fields: GC number, time since start, % CPU in GC so far, phase wall times, heap at start ->
end -> live, next goal. A high % (above 10-25%) with a stable live heap means GOGC/limit headroom
is too tight.
- `runtime/metrics`: `/gc/cycles/total:gc-cycles`, `/memory/classes/heap/objects:bytes`,
  `/gc/heap/goal:bytes`, `/cpu/classes/gc/total:cpu-seconds`. Prometheus `client_golang` exports
  many as `go_gc_*`, `go_memstats_*`.
- Heap profile (`pprof -sample_index=alloc_space`) to cut allocation rate; reducing allocations
  beats any tuning.

## Gotchas
- Setting GOMEMLIMIT to 100% of the container limit leaves no room for goroutine stacks spikes,
  cgo, or page cache accounting; aim for 80-90%.
- `debug.FreeOSMemory` and `GODEBUG=madvdontneed=1` change RSS reporting, not live heap.
- Ballast arrays (pre-1.19 trick) are obsolete; use GOMEMLIMIT.

## Verify
- [ ] Under peak load, RSS stays below the container limit with no OOMKilled restarts.
- [ ] GC CPU fraction from metrics is acceptable (typically under 10%).
- [ ] GOMAXPROCS matches the CPU limit (log `runtime.GOMAXPROCS(0)` at startup).

## Checked
2026-10-21 on Go 1.27.3 (Windows): a scratch program with 50 MiB live heap and 200 MB of churn ran 4 GCs at GOGC=100, 2 at GOGC=200, 8 at GOGC=50, 0 at GOGC=off; `GOGC=off GOMEMLIMIT=200MiB` ran 1 GC, and a 40MiB limit below the live heap ran about 395 GCs with the program still finishing; `GOMEMLIMIT=900MiB` was accepted while `900MB` and `1G` died with `fatal error: malformed GOMEMLIMIT`; `GODEBUG=gctrace=1` printed the documented fields; the four `runtime/metrics` names all read as valid samples; `debug.SetMemoryLimit` docs (`go doc`) say cgo/C memory and Mmap are excluded; the 50% GC CPU cap is from https://go.dev/doc/gc-guide; container-aware GOMAXPROCS and `containermaxprocs` from https://go.dev/doc/go1.25 and https://go.dev/doc/godebug; automemlimit and automaxprocs resolve on the module proxy. Not run: a real cgroup/Kubernetes memory or CPU limit, the OOM killer and cgroup GOMAXPROCS (no Linux host).
