---
id: computing-software.game-programming.unreal-engine.profilegpu-and-gpu-visualizer
name: profilegpu-and-gpu-visualizer
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-insights, gpu-visualizer, profilegpu, gpu-profiling, game-programming]
level: practitioner
status: draft
description: "Find Unreal GPU bottlenecks with ProfileGPU and the GPU Visualizer, stat gpu, r.ScreenPercentage tests, and Insights GPU tracks before tuning settings."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gpu-profiling-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ProfileGPU and the GPU Visualizer

**Goal:** know which passes cost GPU time and whether you are resolution, geometry or shader bound.

## First: are you GPU bound?
`stat unit`: if **GPU** is the largest of Game/Draw/GPU and close to Frame, you are GPU bound.
`stat unitgraph` for spikes.

## Capture
- `ProfileGPU` (or Ctrl+Shift+, in editor) captures one frame and opens the **GPU Visualizer**: tree of
  passes (BasePass, Lights, Shadow Depths, Translucency, PostProcessing, Lumen, Nanite...) with ms.
- `r.ProfileGPU.ShowUI 0` to log to the output instead (packaged/dev builds).
- `stat gpu`: live per-category GPU stats (requires `r.GPUStatsEnabled 1`).
- Unreal Insights with `-trace=default,gpu` gives GPU timing tracks over many frames.

## Quick bisection tests
- `r.ScreenPercentage 50`: big gain = pixel/fill bound (post, lighting, overdraw, resolution).
  Little gain = geometry/vertex or fixed-cost passes.
- `show <flag>` toggles (e.g. `show Translucency`, `show Particles`, `show DynamicShadows`) to see
  the cost of a feature.
- `r.Shadow.MaxResolution`, `r.Lumen...`, `sg.<Group>Quality` for settings sensitivity.
- Viewport > Optimization Viewmodes: Shader Complexity, Quad Overdraw, Light Complexity.

## Common culprits
- Shadow Depths with many movable lights / high cascade counts (`r.Shadow.CSM.MaxCascades`).
- Translucency overdraw (particles, foliage cards).
- Post-process materials at full resolution; DOF/Motion blur on low-end.
- Lumen/Nanite costs on hardware below target — check scalability levels.

## Platform tools
For deeper analysis: RenderDoc (plugin, `renderdoc.CaptureFrame`), PIX on Windows/Xbox, Nsight,
Razor/console tools — ProfileGPU tells you where to look.

## Gotchas
- Editor viewport adds overhead (editor rendering, selection outlines): profile in Standalone or
  packaged Test builds.
- VSync caps hide headroom: `r.VSync 0` and `t.MaxFPS 0` when measuring.

## Verify
- [ ] Capture before/after each change; record pass timings in the PR.
- [ ] Bottleneck classified (pixel vs geometry vs specific pass) before tuning.
