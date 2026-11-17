---
id: computing-software.game-programming.unreal-engine.stat-commands-and-frame-budget
name: stat-commands-and-frame-budget
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, performance, stat-unit, stat-commands, frame-budget, gpu-profiling, profilegpu, game-programming]
level: practitioner
status: draft
description: "Diagnose frame time with stat unit, stat game, stat gpu, stat scenerendering and ProfileGPU: find whether game, draw or GPU thread is the bottleneck against the frame budget."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# stat commands and the frame budget

**Goal:** in two minutes, know which thread is over budget and which system to profile next.

## Budget
60 fps = 16.67 ms, 30 fps = 33.3 ms, 120 fps = 8.33 ms. The **slowest of Game, Draw (render thread),
RHI and GPU** sets the frame time; optimising the others gains nothing.

## stat unit (start here)
`stat unit` shows Frame, Game, Draw, RHIT, GPU, Mem and DynRes.
- Frame ≈ Game: game-thread bound (gameplay code, Blueprints, physics, animation, AI).
- Frame ≈ Draw: render-thread bound (too many draw calls / primitives, visibility).
- Frame ≈ GPU: GPU bound (pixels, shaders, shadows, Lumen, Nanite overdraw).
- `stat unitgraph` plots them over time to catch hitches.
Measure in a **packaged Development or Test build** (or Standalone with `-game`); editor PIE adds overhead.
Disable vsync / frame smoothing (`t.MaxFPS 0`, `r.VSync 0`) when measuring.

## Drill down
| Command | Shows |
|---|---|
| `stat game` | game-thread tick groups, world tick, net |
| `stat gpu` | per-pass GPU timings (BasePass, Shadows, Lumen, Translucency) |
| `stat scenerendering` | draw calls, mesh draw commands, visible primitives |
| `stat initviews` | visibility and occlusion culling cost |
| `stat anim`, `stat physics`, `stat ai`, `stat navigation` | those systems |
| `stat memory`, `stat streaming` | memory, texture streaming pool |
| `stat startfile` / `stat stopfile` | records a `.ue4stats` file for Session Frontend |
| `stat none` | clears all |

- `ProfileGPU` (Ctrl+Shift+,) captures one frame's GPU breakdown in the GPU Visualizer.
- `r.ScreenPercentage 50`: if GPU time drops a lot, you're pixel-bound.
- `show` flags (`show shadows`, `show postprocessing`) to A/B features; `viewmode shadercomplexity`,
  `viewmode quadoverdraw`, `viewmode lightcomplexity`.
- Hitches: `stat dumphitches` with `t.HitchThreshold`.

## Then
For precise, call-level timing use Unreal Insights (`-trace=cpu,gpu,frame`); stat commands are for triage.

## Verify
- [ ] The bottleneck thread is identified on target hardware, in a non-editor build.
- [ ] Every optimisation is re-measured with the same camera path and settings.
