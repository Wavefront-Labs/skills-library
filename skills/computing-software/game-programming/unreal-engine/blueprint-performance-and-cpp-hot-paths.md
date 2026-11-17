---
id: computing-software.game-programming.unreal-engine.blueprint-performance-and-cpp-hot-paths
name: blueprint-performance-and-cpp-hot-paths
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, blueprint-performance, blueprints, tick, profiling, cpp, game-programming]
level: practitioner
status: docs-checked
description: "Decide what belongs in Blueprints vs C++, control Actor ticking (groups, dependency, enable/disable) and find hot spots with Unreal Insights, per Epic's docs."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprint-best-practices-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-ticking-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blueprint performance and C++ hot paths

**Goal:** keep per-frame work out of Blueprints, tick only what needs it, and profile before moving code to C++.

## Blueprint vs C++ (Blueprint Best Practices page)
- Some things impact performance more in Blueprints. A Blueprint doing a lot of operations and complex math every tick may
  be better as native C++.
- Blueprints are best for event-driven functionality such as damage taking and controls, "things that don't get called
  every frame".
- Macros are copied into the graph at compile time (can hold latent nodes, multiple exec wires); functions are really
  called, can be targeted from other Blueprints and overridden in children. Page rule of thumb: macro for a quick bit of
  functionality reused everywhere; function if children may tweak it or other Blueprints call it.
- If the same set of nodes is used more than twice in a graph, make it a function or macro.

## Ticking (Actor Ticking page)
- Actors and components tick once per frame unless given a minimum interval, or can be set not to tick at all.
- Tick groups in order: `TG_PrePhysics`, `TG_DuringPhysics`, `TG_PostPhysics`, `TG_PostUpdateWork`; each group finishes
  all its members before the next starts. PrePhysics: for interacting with physics objects (physics data is one frame
  old). DuringPhysics: only for logic that ignores physics data or can be a frame off (inventory screens, minimaps).
  PostPhysics: final physics results (weapon or movement traces). PostUpdateWork: after cameras update.
- Tick dependency (`AddTickPrerequisiteActor`, `AddTickPrerequisiteComponent`): wait for another actor or component to
  tick. The page prefers it to moving a whole group because many actors in the same group can update in parallel.
- Page snippet in the constructor: `PrimaryActorTick.bCanEverTick = true; PrimaryActorTick.bTickEvenWhenPaused = true;
  PrimaryActorTick.TickGroup = TG_PrePhysics;` and the `PrimaryComponentTick` equivalents. Actor `Tick()` vs component
  `TickComponent()`. Actors register tick functions in BeginPlay.
- Toggle at runtime with `AActor::SetActorTickEnabled` and `UActorComponent::SetComponentTickEnabled`. Multiple tick
  functions via a struct inheriting `FTickFunction` (override `ExecuteTick`, `DiagnosticMessage`).

## Measuring (Unreal Insights page)
- Unreal Insights captures telemetry from a running project (.utrace files) and analyzes it. Start from the
  Trace/Insights status bar widget in the editor; a prebuilt exe is at `Engine\Binaries\[Platform]\UnrealInsights[.exe]`.
- The Trace Server (`UnrealTraceServer.exe`) listens on port 1981. Timing Insights shows CPU and GPU tracks; Memory,
  Networking, Slate, Asset Loading and Cooking Insights exist.
- Per-channel `-trace=` arguments are on the separate Trace and Reference pages, which were not read.

## Checked
Date: 2026-11-07. Read in full: Blueprint Best Practices, Actor Ticking and Unreal Insights pages (all sections),
unversioned en-us pages with no engine version stated.
Removed as not on those pages: per-node VM cost claims, pure-node re-evaluation, `GetAllActorsOfClass` cost, hard
reference and cast-replacement advice, the Tick Interval property and "Start with Tick Enabled" setting, `-trace=cpu,frame`,
`-statnamedevents`, `stat game`, `dumpticks`, "nativization removed in UE5", editor-vs-packaged speed claims, PIE debugging
overhead, and the Verify checklist.
Method: documentation only; no commands were run.
