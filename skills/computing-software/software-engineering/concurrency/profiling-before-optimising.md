---
id: computing-software.software-engineering.concurrency.profiling-before-optimising
name: profiling-before-optimising
category: computing-software
field: software-engineering
product: concurrency
tags: [profiling, performance, optimisation, optimization, flame-graphs, perf, linux-perf, py-spy, pprof, async-profiler, jfr, java-flight-recorder, sampling-profiler, off-cpu, benchmarking, jmh, pytest-benchmark, hyperfine, criterion, lock-contention, amdahls-law, latency-percentiles, coordinated-omission, concurrency, software-engineering]
level: advanced
status: draft
description: "Find where time actually goes before changing code: define the metric, sample with perf/py-spy/pprof/async-profiler, read flame graphs, benchmark correctly, spot lock contention, apply Amdahl."
sources: ["Gregg, Systems Performance (2nd ed.)", "Brendan Gregg - Flame Graphs (brendangregg.com)", "Go documentation - Diagnostics and runtime/pprof", "async-profiler project README", "OpenJDK JMH samples"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profiling before optimising — measure, then change the right thing

**Goal:** make a program measurably faster (or cheaper) by finding the dominant cost
with evidence, changing that, and proving the improvement under realistic load.

## 1. Define the target before touching code
- Pick one metric: p99 latency of endpoint X, throughput at fixed CPU, job wall time,
  memory peak. Report percentiles (p50/p95/p99), never just the mean.
- Establish a baseline on production-like hardware, data size and concurrency, and
  a stopping condition ("p99 under 200 ms at 500 rps").
- Classify the bottleneck first with cheap tools: `top`/`htop` (CPU-bound if a core is
  at ~100%), `vmstat 1` (run queue, swap), `iostat -x 1`, `pidstat -t 1` per thread.
  Low CPU but slow means waiting — on I/O, locks, network or a downstream service.

## 2. Profile with a sampling profiler
Sampling (typically ~100 Hz per thread or more) is low-overhead and safe-ish in
production; instrumenting profilers distort short functions.
- **Linux, any native/JIT code:** `perf record -F 99 -g -p <pid> -- sleep 30`, then
  `perf report` or generate a flame graph (`perf script | stackcollapse-perf.pl |
  flamegraph.pl > cpu.svg`). Build with frame pointers
  (`-fno-omit-frame-pointer`) or use `--call-graph dwarf` for usable stacks.
- **Python:** `py-spy record -o profile.svg --pid <pid>` (add `--native` for C
  extensions, `--idle` to include waiting threads); `py-spy top` for a live view.
  `cProfile` + snakeviz for deterministic call counts in dev.
- **Go:** `import _ "net/http/pprof"`, then
  `go tool pprof -http=:8081 http://localhost:6060/debug/pprof/profile?seconds=30`;
  also `/debug/pprof/heap`, `/mutex` and `/block` (enable with
  `runtime.SetMutexProfileFraction` / `SetBlockProfileRate`).
- **JVM:** `asprof -d 30 -e cpu -f cpu.html <pid>` (async-profiler; older releases use
  `profiler.sh`), `-e alloc` for allocations, `-e lock` for contention, `-e wall` for
  wall-clock. JFR: `jcmd <pid> JFR.start duration=60s filename=rec.jfr`, view in JDK
  Mission Control.
- **Node:** `node --cpu-prof`; **.NET:** `dotnet-trace collect -p <pid>`.

## 3. Read the flame graph
- X-axis is the share of samples (not time order); width = cost. Y-axis is stack depth.
- Look for **wide plateaus** — frames that are wide at the top have self time and are
  your hotspots. Tall, thin towers are cheap however deep.
- Compare before/after with differential flame graphs (`difffolded.pl`) or
  `pprof -diff_base old.pb.gz new.pb.gz`.
- **On-CPU profiles miss waiting.** If the service is slow but CPU is low, use
  off-CPU/wall-clock profiles (`asprof -e wall`, `py-spy --idle`, `offcputime` from
  bcc/bpftrace) or distributed traces.

## 4. Concurrency: contention and Amdahl
- Lock contention shows as threads blocked on monitors/mutexes: async-profiler `-e lock`,
  Go `/debug/pprof/mutex`, `jstack` dumps showing many `BLOCKED` threads on one lock,
  `perf lock` or `bpftrace` on futex waits for native code.
- Fixes in order of preference: shorten the critical section (no I/O under lock),
  shard the lock or data (striped locks, per-core counters), use read-write locks for
  read-heavy data, move to lock-free/immutable snapshots, or remove sharing entirely.
- **Amdahl's law:** speedup = 1 / ((1 − p) + p/n). With 90% parallelisable work,
  even infinite cores give at most 10×; 16 cores give ~6.4×. Measure the serial
  fraction before buying more threads or machines.
- More threads than cores on CPU-bound work adds context-switch overhead; size pools
  from measurement (for blocking I/O, Little's law: concurrency = throughput × latency).

## 5. Benchmark without fooling yourself
- Use a harness: JMH (Java), `pytest-benchmark`/`pyperf` (Python), `go test -bench .
  -benchmem -count 10` + `benchstat`, Criterion (Rust), BenchmarkDotNet (.NET),
  `hyperfine --warmup 3 'cmd-a' 'cmd-b'` for whole commands.
- Warm up JITs and caches; report distribution and confidence, not a single run.
- Prevent dead-code elimination (JMH `Blackhole`, Go `b.Loop()`/sink variables,
  `std::hint::black_box`).
- Keep conditions identical (CPU frequency/turbo, no noisy neighbours, mains power).
- Load tests: use open-model (constant arrival rate) generators such as `wrk2`, k6
  `constant-arrival-rate` or Gatling; closed-loop tools suffer **coordinated
  omission** and under-report tail latency.

## 6. Change one thing, re-measure, keep the evidence
Optimise the widest frame, re-profile, and stop when the target is met. Usual big wins,
in order: algorithmic complexity and N+1 queries, avoiding repeated work (caching,
batching), allocation reduction, data layout — micro-tuning last.

## Gotchas
- Profiling a debug build or tiny dataset optimises the wrong thing.
- JIT inlining and missing symbols produce misleading stacks; for the JVM use
  async-profiler (handles inlined frames) rather than safepoint-biased samplers.
- Container CPU limits (CFS quota) cause throttling stalls that look like random
  latency; check `nr_throttled` in the cgroup's `cpu.stat`.
- Mean latency hides tail regressions; GC pauses live in p99.9.

## Verify
- [ ] A baseline metric and target existed before any code changed.
- [ ] The change targets a frame that was demonstrably wide in a profile of a realistic workload.
- [ ] Off-CPU / lock profiles were checked when CPU was not saturated.
- [ ] Benchmarks used warm-up, multiple runs and a statistical comparison.
- [ ] Before/after numbers (with percentiles) are recorded in the PR.

Related: computing-software.software-engineering.debugging.systematic-debugging
