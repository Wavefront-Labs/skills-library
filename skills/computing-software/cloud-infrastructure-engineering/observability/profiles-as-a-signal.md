---
id: computing-software.cloud-infrastructure-engineering.observability.profiles-as-a-signal
name: profiles-as-a-signal
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [profiles-signal, when-to-profile, continuous-profiling, telemetry-signals, signal-selection]
level: practitioner
status: draft
description: "Decide when to add continuous profiling as a fourth signal: CPU/memory hotspots, cost reduction, latency inside a span. Covers overhead, profile types, and linking to traces."
sources: ["https://opentelemetry.io/blog/2024/profiling/", "https://grafana.com/docs/pyroscope/latest/introduction/", "https://grafana.com/docs/pyroscope/latest/configure-client/trace-span-profiles/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profiles as a fourth signal

Continuous profiling samples stack traces in production (typically ~100 Hz CPU sampling, allocation sampling)
and aggregates them into flame graphs per service/version over time. OTel added profiles as a signal
(OTLP profiles, development status as of 2025-2026); Pyroscope, Parca and vendor profilers are the main backends.

## Add profiles when
- Metrics show high CPU or memory but you cannot tell which code: profiles name the function.
- A span is slow but has no child spans: the time is inside the process (CPU, lock contention, GC).
- You want to cut compute cost: top-N functions by CPU across the fleet are the cheapest wins.
- Regressions between versions: diff flame graphs `service_version=v1` vs `v2`.
- Memory leaks: inuse_space over time per allocation site.

## Skip or defer when
Basic RED metrics and tracing are not yet in place - profiles answer "why is this code slow", not "which service
is broken".

## Profile types
CPU (`process_cpu`), wall clock, alloc objects/space, inuse objects/space, goroutines, mutex/block contention
(Go), lock (Java via async-profiler). Pick CPU + memory first.

## Overhead
Sampling profilers cost ~1-5% CPU. eBPF profilers (Alloy `pyroscope.ebpf`, Parca agent) need no code change and
work for compiled languages; interpreted languages need SDK or language-specific support for readable symbols.

## Linking to traces
Span profiles: the SDK tags samples with the active span ID (`pyroscope.profile.id` on the span), so Grafana
shows "Profiles for this span". Requires the Pyroscope SDK + OTel integration (Go, Java, Ruby, .NET, Python).

## Verify
Flame graph for a service shows symbolised function names (not hex addresses) and total CPU roughly matches
`rate(process_cpu_seconds_total[5m])`.
