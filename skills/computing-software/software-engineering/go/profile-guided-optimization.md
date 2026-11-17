---
id: computing-software.software-engineering.go.profile-guided-optimization
name: profile-guided-optimization
category: computing-software
field: software-engineering
product: go
tags: [go, go-tooling, go-build, pgo, profile-guided-optimization, pprof, performance]
level: practitioner
status: verified
description: "Use Go profile-guided optimization: collect representative CPU profiles, commit default.pgo, measure gains, refresh profiles and avoid common PGO mistakes."
sources:
  - https://go.dev/doc/pgo
  - https://go.dev/blog/pgo
  - https://pkg.go.dev/net/http/pprof
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profile-guided optimization (PGO) in Go

**Goal:** a free 2-14% CPU improvement for hot services by letting the compiler optimise using real production profiles.

## 1. How it works
With a CPU profile, the compiler (Go 1.21+) inlines hot call sites more aggressively and devirtualises hot interface calls (https://go.dev/blog/pgo). It only uses the profile as a hint: builds stay correct with stale profiles.

## 2. Collect a representative profile
From production (best) via `net/http/pprof`:
```go
import _ "net/http/pprof"     // registers /debug/pprof on DefaultServeMux; serve on an internal port only
go func() { log.Println(http.ListenAndServe("localhost:6060", nil)) }()
```
```bash
curl -o cpu1.pprof "http://localhost:6060/debug/pprof/profile?seconds=30"
# collect from several instances/times, then merge
go tool pprof -proto cpu1.pprof cpu2.pprof cpu3.pprof > default.pgo
```
Continuous profiling services can supply merged pprof profiles (the pgo doc names fleet-wide profiles as a source). Benchmarks are a weak substitute: they optimise for the benchmark, not production.

## 3. Build with it
Place `default.pgo` in the **main package** directory (`cmd/app/default.pgo`); `go build` uses it automatically (`-pgo=auto`). Explicit: `go build -pgo=/path/profile.pgo`; disable with `-pgo=off`.
```bash
go version -m ./app | grep pgo      # -pgo=.../default.pgo in build settings
```

## 4. Measure
Compare CPU per request (or throughput at fixed CPU) before and after, under the same load:
```bash
go test -bench=. -count=10 -pgo=off > old.txt
go test -bench=. -count=10 -pgo=auto > new.txt
benchstat old.txt new.txt
```
Better: A/B in production by canary, comparing CPU utilisation per RPS.

## 5. Maintenance
- Refresh the profile periodically (e.g. each release) from the current production build; the iterative workflow (profile built with PGO) is supported and stable.
- Commit the profile to the repo so builds are reproducible.
- Build time increases modestly; binary size slightly.

## Gotchas
- Profiles from a test or staging environment with different traffic shapes give little benefit.
- Exposing `/debug/pprof` publicly leaks internals and enables DoS; bind to localhost or protect it.
- PGO does not help I/O-bound services where CPU is not the bottleneck; check with the profile first.
- Large refactors make old profiles less effective (functions renamed), never incorrect.

## Verify
- `go version -m` shows the pgo setting for release binaries, and benchstat/canary metrics show a statistically significant CPU reduction.

## Checked
2026-10-21 on Go 1.27.3 (Windows): a scratch program with a hot interface call was profiled twice with `runtime/pprof`, merged with `go tool pprof -proto a b > cmd/app/default.pgo`, and built: `go version -m` showed `build -pgo=.../default.pgo` automatically (`-pgo=auto`), nothing with `-pgo=off`, and the same with an explicit `-pgo=path`; runtime fell from about 2.34 s to 2.13 s (one run each, about 9%); `go test -bench -pgo=off|auto` accepted the flag (11.7 vs 10.1 µs/op, single run). The 2-14% figure, default.pgo placement, -pgo=auto default (before 1.21 the default is off), merge command, build-time and binary-size notes, and the iterative workflow come from https://go.dev/doc/pgo; inlining plus devirtualization from https://go.dev/blog/pgo. Vendor profilers and code-layout effects were not verified and were removed.
