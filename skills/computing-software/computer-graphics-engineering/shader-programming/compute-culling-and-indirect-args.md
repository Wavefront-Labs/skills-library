---
id: computing-software.computer-graphics-engineering.shader-programming.compute-culling-and-indirect-args
name: compute-culling-and-indirect-args
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, compute-culling, gpu-driven-rendering, indirect-draw, hi-z-occlusion, frustum-culling, two-phase-occlusion]
level: advanced
status: docs-checked
description: "Cull instances in compute and emit indirect draw args: frustum and Hi-Z occlusion tests, two-phase occlusion culling, DrawIndirectCount and ExecuteIndirect output."
sources: ["https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#drawing-indirect", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/indirect-drawing", "https://vkguide.dev/docs/gpudriven/compute_culling/", "https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute-based culling and indirect argument generation

## 1. Data layout
- Instance buffer: per-object bounding sphere (or AABB) in object space, transform index, mesh/LOD id.
- Draw command buffer: `VkDrawIndexedIndirectCommand {indexCount, instanceCount, firstIndex,
  vertexOffset, firstInstance}` per mesh/batch.
- Visible instance buffer: indices written by the cull shader, read in the vertex shader via
  `gl_InstanceIndex` (which in Vulkan already includes firstInstance).

## 2. Cull shader
```glsl
void main() {
    uint i = gl_GlobalInvocationID.x; if (i >= objectCount) return;
    Obj o = objects[i];
    vec4 s = view * model[o.xform] * vec4(o.center, 1.0); float r = o.radius * o.maxScale;
    bool visible = true;
    for (int p = 0; p < 6; p++) visible = visible && dot(frustum[p], vec4(s.xyz, 1.0)) > -r;
    if (visible && occlusionEnabled) visible = !hizOccluded(s.xyz, r);
    if (visible) {
        uint slot = atomicAdd(draws[o.mesh].instanceCount, 1u);
        visibleIds[draws[o.mesh].firstInstance + slot] = i;
    }
}
```
Reset `instanceCount` to 0 per draw before the dispatch (a clear pass or copy).

## 3. Hi-Z occlusion test
- Build a depth pyramid (max depth per 2x2 for standard Z, min for reversed-Z) from last frame's or
  this frame's early depth.
- Project the bounding sphere to a screen rect; choose the mip where the rect covers ~2x2 texels;
  compare the sphere's nearest depth with the pyramid's farthest depth over those texels.

## 4. Two-phase occlusion culling
1. Draw objects visible last frame (no occlusion test; trust history).
2. Build Hi-Z from that depth.
3. Test all objects against the new Hi-Z; draw those that became visible and weren't drawn in
   phase 1. Record visibility for next frame.
Avoids one-frame popping of reprojection-only schemes.

## 5. Submitting
- Vulkan: `vkCmdDrawIndexedIndirectCount` (core 1.2, needs the `drawIndirectCount` feature) with a count buffer for compacted commands, or
  a fixed draw count with zero-instance commands.
- D3D12: `ExecuteIndirect` with a command signature (a signature can set a root constant per draw; the root constant is reset to 0 after the call).
- Barrier: compute write -> indirect read + vertex shader read.

## Gotchas
- Sphere projection for Hi-Z must handle spheres crossing the near plane (treat as visible).
- Last-frame depth with a fast camera causes false occlusion: two-phase fixes it.
- Shadow passes need their own culling (light frustum), not the camera result.

## Verify
- [ ] Debug overlay draws culled bounds; counts per frame logged.
- [ ] No popping when turning quickly or when occluders move.

## Checked

Checked 2026-10-26 against Vulkan-Docs features and interfaces chapters (main, 2026-10-23), Microsoft D3D12 indirect drawing page. Confirmed: `VkDrawIndexedIndirectCommand` fields (indexCount, instanceCount, firstIndex, vertexOffset, firstInstance); `gl_InstanceIndex` includes `firstInstance` in Vulkan; `vkCmdDrawIndexedIndirectCount` is gated by the `drawIndirectCount` feature; D3D12 `ExecuteIndirect` command signatures and per-draw root constants. The Hi-Z and two-phase occlusion culling descriptions are algorithmic and were not checked against a primary source.

Method: documentation only; no commands were run.
