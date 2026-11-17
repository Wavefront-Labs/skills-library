---
id: computing-software.computer-graphics-engineering.shader-programming.uv-scrolling-and-flow-maps
name: uv-scrolling-and-flow-maps
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, flow-map, uv-scrolling, water-shader, lava, texture-animation, valve-flow]
level: practitioner
status: draft
description: "Animate surfaces with UV scrolling and flow maps: dual-phase flow to hide resets, encoding flow textures, normal-map flow for water/lava, and avoiding stretching."
sources: ["https://alex.vlachos.com/graphics/Vlachos-SIGGRAPH10-WaterFlow.pdf", "https://catlikecoding.com/unity/tutorials/flow/texture-distortion/", "https://docs.unrealengine.com/5.3/en-US/panner-material-expression-in-unreal-engine/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UV scrolling and flow maps

## 1. Scrolling
```glsl
vec2 uv1 = uv + scrollDir1 * time;
vec2 uv2 = uv * 1.37 + scrollDir2 * time * 0.7;   // second layer, different scale/direction
vec3 n = blendNormals(sampleN(uv1), sampleN(uv2));
```
Two layers in different directions break the obvious conveyor-belt look. Wrap time
(`mod(time, period)`) to avoid precision loss after hours of uptime.

## 2. Flow maps (Vlachos, Valve 2010)
A flow texture stores a 2D direction per texel (RG, 0.5 = zero). Offsetting UVs by
`flow * time` distorts indefinitely, so reset periodically and crossfade two phases:
```glsl
vec2 flow = texture(flowMap, uv).rg * 2.0 - 1.0;
flow *= flowStrength;
float t0 = fract(time * speed);
float t1 = fract(time * speed + 0.5);
vec3 a = texture(tex, uv - flow * t0).rgb;
vec3 b = texture(tex, uv - flow * t1 + 0.5).rgb;     // offset hides synchronised pulsing
float w = abs(t0 - 0.5) * 2.0;                       // weight 0 at a's reset
vec3 col = mix(a, b, w);
```
- Add a noise texture to the phase (`time + noise(uv)`) so resets are not visible as a global pulse.
- Normal maps: flow the normal map the same way; for strong distortion rotate normals by flow
  direction (Catlike Coding "directional flow").

## 3. Authoring flow
- Paint in FlowMap Painter / Houdini (from a fluid sim or curve) / Substance; or bake from a
  spline (river) tangent.
- Store linear (not sRGB) RG8; BC5 compression works well.

## Gotchas
- Speed variations stretch textures; clamp flow strength and use a smaller phase period where
  flow is strong.
- Mip selection with offset UVs is fine (derivatives continuous) unless the flow map itself is low-res
  and point sampled; use bilinear.
- Sharp flow discontinuities (around rocks) tear the texture; blur the flow map slightly.

## Verify
- [ ] No visible periodic pulse or reset at any point.
- [ ] Texture detail moves along painted directions at the authored speed.
