---
id: computing-software.computer-graphics-engineering.graphics-math.gpu-vector-path-rendering
name: gpu-vector-path-rendering
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, curves-surfaces, path-rendering, vector-graphics, loop-blinn, stencil-then-cover, font-rendering]
level: advanced
status: draft
description: "Render vector paths (SVG, fonts, UI) on the GPU: stencil-then-cover, Loop-Blinn implicit curves, analytic coverage AA, compute rasterisers (Vello), and fill rules."
sources: ["https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-25-rendering-vector-art-gpu", "https://developer.nvidia.com/gpu-accelerated-path-rendering", "https://github.com/linebender/vello", "https://www.w3.org/TR/SVG2/painting.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU vector path rendering

## Approaches
| Technique | Idea | Notes |
|---|---|---|
| CPU flatten + triangulate | Flatten curves, triangulate (earcut/libtess) | Simple, re-tessellate on zoom, no curve AA |
| Stencil-then-cover | Fan triangles into stencil incr/decr (winding), then cover pass tests stencil | NV_path_rendering, Skia; handles any fill rule; AA via MSAA |
| Loop-Blinn | Curve triangles with implicit-function fragment test (`u^2 - v < 0` for quadratics) | Resolution independent; cubics need classification and splitting |
| Analytic coverage / SDF | Compute coverage per pixel from curve distances | Slug (fonts), signed distance fields (msdfgen) |
| Compute rasteriser | Bin segments to tiles, prefix-sum winding per tile | Vello, Pathfinder, Rive; scales to complex scenes |

## Loop-Blinn quadratic
Assign texture coordinates (0,0), (0.5,0), (1,1) to the control triangle; in the fragment shader
discard where `u*u - v > 0` (flip sign for the other side). AA: use the gradient of the implicit
function to compute signed pixel distance, `alpha = clamp(0.5 - f / length(fwidth-based gradient), 0, 1)`.

## Fill rules
Non-zero (SVG default) vs even-odd: stencil-then-cover uses increment/decrement wrap (non-zero) or
invert (even-odd). Compute rasterisers accumulate signed winding per pixel and apply the rule.

## Anti-aliasing quality
MSAA 4x/8x gives visible stepping on near-horizontal edges of text; analytic coverage (exact area of
the path within the pixel) gives the best quality. Do coverage blending in **linear** space with
gamma-correct text blending caveats (fonts are often tuned for sRGB blending).

## Strokes
Convert strokes to fills (offset curves, joins, caps, dashes) on CPU, or render strokes as distance
to curve segments in the shader (thick quadratic distance needs a cubic solve).

## Verify
Render the SVG test suite (resvg tests) and compare against a reference rasteriser (resvg/Skia CPU)
with a pixel diff tolerance.
