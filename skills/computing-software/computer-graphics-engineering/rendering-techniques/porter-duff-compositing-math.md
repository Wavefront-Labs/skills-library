---
id: computing-software.computer-graphics-engineering.rendering-techniques.porter-duff-compositing-math
name: porter-duff-compositing-math
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, porter-duff, alpha-compositing, premultiplied-alpha, blend-state, over-operator]
level: practitioner
status: docs-checked
description: "Apply Porter-Duff compositing algebra: over/in/out/atop/xor with premultiplied alpha, mapping operators to GPU blend states, and avoiding fringe and double-multiplication errors."
sources: ["https://drafts.csswg.org/compositing-1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Porter-Duff compositing math

Porter & Duff (1984) defined compositing operators on premultiplied colours
(`C = colour * alpha`). With source S, destination D:
`result = S * Fa + D * Fb` for both colour and alpha.

## 1. Operators
| Operator | Fa | Fb | GPU blend (premultiplied) |
|---|---|---|---|
| clear | 0 | 0 | ZERO, ZERO |
| source (copy) | 1 | 0 | ONE, ZERO |
| **over** | 1 | 1 - As | ONE, ONE_MINUS_SRC_ALPHA |
| destination over | 1 - Ad | 1 | ONE_MINUS_DST_ALPHA, ONE |
| in | Ad | 0 | DST_ALPHA, ZERO |
| out | 1 - Ad | 0 | ONE_MINUS_DST_ALPHA, ZERO |
| atop | Ad | 1 - As | DST_ALPHA, ONE_MINUS_SRC_ALPHA |
| xor | 1 - Ad | 1 - As | ONE_MINUS_DST_ALPHA, ONE_MINUS_SRC_ALPHA |
| plus (additive) | 1 | 1 | ONE, ONE |

The W3C Compositing and Blending spec defines the same operators through Fa and Fb (clear 0,0; source 1,0; source-over 1,1-as; destination-over 1-ab,1;
source-in ab,0; source-out 1-ab,0; source-atop ab,1-as; xor 1-ab,1-as; lighter 1,1) in addition to its separable and non-separable blend modes.

## 2. Straight vs premultiplied
- Straight alpha "over": `C = Cs * As + Cd * (1 - As)` (blend `SRC_ALPHA, ONE_MINUS_SRC_ALPHA`)
  and alpha must be handled separately: `A = As + Ad * (1 - As)` (use separate alpha blend factors
  `ONE, ONE_MINUS_SRC_ALPHA`).
- Premultiplied makes every operator a simple linear combination, filters correctly (no dark
  fringes when mipmapping/bilinear), and composes associatively (you can pre-composite layers).

## 3. Common errors
- Double premultiplication (asset already premultiplied, shader multiplies again): darkened edges.
- Straight-alpha textures filtered bilinearly bleed black from transparent texels with RGB = 0:
  premultiply at import or dilate colour into transparent areas.
- Writing straight alpha into a render target later composited as premultiplied: halos.
- Destination alpha not tracked (RGB-only target) makes `in/out/atop` meaningless.

## 4. Group transparency
To fade a group of overlapping objects as one: render them opaque into an offscreen RGBA target,
then composite that with "over" at group opacity. Fading each object individually shows overlaps.

## Gotchas
- Blending into a non-sRGB format happens on the stored (encoded) values; with an sRGB attachment format Vulkan linearises the destination before blending and re-encodes the result.
- Additive ("plus") in premultiplied form with alpha = 0 gives pure emission from the same shader.

## Verify
- [ ] Bilinear-magnified premultiplied sprites show no dark outlines.
- [ ] Group fade shows no internal overlaps.

## Checked

2026-10-26: CSS Compositing and Blending Level 1 (w3c/csswg-drafts compositing-1/Overview.bs) and Vulkan-Docs framebuffer.adoc, read 2026-10-26. Confirmed every Fa/Fb pair in the operator table (clear, source, over, destination-over, in, out, atop, xor, plus/lighter) against the W3C text, and the sRGB blending behaviour for Vulkan attachments. The corresponding GPU blend factors follow arithmetically from those pairs.

Method: documentation only; no commands were run.
