---
id: computing-software.computer-graphics-engineering.shader-programming.edge-detection-outline-shader
name: edge-detection-outline-shader
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, edge-detection-outline, outline-shader, sobel, depth-normal-edges, depth-normal-outlines]
level: practitioner
status: draft
description: "Draw screen-space outlines from depth, normal and object-ID edges (Sobel/Roberts), with thresholds that survive distance, plus a jump-flood option for thick outlines."
sources: ["https://roystan.net/articles/outline-shader/", "https://bgolus.medium.com/the-quest-for-very-wide-outlines-ba82ed442cd9", "https://en.wikipedia.org/wiki/Sobel_operator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edge-detection outlines

## 1. Inputs
Depth (linear), view-space normals, and optionally an object/material ID buffer. Each catches
different edges: silhouettes (depth), creases (normals), touching objects (ID).

## 2. Roberts cross on depth and normals
```glsl
float d0 = linDepth(uv), d1 = linDepth(uv + vec2(px.x, px.y)),
      d2 = linDepth(uv + vec2(px.x, 0)), d3 = linDepth(uv + vec2(0, px.y));
float dEdge = sqrt(pow(d1 - d0, 2.0) + pow(d3 - d2, 2.0)) / d0;   // relative: same at all distances
vec3 n0 = N(uv), n1 = N(uv + px), n2 = N(uv + vec2(px.x, 0)), n3 = N(uv + vec2(0, px.y));
float nEdge = sqrt(dot(n1 - n0, n1 - n0) + dot(n3 - n2, n3 - n2));
// grazing angles: raise depth threshold where view and normal nearly perpendicular
float NdotV = 1.0 - dot(n0, -viewDir);
float dThresh = mix(0.02, 0.2, smoothstep(0.5, 1.0, NdotV));
float edge = max(step(dThresh, dEdge), step(0.4, nEdge));
color = mix(color, outlineColor, edge);
```
Sobel (3x3) is smoother but 9 taps per buffer.

## 3. Thickness
Outline width = sample offset in pixels; >2 px from offsets creates gaps. For wide, even
outlines around selected objects use a **jump flood** on a mask (log2(width) passes) and
threshold the distance.

## Gotchas
- Absolute depth thresholds miss far edges and over-detect near; normalise by depth.
- Flat floors at grazing angles produce false edges; the NdotV term fixes most.
- With TAA, run outlines after TAA or jitter-compensate, or they shimmer.
- Alternative for per-object outlines: inverted hull (see inverted-hull-outlines).

## Verify
- [ ] Consistent line weight near and far; no lines on flat floors.
