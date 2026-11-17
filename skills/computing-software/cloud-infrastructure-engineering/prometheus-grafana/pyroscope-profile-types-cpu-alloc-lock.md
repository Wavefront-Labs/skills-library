---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.pyroscope-profile-types-cpu-alloc-lock
name: pyroscope-profile-types-cpu-alloc-lock
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [pyroscope, profile-types, alloc-profile, cpu-profile, continuous-profiling, flame-graph]
level: practitioner
status: docs-checked
description: "Choose continuous profiling types in Pyroscope (CPU, alloc, inuse, goroutines, mutex, block, lock, wall) per language and instrumentation method."
sources: ["https://grafana.com/docs/pyroscope/latest/view-and-analyze-profile-data/profiling-types/", "https://grafana.com/docs/pyroscope/latest/configure-client/", "https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/go_push/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pyroscope profile types

**Goal:** pick the right profile type for the question, and know which instrumentation method can supply it.

## Types Pyroscope supports
- CPU (CPU time, wall time)
- Memory: allocation objects, allocation space, heap
- In-use objects and in-use space
- Goroutines
- Mutex count and duration
- Block count and duration
- Lock count and duration
- Exceptions

Typical questions: CPU = where is CPU spent; alloc objects/space = what allocates the most; inuse = what holds memory now; mutex/lock = contention; block = time waiting on blocking operations.

## Auto-instrumentation with Grafana Alloy
- Alloy supports eBPF, Java and Go (pull mode). New installs should use Alloy, not the deprecated Grafana Agent.
- The eBPF profiler collects CPU profiles only. Natively compiled languages (C/C++, Go, Rust, Zig) are supported without frame pointers; Java (Hotspot JVM), .NET, Python, Ruby, PHP, Node.js and Perl are supported too, each individually enabled in the `pyroscope.ebpf` component.
- Go pull: CPU, alloc objects/space, goroutines, block count/duration. Java: CPU, alloc objects/space, lock count/duration, wall.
- A Java wall profile received also ingests the CPU profile, even if CPU profiling is off.

## SDKs (push)
- All SDKs (Go, Java, .NET, .NET Framework, Ruby, Python, Rust, Node.js) support CPU.
- Go push also: alloc objects/space, inuse objects/space, goroutines, mutex and block count/duration.
- Exceptions: .NET only. Lock count/duration: Java and .NET. Wall: Java, .NET, .NET Framework, Node.js.
- Check the page's table for the other cells; do not assume a type exists for a language.

## Go SDK settings
```go
runtime.SetMutexProfileFraction(5)   // only needed for mutex profiling
runtime.SetBlockProfileRate(5)       // only needed for block profiling
pyroscope.Start(pyroscope.Config{
  ApplicationName: "checkout",
  ServerAddress:   "http://pyroscope-server:4040",
  ProfileTypes: []pyroscope.ProfileType{
    pyroscope.ProfileCPU, pyroscope.ProfileAllocObjects, pyroscope.ProfileAllocSpace,
    pyroscope.ProfileInuseObjects, pyroscope.ProfileInuseSpace, // default set above
    pyroscope.ProfileGoroutines, pyroscope.ProfileMutexCount, pyroscope.ProfileMutexDuration,
    pyroscope.ProfileBlockCount, pyroscope.ProfileBlockDuration, // optional
  },
})
```
- Default Go types: CPU, alloc objects/space, inuse objects/space. Goroutines, mutex and block types are optional.
- Mutex rate: on average 1/rate contention events are reported. Block rate: aims for one blocking event per `rate` nanoseconds blocked.
- Heap profiles force a GC each time by default; `DisableGCRuns: true` cuts that CPU cost at the price of a less precise heap profile.

## Span profiles
Only the CPU profile type is supported for span profiles (Go, Java, Ruby, .NET, Python).

## Tag names
Tags must match `[a-zA-Z_][a-zA-Z0-9_]`; a period is not valid in a tag or label name.

## Checked
2026-11-08. Confirmed against the Pyroscope profiling-types, configure-client and Go (push mode) pages: type list, Alloy and SDK support tables (cells quoted above), span-profile limit, Go config, sampling-rate semantics, DisableGCRuns, tag format. Removed: flame-graph reading rules and diff-view advice, the Verify checklist, and the go.dev source (not read in full).
Method: documentation only; no commands were run.
