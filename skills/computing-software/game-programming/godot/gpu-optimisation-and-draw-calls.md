---
id: computing-software.game-programming.godot.gpu-optimisation-and-draw-calls
name: gpu-optimisation-and-draw-calls
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gpu, draw-calls, multimesh, batching, lod, game-programming, godot-draw-calls]
level: practitioner
status: docs-checked
description: "Reduce Godot draw calls and GPU cost: Visual Profiler, material reuse, automatic instancing and MultiMesh, 2D batching, mesh LOD and visibility ranges."
sources: ["https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html", "https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# GPU optimisation and draw calls

**Goal:** identify whether a Godot scene is limited by draw calls, vertices or shading, and fix that.

## Measure
- Debugger panel **Monitors** and **Visual Profiler**. The Visual Profiler shows CPU and GPU time for rendering tasks
  only (not scripting or physics; use the standard Profiler for those), results vary with viewport resolution, and
  it is not supported on the Compatibility renderer on macOS. Run the project, open the tab, click Start.
- The standard Profiler is off by default because it is performance-intensive; click Start (or tick Autostart,
  which is not preserved across editor sessions).
- Profile exported builds on your lowest target device as well as in the editor.

## Draw calls (CPU-side cost)
- **Reuse materials**: fewer distinct materials render faster in scenes with hundreds or thousands of objects.
  In the worst case use texture atlases to reduce texture changes. If materials cannot be reused, reuse shaders:
  StandardMaterial3Ds with the same feature configuration share a shader even with different parameters.
- **Automatic instancing**: MeshInstance3D nodes with the same mesh and material are instanced with no setup, but
  the material must be opaque or alpha-tested (alpha scissor or alpha hash); alpha-blended or depth pre-pass
  materials are never instanced this way.
- **MultiMesh** for thousands of identical objects in the same place or nearby (flocks, grass, particles).
- **2D batching**: similar items are grouped into a batch with a single draw call, keeping state, material and
  texture changes to a minimum; keep items with the same texture and material together.

## Vertices and LOD
Mesh level of detail can be generated automatically on mesh import; visibility ranges (HLOD) are the manual
approach set on 3D nodes and also suit impostors for distant geometry. Godot does view frustum culling
automatically, which stops being enough in larger levels.

## Gotchas
- Check the optimisation pages for occlusion culling, resolution scaling, post-effect and shadow settings; this
  skill no longer lists their property names because they were not confirmed.

## Verify
- [ ] Draw calls and GPU frame time recorded per level on the lowest target device and within budget.

## Checked
2026-10-28. Confirmed on the GPU optimization, 3D performance and profiler pages and the debugger panel: Visual
Profiler scope and limits, profiler off by default, material and shader reuse, atlases, automatic instancing
conditions, MultiMesh, 2D batching, import LOD, visibility ranges, frustum culling. Removed (not confirmed): the
specific Monitors entries, viewport debug draw modes and `viewport_set_measure_render_time`, RenderDoc, the Forward+
and Mobile batching claim, `lod_bias`, OccluderInstance3D, particle/alpha-scissor fill-rate advice, post-effect and
shadow settings, `scaling_3d_*` modes, and the `duplicate()` material claim.
Method: documentation only; no commands were run.
