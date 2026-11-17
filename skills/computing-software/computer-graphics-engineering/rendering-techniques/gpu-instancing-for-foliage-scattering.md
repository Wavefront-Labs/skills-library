---
id: computing-software.computer-graphics-engineering.rendering-techniques.gpu-instancing-for-foliage-scattering
name: gpu-instancing-for-foliage-scattering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-lod, gpu-instancing, foliage-rendering, procedural-scattering, indirect-draw, compute-shader, vegetation]
level: practitioner
status: draft
description: "Render dense foliage with GPU instancing and procedural scattering: instance buffers, compute-based placement from density maps, per-instance culling/LOD and indirect draws."
sources: ["https://developer.nvidia.com/gpugems/gpugems3/part-i-geometry/chapter-1-generating-complex-procedural-terrains-using-gpu", "https://www.gdcvault.com/play/1027033/Advanced-Graphics-Summit-Procedural-Grass", "https://docs.unity3d.com/ScriptReference/Graphics.RenderMeshIndirect.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Foliage instancing and GPU scattering

## 1. Instancing basics
One draw renders many copies of a mesh; per-instance data (transform, colour variation, LOD fade)
comes from a structured buffer indexed by instance ID.
- Compact transforms: position (3 floats) + quaternion or yaw + uniform scale packed into 16-32 bytes.
- GL `glDrawElementsInstanced`, D3D `DrawIndexedInstanced`, Vulkan `vkCmdDrawIndexed` with
  instanceCount, Unity `Graphics.RenderMeshInstanced/Indirect`.

## 2. GPU scattering
Generate instances in compute instead of storing millions in assets:
1. Per terrain tile near the camera, dispatch threads on a jittered grid (or Poisson pattern).
2. Sample density maps (painted foliage layers, slope/height rules, exclusion masks from roads).
3. Hash position for random rotation/scale/variant; reject by density.
4. Frustum/occlusion cull, choose LOD by distance, append to per-LOD instance lists.
5. Write indirect args (instance counts) and draw with `DrawIndexedIndirect`.
Regenerate tiles as the camera moves (ring buffer of tiles) - zero storage for grass.

## 3. LOD and density falloff
- Mesh LODs (blade clusters -> cards -> nothing) by distance.
- Reduce density with distance by rejecting a hashed fraction, while scaling up survivors to keep
  coverage (avoids visible thinning).
- Crossfade with dithering (hash-based alpha test) to hide pops.

## 4. Grass specifics
Ghost of Tsushima generated blades procedurally in compute (per-blade Bezier curves, wind, LOD by
vertex count) - see GDC 2021 "Procedural Grass in Ghost of Tsushima".

## Gotchas
- Per-instance data fetch in the vertex shader is cheap; per-instance CPU work isn't. Keep the CPU
  out of the per-instance loop.
- Shadows of millions of instances: render grass shadows only near the camera or not at all; use
  contact shadows/AO.
- Motion vectors for wind-animated instances need previous-frame wind.

## Verify
- [ ] Instance count, GPU time per LOD logged; CPU time constant regardless of density.
- [ ] No visible popping or thinning when moving.
