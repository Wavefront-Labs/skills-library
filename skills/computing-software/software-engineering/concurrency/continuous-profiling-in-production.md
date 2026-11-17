---
id: computing-software.software-engineering.concurrency.continuous-profiling-in-production
name: continuous-profiling-in-production
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, continuous-profiling, pyroscope, parca, ebpf-profiling, flame-graphs, pprof]
level: advanced
status: draft
description: "Run continuous profiling in production with Pyroscope, Parca or cloud profilers: eBPF vs in-process agents, overhead, labels, and comparing flame graphs across versions."
sources: ["https://grafana.com/docs/pyroscope/latest/", "https://www.parca.dev/docs/overview", "https://cloud.google.com/profiler/docs/about-profiler", "https://github.com/google/pprof"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Continuous profiling in production

Always-on, low-overhead sampling profiles from every instance, stored over time. Answers "what was
the CPU doing during last night's spike?" and "which function got slower in v2.3?" without
reproducing locally.

## Options
| Tool | How |
|---|---|
| **Grafana Pyroscope** | SDK push (Go, Java via async-profiler, Python, Ruby, .NET, Node, Rust) or Grafana Alloy eBPF collection; stores in Pyroscope/Grafana Cloud |
| **Parca** | Parca Agent uses eBPF to profile all processes on a node (no code changes), symbolises via debuginfod; Parca server stores pprof |
| Google Cloud Profiler, Datadog Continuous Profiler, AWS CodeGuru Profiler, Elastic Universal Profiling | vendor agents |
| OpenTelemetry profiles signal | emerging standard; eBPF profiler donated by Elastic |

## eBPF vs in-process
- **eBPF (whole-node)**: no app changes, all languages, CPU profiles mainly. Needs frame pointers
  or unwinding info (DWARF/`.eh_frame`) and symbols; interpreted languages need specific support
  (Python, Node, JVM unwinders exist in Parca/Elastic agents).
- **In-process SDK**: richer profile types (allocations, heap, lock contention, goroutines, wall
  time), per-request labels (endpoint, tenant), but per-language setup.

## Setup notes
- Overhead target ~1-2% CPU; sample at ~100 Hz (default in most).
- Tag profiles with `service`, `version`, `region`, `pod` so you can diff versions.
- Go: `pyroscope.Start(...)` or expose `net/http/pprof` and scrape; JVM: async-profiler agent
  (`-agentpath:...libasyncProfiler.so=start,event=cpu,...`); compile native code with
  `-fno-omit-frame-pointer` for good eBPF stacks.
- Protect profile endpoints (`/debug/pprof`) from public access.

## Using it
- **Diff flame graphs**: baseline (last week / previous version) vs now; red = more samples.
- Filter by label to see one endpoint's CPU.
- Correlate with traces (span profiles: Pyroscope links profile samples to trace spans).
- Look at self time (wide plateaus at the top) for hot functions; wide towers from one caller for
  wasteful call paths (serialization, logging, regex compilation, allocations).
