---
id: computing-software.computer-graphics-engineering.shader-programming.false-colour-debug-visualisation
name: false-colour-debug-visualisation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, debug-visualization, false-color, heatmap, debug-views]
level: practitioner
status: draft
description: "Add false-colour debug views to a renderer: normals, UVs, mip level, overdraw, NaN highlight, light counts and heatmaps with a perceptual colour ramp."
sources: ["https://www.shadertoy.com/view/WlfXRN", "https://renderdoc.org/docs/window/texture_viewer.html", "https://docs.unrealengine.com/5.3/en-US/viewport-modes-in-unreal-engine/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# False-colour debug visualisation

## 1. A debug-view switch
One uniform `uDebugView` in the main shaders (or a final pass reading the G-buffer) selects:
```glsl
if (uDebugView == 1) out = vec4(N * 0.5 + 0.5, 1);                 // world normals
if (uDebugView == 2) out = vec4(fract(uv), 0, 1);                   // UVs (tiling visible)
if (uDebugView == 3) out = vec4(vec3(roughness), 1);
if (uDebugView == 4) out = vec4(turbo(float(lightCount) / 32.0), 1);  // light cull heatmap
if (uDebugView == 5 && any(isnan(c) || isinf(c))) out = vec4(1, 0, 1, 1);  // NaN magenta
```

## 2. Use a perceptual ramp
Turbo or viridis instead of a rainbow (HSV) ramp; rainbows invent false boundaries.
```glsl
vec3 turbo(float x) {   // Google's polynomial approximation
  const vec4 kR = vec4(0.13572138, 4.61539260, -42.66032258, 132.13108234);
  const vec4 kG = vec4(0.09140261, 2.19418839, 4.84296658, -14.18503333);
  const vec4 kB = vec4(0.10667330, 12.64194608, -60.58204836, 110.36276771);
  const vec2 kR2 = vec2(-152.94239396, 59.28637943), kG2 = vec2(4.27729857, 2.82956604), kB2 = vec2(-89.90310912, 27.34824973);
  x = clamp(x, 0.0, 1.0); vec4 v4 = vec4(1.0, x, x*x, x*x*x); vec2 v2 = v4.zw * v4.z;
  return vec3(dot(v4, kR) + dot(v2, kR2), dot(v4, kG) + dot(v2, kG2), dot(v4, kB) + dot(v2, kB2));
}
```
Always show a legend with the scale.

## 3. Standard views worth having
- Mip level: `log2(max(length(dFdx(uv*texSize)), length(dFdy(uv*texSize))))` mapped to colours.
- Overdraw: additive blend of a constant (e.g. 0.1) with depth test off.
- Quad overdraw / triangle density, shader complexity (instruction count per material),
  motion vectors (direction as hue), cascade index for shadows.

## Gotchas
- Write debug output before tone mapping is skipped: bypass tone mapping/TAA for debug views.
- sRGB targets re-encode values: normals look washed out; compare in a UNORM view or RenderDoc.

## Verify
- [ ] Each view toggles live; NaN view catches an injected NaN.
