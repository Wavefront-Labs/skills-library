---
id: computing-software.software-engineering.csharp-dotnet.gc-modes-runtimeconfig-and-large-object-heap
name: gc-modes-runtimeconfig-and-large-object-heap
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-memory-management, gc-settings-runtimeconfig, large-object-heap, server-gc, concurrent-gc, gc-conserve-memory]
level: advanced
status: docs-checked
description: "Tune the .NET GC through runtimeconfig.json and env vars: workstation vs server, concurrent, DATAS, container limits, and keep large arrays off the Large Object Heap."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/runtime-config/garbage-collector", "https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/large-object-heap", "https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GC settings and the Large Object Heap

## Settings (csproj properties become runtimeconfig.json)
```xml
<PropertyGroup>
  <ServerGarbageCollection>true</ServerGarbageCollection>          <!-- System.GC.Server: false = workstation (the default) -->
  <ConcurrentGarbageCollection>true</ConcurrentGarbageCollection>  <!-- System.GC.Concurrent: true = background GC -->
</PropertyGroup>
```
Others in `runtimeconfig.template.json`: `System.GC.ConserveMemory` (0-9; trades more frequent GCs and possibly longer pauses for a smaller heap; non-zero also compacts the LOH automatically when it is too fragmented), `System.GC.HeapHardLimit` / `System.GC.HeapHardLimitPercent`, `System.GC.HeapCount` (server GC only), `System.GC.RetainVM`. Env equivalents: `DOTNET_gcServer=1`, `DOTNET_GCHeapCount`; for env vars the heap-limit and heap-count values are hexadecimal (decimal in runtimeconfig.json).
- Workstation GC is the default; server GC (`System.GC.Server`) is opt-in.
- **DATAS** (dynamic adaptation to application sizes): setting `System.GC.DynamicAdaptationMode` (1 enabled, 0 disabled; env `DOTNET_GCDynamicAdaptationMode`) exists from .NET 8 and DATAS is enabled by default from .NET 9 (server GC). It sizes the heap roughly in proportion to long-lived data; it starts with one heap.
- Containers: when a memory limit is set, the GC treats it as total physical memory, and the default hard limit is 75% of it.

## LOH
Objects of 85,000 bytes or more go to the large object heap, which is collected only during a generation 2 GC and is not compacted by default (fragmentation is possible).
- `GCSettings.LargeObjectHeapCompactionMode` asks for the LOH to be compacted during the next full blocking GC; if objects must not move, pin them.
- Keep large short-lived allocations rare: temporary large objects trigger repeated gen2 GCs (trigger reason AllocLarge in the docs' PerfView example).

## Gotchas
- Calling `GC.Collect()` routinely hurts; measure first.
- A memory limit on a container affects GC behaviour; test with the real limit.

## Checked
Date: 2026-11-09. Confirmed against the three cited Microsoft Learn pages (runtime-config/garbage-collector, large-object-heap, garbage-collection fundamentals): property names (the MSBuild property is `ServerGarbageCollection`, fixed from `ServerGarbageCollector`), workstation default, ConserveMemory 0-9 and LOH auto-compaction, DATAS setting and .NET 9 default, 75% container default, hex env values, 85,000-byte threshold, gen2-only collection, LOH compaction mode. Removed unconfirmed claims: TieredPGO, ASP.NET workstation wording, ArrayPool/MemoryPool/RecyclableMemoryStream advice, tooling commands, restart and 256 MB container remarks.
Method: documentation only; no commands were run.
