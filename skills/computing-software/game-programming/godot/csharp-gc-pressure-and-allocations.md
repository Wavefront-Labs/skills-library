---
id: computing-software.game-programming.godot.csharp-gc-pressure-and-allocations
name: csharp-gc-pressure-and-allocations
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-csharp, godot-csharp-gc, allocations, stringname-caching, game-programming]
level: practitioner
status: gated
description: "Reduce GC spikes in Godot C#: Variant and string marshalling, cached StringName/NodePath, Godot collections vs .NET, avoiding per-frame allocations and measuring them."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_basics.html#performance-of-c-in-godot", "https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_variant.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GC pressure and allocations in Godot C#

**Goal:** steady frame times in C# projects; no periodic hitches from .NET garbage collection.

## Allocation sources specific to Godot
- **String -> StringName/NodePath conversions** every call: `GetNode("Player")`, `Input.IsActionPressed("jump")`,
  `EmitSignal("hit")`, `anim.Play("run")` allocate a native StringName each time. Cache:
```csharp
static readonly StringName Jump = "jump";
static readonly NodePath PlayerPath = "../Player";
if (Input.IsActionPressed(Jump)) ...
```
  Prefer the generated `SignalName`, `MethodName` and `PropertyName` StringName constants to avoid extra StringName allocations (per the C# basics docs).
- **Godot.Collections** types are Godot-backed Variant containers; use `System.Collections.Generic` for game logic where possible and convert at API boundaries (see the C# Variant docs).
- **Variant boxing**: `Call`, `Get`/`Set` by name, signals with Variant args. Prefer typed C# calls and
  C# events for C#-to-C# communication.
- Engine methods that return arrays or collections create new ones per call; cache results rather than calling every frame.
- Usual .NET suspects: LINQ in hot paths, closures, `string.Format`/interpolation, boxing enums in
  generic non-constrained code.

## Measuring
- `GC.GetAllocatedBytesForCurrentThread()` delta per frame in a debug overlay (gated: unconfirmed, source is paywalled or blocked).
- The .NET diagnostics tools (`dotnet-counters`, `dotnet-trace`); see Microsoft's documentation for their options.

## GC settings
The .NET runtime GC settings and `GCSettings.LatencyMode` are documented by Microsoft; measure before changing them. Not covered by the Godot docs.

## Gotchas
- Struct math types such as `Vector3` are value types.
- Cache node references instead of calling `GetNode<T>` each frame.

## Verify
- [ ] Allocated bytes per frame ~0 in steady gameplay.
- [ ] A .NET diagnostics tool shows no regular gen-2 collections during play.

## Checked

2026-10-28. Confirmed against: C# basics and C# Variant pages (use the exposed StringName in PropertyName, MethodName and SignalName to avoid extra StringName allocations; Godot.Collections namespace types).

Removed or rewritten: the .NET 8 default-GC statement, ServerGarbageCollector and SustainedLowLatency advice, counter names, per-call allocation claims for specific engine methods, dispose/finalize statements and the cache-GetNode claim phrasing.

Gated: the .NET GC tuning advice is not covered by the Godot docs and was not confirmed against Microsoft's documentation in this batch (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
