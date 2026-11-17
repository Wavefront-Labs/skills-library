---
id: computing-software.computer-graphics-engineering.rendering-techniques.impostors-and-billboards
name: impostors-and-billboards
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-algorithms, impostors, billboards, octahedral-impostors, imposter-baking, axial-billboard, sprite-lod, vegetation-lod]
level: advanced
status: draft
description: "Replace distant geometry with billboards and impostors: camera-facing and axial billboards, baking octahedral impostor atlases with normals/depth, frame blending."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 13.6", "https://shaderbits.com/blog/octahedral-impostors", "https://developer.nvidia.com/gpugems/gpugems3/part-i-geometry/chapter-4-next-generation-speedtree-rendering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Impostors and billboards

**Goal:** forests, crowds and city skylines at long range for a few triangles each, without
looking like flat cards (RTR4 §13.6).

## 1. Billboards
- **Screen-aligned / view-facing**: quad expanded in the vertex shader along camera right/up —
  particles, distant lights.
- **Axial (cylindrical)**: rotates only around the object's up axis — trees, grass, poles;
  stays upright when the camera tilts.
```glsl
vec3 right = normalize(cross(vec3(0, 1, 0), viewDirToObject));       // axial
vec3 worldPos = center + right * corner.x * size.x + vec3(0, 1, 0) * corner.y * size.y;
```
Use alpha-test (with alpha-to-coverage under MSAA) rather than blending for opaque foliage.

## 2. Impostors: capture many views
Render the object from N directions offline into an atlas, storing **albedo+alpha, normal,
depth** (and optionally roughness/AO). At runtime pick the frame(s) nearest the view direction.
- **Octahedral impostors** (Ryan Brucks): view directions mapped onto an octahedron unfolded
  into a square grid (e.g. 8x8 or 12x12 frames); hemispherical variant for objects only seen
  from above.
- **Frame blending**: blend the 3 nearest frames (barycentric on the octahedral grid) to hide
  transitions; use depth for parallax-correcting each frame's UVs.

## 3. Lighting
Store normals (and depth) so impostors are **lit dynamically** in the same G-buffer/forward
path as meshes — baked lighting in the atlas breaks with time-of-day. Depth output lets
impostors intersect terrain correctly and cast/receive shadows plausibly.

## 4. Transition from mesh
LOD chain ends with the impostor; cross-fade with dither over ~0.3 s. Match bounding and
pivot exactly; bake at a resolution so impostor texels ≈ screen pixels at the switch distance.

## Gotchas
- Too few frames → visible "snapping" as the camera orbits; too many → huge atlases.
  8x8 at 2048² (256² per frame) is a common start for trees.
- Mip bleeding between atlas frames: pad frames and clamp mips.
- Alpha-tested mips lose coverage (trees thin out at distance) — preserve coverage when
  generating alpha mips.

## Verify
- [ ] Orbiting camera at switch distance: no visible popping/snapping.
- [ ] Impostors darken/brighten with sun direction like the meshes.
- [ ] Draw/triangle counts for a forest scene drop by the expected factor.
