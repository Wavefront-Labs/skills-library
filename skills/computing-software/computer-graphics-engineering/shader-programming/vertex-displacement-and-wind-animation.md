---
id: computing-software.computer-graphics-engineering.shader-programming.vertex-displacement-and-wind-animation
name: vertex-displacement-and-wind-animation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, vertex-displacement, wind-animation, foliage-animation, vertex-shader]
level: practitioner
status: draft
description: "Animate geometry in vertex shaders: displacement maps, wind sway for grass/trees with vertex colours as weights, normals after displacement, and bounds."
sources: ["https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis", "https://www.khronos.org/opengl/wiki/Vertex_Shader"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vertex displacement and wind animation

## 1. Wind sway (foliage)
```glsl
uniform float uTime; uniform vec3 uWindDir; uniform float uWindStrength;
in vec4 aColor;                 // r = bend weight (0 at root, 1 at tip), g = phase offset
void main() {
  vec3 p = aPosition;
  vec3 world = (uModel * vec4(p, 1.0)).xyz;
  float phase = dot(world.xz, vec2(0.15)) + aColor.g * 6.28;      // per-plant offset
  float sway = sin(uTime * 1.7 + phase) * 0.6 + sin(uTime * 3.9 + phase * 1.3) * 0.25;
  world += uWindDir * sway * uWindStrength * aColor.r * aColor.r; // quadratic: tips move most
  gl_Position = uViewProj * vec4(world, 1.0);
}
```
Crysis-style: main bending (whole plant, based on height), detail bending (leaf flutter from
vertex colour channels), gusts from a scrolling noise texture sampled at world position.

## 2. Displacement maps
```glsl
float h = textureLod(uHeight, aUV, 0.0).r;      // explicit LOD in vertex shaders
vec3 p = aPosition + aNormal * (h - 0.5) * uScale;
```
Needs enough vertices (tessellation or dense mesh). Recompute normals: sample neighbours with
finite differences, or bake a matching normal map.

## 3. Things to keep in sync
- Use the same displacement in shadow, depth prepass and motion-vector passes (previous-frame
  time for motion vectors, or TAA ghosts).
- Expand bounding volumes by max displacement so culling does not pop.

## Gotchas
- Pivot matters: bending around the object origin needs the origin at the root.
- Large sway on low-poly trunks stretches visibly; keep trunk weight near 0.
- Animating in object space with scaled instances changes amplitude; work in world space.

## Verify
- [ ] Shadows sway with geometry; no TAA smearing; no culling pops at screen edges.
