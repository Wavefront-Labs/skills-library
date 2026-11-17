---
id: computing-software.game-programming.game-engine-architecture.render-graph-frame-graph-architecture
name: render-graph-frame-graph-architecture
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, render-graph-architecture, frame-graph, transient-resources, resource-barriers, pass-culling, async-compute, game-programming]
level: sme
status: draft
description: "Design a render graph: declare passes and resource reads/writes, compile to cull passes, alias transient memory, insert barriers and schedule async compute."
sources: ["https://www.gdcvault.com/play/1024612/FrameGraph-Extensible-Rendering-Architecture-in", "https://dev.epicgames.com/documentation/en-us/unreal-engine/render-dependency-graph-in-unreal-engine", "https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@17.0/manual/render-graph-system.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render graph / frame graph architecture

**Goal:** a renderer where features are added as passes that declare what they read and write, and
the graph handles ordering, memory and synchronisation (Frostbite FrameGraph, GDC 2017; Unreal RDG;
Unity Render Graph).

## Three phases per frame
1. **Setup:** each pass declares inputs/outputs.
```cpp
struct GBufferData { RGTexture albedo, normal, depth; };
auto& gb = graph.addPass<GBufferData>("GBuffer",
    [&](RGBuilder& b, GBufferData& d) {
        d.albedo = b.create("Albedo", {w, h, RGBA8});    // transient: lives only within the frame
        d.normal = b.create("Normal", {w, h, RGB10A2});
        d.depth  = b.create("Depth",  {w, h, D32});
        b.write(d.albedo); b.write(d.normal); b.write(d.depth);
    },
    [=](const GBufferData& d, RGContext& ctx) { drawOpaque(ctx, d); });
graph.addPass<LightingData>("Lighting", [&](RGBuilder& b, LightingData& d) {
        d.gb = b.read(gb.albedo); /* ... */ d.out = b.write(b.import(backbuffer));
    }, executeLighting);
```
2. **Compile:** build the dependency DAG from read/write edges; **cull** passes whose outputs nobody
   reads (reference counting from imported/output resources backwards); compute each transient
   resource's first and last use; **alias** non-overlapping transients onto the same memory;
   determine resource state transitions and insert **barriers**; order passes (topological).
3. **Execute:** run pass lambdas in order, recording command lists (parallelisable per pass).

## Benefits
- Features become self-contained passes; disabling a feature removes its passes and memory.
- Transient aliasing commonly saves large amounts of render-target memory.
- Correct barriers/layout transitions in one place for D3D12/Vulkan.
- Async compute: passes flagged compute-capable can be scheduled on a second queue with fences
  derived from the graph.

## Design rules
- Imported resources (backbuffer, history buffers, persistent shadow atlases) have external
  lifetime; everything else should be transient.
- Do no resource creation or GPU work in setup lambdas, only declarations.
- Make passes declare **every** access, including UAV read-modify-write, or barriers are wrong.
- Keep graph rebuild per frame cheap (it is rebuilt every frame in Frostbite/RDG); cache compiled
  results only if profiling demands it.

## Engine specifics
Unreal RDG: `FRDGBuilder GraphBuilder(RHICmdList); GraphBuilder.AddPass(RDG_EVENT_NAME("X"),
PassParameters, ERDGPassFlags::Raster, Lambda); GraphBuilder.Execute();` with `RDG_TEXTURE_ACCESS`
in shader parameter structs; debug via `r.RDG.Debug 1`, `r.RDG.ImmediateMode 1` (executes passes
on add, to locate crashes). Unity URP 17+ (Unity 6) uses Render Graph for ScriptableRenderPasses
(`RecordRenderGraph`); Render Graph Viewer window shows passes and resource lifetimes.

## Verify
- [ ] Graph viewer shows culled passes when a feature is off.
- [ ] GPU validation layers report no missing/redundant barriers.
- [ ] Transient memory peak reported per frame and reduced vs pre-graph allocation.
