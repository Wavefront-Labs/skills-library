---
id: computing-software.game-programming.unity.rendering-statistics-and-batch-counts
name: rendering-statistics-and-batch-counts
category: computing-software
field: game-programming
product: unity
tags: [unity, rendering-statistics, stats-window, draw-calls, setpass-calls, batches, game-programming]
level: practitioner
status: docs-checked
description: "Read Unity rendering statistics (Game view Stats, Rendering Profiler module, ProfilerRecorder counters): batches, SetPass calls, triangles, draw breakdown."
sources: ["https://docs.unity3d.com/Manual/RenderingStatistics.html", "https://docs.unity3d.com/Manual/ProfilerRendering.html", "https://docs.unity3d.com/ScriptReference/Unity.Profiling.ProfilerRecorder.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rendering statistics and batch counts

**Goal:** know whether a scene is draw-call bound and where the draw calls come from.

## Where to read them
- **Game view Stats**: enter Play mode, select the **Stats** button in the top-right of the Game view. Which
  statistics appear depends on your build profile. Sections: Hardware (FPS, Global Frametime, GPU Frametime,
  CPU Main Thread vs Render Thread), Scene (Triangles, Vertices, Set Pass Calls, Draw Calls), Memory, and
  Animation and Meshes (In-flight animators, Visible skinned meshes, Updated skinned meshes).
  The main-thread percentage includes Editor work (Scene view, other windows); the render-thread value does not.
- **Profiler > Rendering module** (Window > Analysis > Profiler): the chart shows Batches Count, SetPass Calls
  Count, Triangles Count and Vertices Count; the details pane matches the Stats window and has an Open Frame
  Debugger button. Some detail statistics (static batching, instancing, used textures) are not accessible in
  Release Players; SetPass Calls, Draw Calls, Batches, Triangles, Vertices, Render Textures, Used Buffers and
  Shadow Casters Count are.
- **In code** with `ProfilerRecorder` (Editor and Player builds, including Release Players):
```csharp
ProfilerRecorder setPass, draws;
void OnEnable() {
    setPass = ProfilerRecorder.StartNew(ProfilerCategory.Render, "SetPass Calls Count");
    draws   = ProfilerRecorder.StartNew(ProfilerCategory.Render, "Draw Calls Count");
}
void OnDisable() { setPass.Dispose(); draws.Dispose(); }
// read .LastValue when Valid is true
```
`ProfilerRecorder` allocates unmanaged resources, so call `Dispose`. `ProfilerRecorderHandle.GetAvailable`
lists the supported metrics.

## Reading them
- **Set Pass Calls**: times Unity switches shader pass; each pass needs a new shader bound, which might add CPU
  overhead.
- **Draw Calls**: the Stats window shows in parentheses how many were combined into instances, and a foldout
  breaks them down: SRP Batcher, BRG/GRD (BatchRendererGroup API and GPU Resident Drawer), Non-SRP Compatible
  (not compatible with the SRP Batcher and not optimised by BRG, GPU Resident Drawer or GPU instancing), and
  Standard Instanced (GPU Instancing).
- **Triangles and Vertices**: the page says these matter most when optimising for low-end hardware.
- **Shadow Casters Count**: GameObjects casting shadows; one entry per shadow cast if several lights light it.
A large Non-SRP Compatible count is the first thing to look at when draw calls are high.

## Workflow
1. Compare CPU main thread, render thread and GPU frametime first.
2. If rendering is the bottleneck, use these counters, then open the Frame Debugger from the Rendering module to
   see individual draw calls.

## Verify
- [ ] Counters are tracked on a player build per level, using the budget set for your target hardware.

## Checked
Date 2026-11-09. Read in full as fetched text: Rendering Statistics window reference, Rendering Profiler module
reference, ProfilerRecorder script reference. Confirmed statistic names and meanings, draw breakdown categories,
Release Player availability, ProfilerRecorder counter names used above and Dispose requirement.
Removed as unconfirmed: the lever table (atlases, LODs, shadow distance and similar advice), the "SRP Batcher can
keep batches high while SetPass is low" claim, Frame Debugger break-reason strings, canvas and editor camera
gotchas and the numeric budget example.
Method: documentation only; no commands were run.
