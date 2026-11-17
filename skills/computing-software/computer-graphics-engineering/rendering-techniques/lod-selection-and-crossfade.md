---
id: computing-software.computer-graphics-engineering.rendering-techniques.lod-selection-and-crossfade
name: lod-selection-and-crossfade
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-algorithms, level-of-detail, lod-selection, lod-crossfade, screen-space-error, dithered-lod, hysteresis, lod-bias]
level: practitioner
status: draft
description: "Select mesh LODs by projected screen size or geometric error, avoid popping with hysteresis and dithered cross-fades, and budget LOD bias per platform and quality setting."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 19.9", "https://docs.unrealengine.com/5.3/en-US/creating-and-using-lods-in-unreal-engine/", "https://docs.unity3d.com/Manual/class-LODGroup.html", "https://developer.nvidia.com/gpugems/gpugems2/part-i-geometric-complexity/chapter-4-inside-geometry-instancing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LOD selection and cross-fading

**Goal:** draw fewer triangles for distant objects without visible popping, with LOD
switches driven by what's actually on screen (RTR4 §19.9).

## 1. Selection metric
Distance alone breaks with FOV changes (zoom/scopes) and resolution. Use **projected size**:
```cpp
float projectedRadiusPx(const Sphere& s, const Camera& c, float screenH) {
    float d = max(length(s.center - c.pos), s.radius);
    return (s.radius / (d * tanf(c.fovY * 0.5f))) * (screenH * 0.5f);
}
// LOD i used while projected size >= threshold[i]; thresholds authored per asset (e.g. 300, 120, 50, 15 px)
```
Better still with **geometric error**: each LOD stores max deviation ε (from the simplifier);
project ε to pixels and pick the coarsest LOD with error < 1 px (or a quality-setting target).

## 2. Global bias
`threshold *= lodBias` per quality level / platform; dynamic LOD bias when GPU-bound
(feedback from frame time). Shadow passes can use coarser LODs (separate bias) — shadows
tolerate it.

## 3. Avoid flicker: hysteresis
Switch to a coarser LOD at threshold × 0.9 and back at threshold × 1.1 so objects sitting
on a boundary don't toggle every frame.

## 4. Hide the switch: cross-fade
- **Dithered cross-fade**: for ~0.25–0.5 s render both LODs, outgoing with alpha-to-coverage
  or screen-door dithering `discard` using a complementary pattern
  (`dither > fade` vs `dither <= fade`) — no sorting, works in deferred, TAA smooths it.
- Alpha blending both LODs: requires sorting and breaks depth; avoid for opaque meshes.
- Geomorphing (vertex interpolation) for terrain/progressive meshes.
- Final LOD → impostor/billboard, then cull by distance with a fade.

## 5. Authoring
- Each LOD ~50% of the previous triangle count; keep silhouettes and UV seams.
- Same material count per LOD or fewer (merge materials at distant LODs to cut draw calls).
- Normal maps baked from the high-res mesh keep shading consistent across LODs.

## Gotchas
- LOD from the wrong camera in multi-view (shadows, reflections, VR) — compute per view or
  use the main camera consistently to avoid mismatched shadows.
- Skinned meshes: skeleton LOD (fewer bones) too, else CPU/GPU skinning cost stays.
- Bounding spheres must cover all LODs.

## Verify
- [ ] LOD debug colouring shows sensible transitions across distances and FOVs.
- [ ] Camera dolly slowly through thresholds: no visible pops with cross-fade enabled.
- [ ] Triangle counts per frame drop as expected; GPU time measured.
