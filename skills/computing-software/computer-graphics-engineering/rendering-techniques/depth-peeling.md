---
id: computing-software.computer-graphics-engineering.rendering-techniques.depth-peeling
name: depth-peeling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, depth-peeling, dual-depth-peeling, order-independent-transparency]
level: advanced
status: docs-checked
description: "Implement exact order-independent transparency with depth peeling and dual depth peeling: passes, depth textures, under-blending equations, and layer count."
sources: ["https://developer.download.nvidia.com/assets/gamedev/docs/OrderIndependentTransparency.pdf", "https://developer.download.nvidia.com/SDK/10/opengl/src/dual_depth_peeling/doc/DualDepthPeeling.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth peeling

**Goal:** correct per-pixel depth-ordered transparency, with geometry rendered in any order.
Depth peeling guarantees correct fragment ordering, at the cost of one geometry pass per layer
(NVIDIA Dual Depth Peeling, 2008).

## 1. Front-to-back peeling
Pass 0 renders the scene normally with a depth test, which returns the nearest fragments to the
eye. In each later pass the depth buffer from the previous pass is bound to the fragment shader;
if the fragment depth is less than or equal to the depth stored for that pixel, the fragment is
discarded, so the depth test returns the next layer underneath. Swap the source and destination
depth buffers every pass (ping-pong) to avoid read-modify-write hazards.
```glsl
uniform sampler2D uPrevDepth;   // depth written by the previous pass
void main() {
  float prev = texelFetch(uPrevDepth, ivec2(gl_FragCoord.xy), 0).r;
  if (gl_FragCoord.z <= prev) discard;
  ...
}
```
The NVIDIA sample uses a 32-bit depth buffer (earlier hardware offered 24 bits at most); because
`gl_FragCoord.z` and the stored depth are both 32-bit floats, they can be compared without a bias.

## 2. Compositing front to back ("under" blending)
To composite layers as they are peeled front to back, blend with Adst initialised to 1.0:
```
Cdst = Adst * (Asrc * Csrc) + Cdst
Adst = (1 - Asrc) * Adst
```
Do it by premultiplying Csrc by Asrc in the shader and using separate RGB and alpha blend
equations:
```c
glEnable(GL_BLEND);
glBlendEquation(GL_FUNC_ADD);
glBlendFuncSeparate(GL_DST_ALPHA, GL_ONE, GL_ZERO, GL_ONE_MINUS_SRC_ALPHA);
```
Finally composite with the background colour: `Cdst = Adst * Cbg + Cdst`. The older NVIDIA
presentation instead captures each pass's RGBA as a layer and blends all layers back to front at
the end, where opaque fragments completely overwrite earlier transparent ones.

## 3. Dual depth peeling
Peels one layer from the front and one from the back each pass, so depth complexity N needs
N/2+1 geometry passes instead of N (the extra pass is because it works on two consecutive layers
at a time). It can speed up geometry-bound applications by about 2x.
- Min-max depth buffer: an RG32F colour texture with MAX blending, writing `float2(-depth, depth)`,
  so the hardware depth test is turned off and blending does the depth comparison.
- Three render targets via an FBO: RT0 the min-max depth buffer, RT1 the front fragments (blended
  under) and RT2 the back fragments (blended over). The two results are then blended together
  with under blending.
- When the front and back fronts meet, the algorithm processes the fragment as a front fragment.
- With N = 2 it extracts the front and the back layer, which suits the look of convex objects.
  Since dual peeling uses no depth test, it disables the hardware's early-z optimisation.
  Exiting early still captures the foremost layers.

## 4. Stopping
The NVIDIA sample uses occlusion queries by default to stop when a pass produces no more
fragments; with them off it uses a fixed layer count. The older presentation notes that all layers
must be peeled to avoid blending artifacts.

## Verify
- [ ] Intersecting transparent objects render correctly from any view, matching a reference
      sorted by depth.
- [ ] Pass count matches N (front-to-back) or about N/2+1 (dual) for a scene of known depth complexity.

## Checked
2026-11-09. Read: NVIDIA "Dual Depth Peeling" (Feb 2008: depth comparison, under-blending
equations and blend functions, RG32F min-max buffer, render targets, N/2+1 passes, occlusion
queries in the sample) and the NVIDIA Order Independent Transparency presentation (ping-pong
depth buffers, per-pass layer capture, back-to-front composite). Corrected: the under-blend
formula (now the paper's separate colour and alpha equations) and the 1e-7 depth epsilon (the
paper compares 32-bit floats without bias). Removed: the 4 to 8 layer cap, the WBOIT hybrid,
the coplanar-fragment epsilon advice, MSAA per-sample peeling and the geometry-cost remark.
Method: docs-checked 2026-11-09 against the NVIDIA Dual Depth Peeling paper and the NVIDIA OIT presentation.
