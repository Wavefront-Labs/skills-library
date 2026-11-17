---
id: computing-software.computer-graphics-engineering.shader-programming.sdf-2d-shapes-and-antialiasing
name: sdf-2d-shapes-and-antialiasing
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, sdf, sdf-2d, sdf-antialiasing, signed-distance-field, msdf, fwidth, ui-shapes, rounded-rectangle, outlines, procedural-shapes]
level: practitioner
status: docs-checked
description: "Draw resolution-independent 2D shapes, outlines and glyphs with signed distance functions in shaders: core SDF primitives, fwidth-based antialiasing, borders."
sources: ["https://iquilezles.org/articles/distfunctions2d/", "https://thebookofshaders.com/07/", "https://github.com/Chlumsky/msdfgen", "https://iquilezles.org/articles/smin/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# 2D SDF shapes and antialiasing

**Goal:** crisp UI elements, icons, outlines and text at any scale and rotation from a few
lines of shader math.

## 1. Core primitives (distance < 0 inside)
```glsl
float sdCircle(vec2 p, float r) { return length(p) - r; }
float sdRoundBox(vec2 p, vec2 halfSize, float r) {        // rounded rectangle
    vec2 q = abs(p) - halfSize + r;
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}
float sdSegment(vec2 p, vec2 a, vec2 b) {
    vec2 pa = p - a, ba = b - a; float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h);
}
```
IQ's 2D distance functions page has many exact SDFs (circle, rounded box, segment above are taken from it). Combine: union `min(a,b)`,
intersection `max(a,b)`, subtraction `max(a,-b)`, smooth union with `smin`.

## 2. Antialiasing with screen-space derivatives
```glsl
float d = sdRoundBox(p, size, radius);          // p in pixels or any unit
float aa = fwidth(d);                            // distance change per pixel
float fill = 1.0 - smoothstep(-aa, aa, d);       // ~1-pixel soft edge at any zoom
```

## 3. Borders, glows, shadows
```glsl
float border = 1.0 - smoothstep(-aa, aa, abs(d) - thickness * 0.5);   // stroke centred on edge
float glow   = exp(-max(d, 0.0) * falloff);                            // outer glow
float shadow = 1.0 - smoothstep(-blur, blur, sdRoundBox(p - offset, size, radius));
vec4 col = mix(bg, fillColor, fill); col = mix(col, borderColor, border);
```
Composite in premultiplied alpha to avoid dark fringes.

## 4. SDF and MSDF text/icons
- **MSDF** (multi-channel, msdfgen): sample the texture and take `median(r,g,b)` to get the signed distance, then use it like a single-channel one.
- `screenPxRange` is the distance-field range in output screen pixels (pixel range x on-screen size / texture size; msdfgen's example: range 2, 32x32 field drawn at 72x72 gives 4.5). It must never be lower than 1; below 2 the antialiasing will probably fail, so regenerate with a wider range.

## Gotchas
- Not every combination is an exact SDF: `max`-based subtraction and smooth unions give
  bounds, which is fine for fill AA but distorts thick outlines/glows.

## Checked
2026-11-01. Confirmed: circle, rounded-box and segment SDFs (iquilezles.org distfunctions2d), smoothstep edges (Book of Shaders ch. 7), median-of-channels and screenPxRange rules (msdfgen README), subtraction/smooth-union as bounds (Quilez distfunctions). Removed: pixel-space aa constant, single-channel corner claim, msdf-atlas-gen mention, fwidth control-flow and quad-flicker gotchas (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Shapes stay sharp and 1-px-antialiased from 0.25x to 8x zoom and under rotation.
- [ ] MSDF text corners sharp at large sizes; no artefacts at small sizes.
- [ ] Premultiplied compositing: no dark halos over light backgrounds.
