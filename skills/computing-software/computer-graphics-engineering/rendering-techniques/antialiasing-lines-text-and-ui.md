---
id: computing-software.computer-graphics-engineering.rendering-techniques.antialiasing-lines-text-and-ui
name: antialiasing-lines-text-and-ui
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, antialiasing, line-antialiasing, thick-lines, sdf-text, msdf, ui-rendering, coverage]
level: practitioner
status: docs-checked
description: "Draw wide lines with instanced quads, joins and caps, and render crisp scalable text with multi-channel signed distance fields (msdfgen): median, screen pixel range."
sources: ["https://github.com/Chlumsky/msdfgen", "https://wwwtyro.net/2019/11/18/instanced-lines.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Antialiasing lines, text and UI

## 1. Lines
Native line primitives are unreliable for wide lines. In WebGL the implementation is inconsistent,
so the width you ask for may not be available, and there are no line joins or caps (Terrell, instanced
line rendering). Draw lines as instanced quads instead:
- Instance geometry: two triangles (six vertices) spanning 0..1 along the segment and -0.5..0.5 across
  it. Per instance supply the two endpoints (`pointA`, `pointB`) with an attribute divisor of 1.
- Vertex shader: `xBasis = pointB - pointA`, `yBasis = normalize(vec2(-xBasis.y, xBasis.x))`, then
  `point = pointA + xBasis * position.x + yBasis * width * position.y`. You now control the width.
- A line strip of N vertices has N - 1 segments; independent segments (GL_LINES style) have N / 2.
  One vertex buffer can serve both by changing the attribute offset and stride.
- Joins (miter, round, bevel) and caps (butt, round, square): butt caps come free from the quad ends.
  Round joins can be a circle instance (triangle fan) placed at each interior vertex. A miter join
  needs three consecutive points (previous, current, next) to compute the miter vector.
- Draw segments, joins and caps as separate instanced draws sharing one buffer, or write a
  purpose-built shader to reduce draw calls.
The fetched page does not cover antialiasing the quad edges; derive coverage from the distance across
the line in the fragment shader and check the result visually.

## 2. Text with multi-channel signed distance fields
`msdfgen` generates multi-channel signed distance fields (MSDF) from glyph outlines; its
`msdf-atlas-gen` companion builds whole font atlases. Modes: `sdf` (monochrome true SDF), `psdf`
(perpendicular), `msdf` (default) and `mtsdf` (MSDF plus a true SDF in alpha). `-pxrange` sets the
width of the distance range in distance-field pixels.

Using an MSDF in a fragment shader is the usual SDF lookup plus a median of the three channels:
```glsl
float median(float r, float g, float b) { return max(min(r, g), min(max(r, g), b)); }
vec3 msd = texture(msdf, texCoord).rgb;
float sd = median(msd.r, msd.g, msd.b);
float screenPxDistance = screenPxRange() * (sd - 0.5);
float opacity = clamp(screenPxDistance + 0.5, 0.0, 1.0);
```
- `screenPxRange()` is the distance field range in output screen pixels. Example from the README: pixel
  range 2, a 32x32 field drawn on a 72x72 pixel quad gives 72 / 32 * 2 = 4.5. In 2D a precomputed
  uniform is enough; in 3D perspective compute it from fragment derivatives.
- `screenPxRange()` must never be lower than 1. Below 2, antialiasing will probably fail: regenerate
  the field with a wider range.
- Read the MSDF channels as linear data, not sRGB, even if the PNG or BMP suggests sRGB.
- Call `simulate8bit` on the field when testing how an 8-bit-per-channel image will render.

## Gotchas
- Verify antialiasing width on screen at several scales; a wrong `screenPxRange()` shows as blur or
  jagged edges.
- Test lines across the widths you need, because native wide-line support varies by platform.

## Checked
2026-11-08. Confirmed against the msdfgen README (generation modes, `-pxrange`, shader median and `screenPxRange` code and 4.5 example, minimum range, linear colour-space note, `simulate8bit`) and the instanced-lines article (native line problems, instance geometry and vertex shader, segment counts, joins and caps strategy, miter needing three points). Removed: claims about Vulkan `wideLines` and core-profile deprecation, `fwidth` shape and UI antialiasing snippets, TAA and gamma advice, the Valve SDF history, FreeType hinting size thresholds (not in the fetched pages). The mattdesl article returned a server error and was dropped.
Method: documentation only; no commands were run.

## Verify
- [ ] Lines of 0.5-10 px width show no stair-stepping or flicker while animating.
- [ ] Text crisp at 0.5x-4x atlas scale with MSDF.
