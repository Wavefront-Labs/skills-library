---
id: computing-software.qa-testing-engineering.performance-testing.apm-tracing-and-profiling-root-cause
name: apm-tracing-and-profiling-root-cause
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [apm, distributed-tracing, opentelemetry, jaeger, datadog, new-relic, flame-graph, profiling, cpu-profiling, py-spy, async-profiler, perf, n-plus-one, lock-contention, gc-pause, root-cause-analysis, span, trace-waterfall]
level: advanced
status: draft
description: "Use distributed tracing and CPU/allocation profiling to find exactly which function, query, or lock is the bottleneck a load test exposed, instead of guessing from aggregate metrics."
sources: ["https://opentelemetry.io/docs/concepts/signals/traces/", "https://www.brendangregg.com/flamegraphs.html", "https://github.com/benfred/py-spy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# From "p95 is too high" to the exact line: tracing and profiling

**Goal:** a load test tells you *that* the system is slow under load; it does not
tell you *where*. This skill closes that gap using distributed tracing for
cross-service latency and profiling for in-process CPU/lock time.

## 1. Distributed tracing — which hop is slow
A single user request fans out across services; aggregate latency hides which hop
grew. Instrument with OpenTelemetry (vendor-neutral SDK, exports to Jaeger,
Datadog, New Relic, Grafana Tempo, etc.) so every request carries a trace ID
through all services, and inspect the **trace waterfall**: each span's start/end
relative to its parent. Look for:
- One span growing disproportionately under load while siblings stay flat →
  that service/call is the bottleneck, not the aggregate "slow API."
- Large **gaps between spans with no child span** → time spent in application code
  that isn't instrumented (add a span) or queued waiting for a resource (thread
  pool, connection pool) rather than doing work.
- Sequential spans that could be parallel (N sequential DB calls instead of one
  batched call) — visible instantly in a waterfall, invisible in a single latency
  number.

## 2. The classic N+1 signature
A trace showing one query span followed by dozens-to-hundreds of near-identical
child query spans, each fast individually, but summing to the real latency, is an
N+1 query pattern (ORM lazy-loading a relation per row). The fix is almost always
eager loading / batching, not a faster database — recognize the *shape* in the
trace before reaching for an index.

## 3. CPU and allocation profiling — which function
When the bottleneck is inside one process rather than between services, attach a
profiler and read a **flame graph**: width = time spent (including children),
stacking = call hierarchy. Wide plateaus near the top of the stack are where time
is actually spent, not deep narrow towers.
- Python: `py-spy record -o profile.svg --pid <pid>` (sampling, safe on
  production — no code changes, no restart).
- JVM: `async-profiler` or built-in JFR (Java Flight Recorder).
- Linux, language-agnostic: `perf record`/`perf script` + `FlameGraph` scripts.
Allocation profiles (not just CPU) catch GC-pressure bottlenecks that look like
"CPU is fine but latency spikes periodically" — a sawtooth in response time
correlated with GC logs is the signature; fix allocation rate, not CPU.

## 4. Lock contention and thread-pool saturation
A thread stuck in `WAITING`/`BLOCKED` state (visible in a JVM thread dump,
Python's GIL contention, or a connection-pool wait span) under load but fine at
low concurrency is contention, not raw compute cost — more CPU won't fix it; the
fix is a smaller critical section, a different lock granularity, or more pool
capacity sized to the arrival rate (see `jmeter-k6.results-analysis-and-ci-gating`
for measuring the arrival rate correctly first).

## 5. Correlate, don't guess
Run the profiler/tracer *during* the load test that exposed the problem, not
afterward in isolation — a bottleneck that only appears at concurrency 200 may be
invisible when profiled at concurrency 1. Capture the trace/profile sample at the
same moment the load tool reports the p99 spike (shared timestamps, or trigger the
profile from the load test's ramp schedule).

## Unconfirmed / notes
Tool specifics (exact flags, vendor UI) drift fast; the waterfall-reading and
flame-graph-reading skills are the durable part. Not independently verified
against a live production incident here.

## Verify
- [ ] Trace waterfall inspected for the growing span, not just end-to-end latency.
- [ ] N+1 pattern checked for (repeated near-identical child spans) before indexing.
- [ ] A flame graph taken under the same load that produced the reported regression.
- [ ] GC/allocation profile checked if latency is periodic rather than steady.
- [ ] Thread/connection-pool wait time distinguished from raw CPU-bound time.
