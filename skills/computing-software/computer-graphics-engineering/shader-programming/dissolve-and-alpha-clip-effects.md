---
id: computing-software.computer-graphics-engineering.shader-programming.dissolve-and-alpha-clip-effects
name: dissolve-and-alpha-clip-effects
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, dissolve-effect, alpha-clip, discard, noise-threshold, burn-edge]
level: practitioner
status: draft
description: "Build dissolve and alpha-clip effects: noise threshold with discard, glowing burn edges, shadow-pass consistency, and the early-Z and MSAA costs of discard."
sources: ["https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/Alpha-Clip-Threshold.html", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/discard.xhtml", "https://developer.arm.com/documentation/101897/latest/Fragment-shading/Shader-discard"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dissolve and alpha-clip effects

## 1. Core dissolve
```glsl
uniform float uProgress;           // 0 = solid, 1 = gone
uniform sampler2D uNoise;
uniform vec3 uEdgeColor; uniform float uEdgeWidth;
void main() {
  float n = texture(uNoise, vUV).r;          // or 3D noise from world position for UV-less meshes
  float t = n - uProgress;
  if (t < 0.0) discard;
  float edge = 1.0 - smoothstep(0.0, uEdgeWidth, t);
  vec3 col = baseColor() + uEdgeColor * edge * 4.0;   // HDR emissive: blooms
  outColor = vec4(col, 1.0);
}
```
Remap progress to `mix(-uEdgeWidth, 1.0, p)` so the edge is visible at the start and fully
gone at 1.

## 2. Consistency
Apply the same discard in the **shadow and depth-prepass shaders**, or the invisible parts still
cast shadows and occlude.

## 3. Alpha clip for foliage/fences
`if (texture(albedo, uv).a < 0.5) discard;` with mip-mapped alpha: alpha shrinks in distant
mips and leaves vanish. Fix by computing per-mip alpha scale at import (preserve coverage), or
use alpha-to-coverage with MSAA.

## 4. Costs
- `discard` disables early-Z for that shader on many GPUs (depth written late); keep it out of
  opaque shaders that do not need it.
- On tile-based mobile GPUs discard breaks hidden surface removal benefits; draw clipped objects
  after opaque.
- Depth prepass with the clip shader, then main pass with `depthFunc EQUAL` and no discard,
  restores early-Z for expensive shading.

## Gotchas
- Noise from UVs shows seams on meshes with UV islands; world or object-space 3D noise avoids it.
- Dithered (screen-door) fades with TAA give a smooth fade without sorting.

## Verify
- [ ] Shadows dissolve with the mesh; profiler shows no early-Z loss on unrelated materials.
