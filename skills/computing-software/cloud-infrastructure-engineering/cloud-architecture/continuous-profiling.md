---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.continuous-profiling
name: continuous-profiling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, continuous-profiling, flame-graphs, pyroscope, ebpf-profiling]
level: practitioner
status: draft
description: "Run continuous profiling in production: profiler choice, overhead, flame graph analysis, diffing between versions and linking profiles to traces and cost."
sources: ["https://grafana.com/docs/pyroscope/latest/", "https://cloud.google.com/profiler/docs/about-profiler", "https://www.brendangregg.com/flamegraphs.html", "https://opentelemetry.io/blog/2024/profiling/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Continuous profiling

Always-on, low-overhead sampling profilers show where CPU time, allocations and lock waits
go in production, where synthetic profiling misses real behaviour.

## Tools
Grafana Pyroscope (SDKs and eBPF agent), Parca (eBPF), Google Cloud Profiler, Amazon CodeGuru
Profiler (Java/Python), Datadog / Elastic profilers; OpenTelemetry profiling signal is emerging.

## Steps
1. **Deploy** an eBPF agent per node for compiled languages (whole-system, no code change)
   or language SDKs for runtime-aware stacks (JVM, Go pprof, Python, .NET). Typical overhead
   about 1-2% CPU at default sampling (around 100 Hz).
2. **Label** profiles with service, version, region, endpoint where supported.
3. **Read flame graphs**: width = share of samples; look for wide plateaus; ignore colour.
   Check CPU, allocation (memory churn drives GC), lock contention and wall-clock profiles.
4. **Diff** profiles between versions or time ranges to explain regressions after deploys.
5. **Link to traces** (span profiles) to see why a specific slow request spent its time.
6. **Cost work**: rank functions by fleet-wide CPU; optimising the top few often lets you
   shrink instance counts.

## Gotchas
- Missing symbols (stripped binaries, JIT frames without perf maps) produce unreadable stacks; ship debug info or symbol servers.
- Profiling only one replica misses behaviour that depends on traffic mix.

## Verify
- [ ] Profiles available for every production service with version labels.
- [ ] At least one optimisation tracked from profile to cost saving.
