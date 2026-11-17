---
id: computing-software.software-engineering.fsharp.gc-runtime-settings
name: gc-runtime-settings
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, gc-runtime-settings, fsharp-perf-measure, server-gc, tiered-pgo]
level: advanced
status: draft
description: "Tune the .NET runtime for F# apps with ServerGarbageCollector, ConcurrentGarbageCollection, TieredPGO and InvariantGlobalization."
sources:
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Runtime settings
**Goal:** know the knobs and when to turn them.

```xml
<PropertyGroup>
  <ServerGarbageCollector>true</ServerGarbageCollector>
  <ConcurrentGarbageCollection>false</ConcurrentGarbageCollection>
  <TieredPGO>true</TieredPGO>
  <TieredCompilation>true</TieredCompilation>
  <InvariantGlobalization>true</InvariantGlobalization>
</PropertyGroup>
```
- Workstation GC is the default for console apps; Server GC (ASP.NET defaults vary) uses per-core heaps and more memory for throughput.
- Disabling concurrent GC reduces background threads for latency-sensitive or container-limited apps.
- Tiered compilation starts fast and re-JITs hot methods; Dynamic PGO is on by default in newer runtimes (unconfirmed which version), `TieredPGO` toggles it.
- `InvariantGlobalization` drops ICU and culture data, shrinking containers (and changing culture behaviour).
- Container memory/CPU limits are honoured by the runtime; check `GCHeapHardLimit` options if needed.
- Settings also live in `runtimeconfig.json` or `DOTNET_*` environment variables.

## Gotchas
- Measure before and after; server GC can use much more memory.
- InvariantGlobalization breaks culture-specific formatting expectations.

## Self-check
Toggle `ServerGarbageCollector` and compare dotnet-counters GC heap size.
