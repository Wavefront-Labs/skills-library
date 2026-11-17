---
id: computing-software.computer-graphics-engineering.rendering-techniques.premultiplied-alpha-compositing
name: premultiplied-alpha-compositing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, alpha-blending, premultiplied-alpha, straight-alpha, dark-fringes, over-operator, mipmap-alpha, additive-blending]
level: practitioner
status: docs-checked
description: "Use premultiplied alpha throughout a renderer: the over operator and blend state, converting straight-alpha assets, correct filtering and mipmaps without dark halos."
sources: ["https://drafts.csswg.org/compositing-1/", "https://github.com/w3c/PNG-spec", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/framebuffer.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Premultiplied alpha compositing

**Goal:** transparent sprites, UI, particles and render targets that filter, mip and blend
without dark or bright fringes (Porter & Duff 1984).

## 1. Definitions
- **Straight (unassociated)**: colour C, coverage α stored separately; blended as
  `C·α + dst·(1−α)`.
- **Premultiplied (associated)**: stored colour is `C·α`; blended as
  `src + dst·(1−α_src)`.
Blend state for premultiplied "over": `src = ONE, dst = ONE_MINUS_SRC_ALPHA` (for both colour and
alpha). Straight alpha would use `SRC_ALPHA, ONE_MINUS_SRC_ALPHA` for colour.

## 2. Why premultiplied
- **Filtering is correct**: bilinear/mip averaging of premultiplied texels weights colour by
  coverage. With straight alpha, invisible pixels' colours (often black or garbage) bleed into
  edges → dark halos around foliage/UI after mipmapping or scaling.
- **Associative compositing**: layers can be pre-composited into render targets (UI layers,
  offscreen particles) and blended later with the same equation.
- **Additive + alpha in one state**: premultiplied colour with α = 0 adds light (glow,
  fire core) while α > 0 occludes — fire/smoke particles in one draw call without sorting by
  blend mode.

## 3. Converting assets
Premultiply at import/bake time in **linear** space: `rgb_lin *= a`. Do it before generating
mips and before block compression. PNG files are straight alpha by spec (colour values are not premultiplied) — premultiply on load
(or in the pipeline), and mark textures accordingly (`ktx create --premultiply-alpha` premultiplies and sets the flag in the KTX2 metadata).

## 4. Shader output
```glsl
vec4 tex = texture(spriteTex, uv);          // premultiplied asset
fragColor = tex * tint;                      // tint.rgb premultiplied too: tint.rgb *= tint.a
// fading the sprite: multiply ALL channels by fade (not just alpha)
```
Lighting a premultiplied surface: `lit = (albedo_premul * lightTerm)`, alpha unchanged.

## Gotchas
- Mixing conventions (premultiplied texture with straight blend state) → over-dark or
  over-bright edges; one convention per pipeline, enforced in asset metadata.
- Un-premultiplying (dividing by α) for effects loses precision at low α; avoid.
- sRGB: premultiply in linear light; premultiplying sRGB-encoded values gives slightly wrong
  edges.
- WebGL: the context's `premultipliedAlpha` attribute must match what you output.

## Verify
- [ ] Foliage/UI edges free of dark halos at all mip levels and scales.
- [ ] Asset pipeline flags premultiplied textures; lint rejects mismatched blend states.
- [ ] Additive/alpha particle mix renders correctly in one draw.

## Checked

2026-10-26: CSS Compositing and Blending Level 1 (w3c/csswg-drafts compositing-1), PNG specification (w3c/PNG-spec: colour values are not premultiplied), WebGL 1.0 spec (premultipliedAlpha context attribute), KTX-Software ktx create (premultiply-alpha option sets the metadata flag) and Vulkan-Docs framebuffer.adoc (blending of sRGB attachments is done on linearised values), read 2026-10-26. Removed the three.js texture.premultiplyAlpha reference and the book chapter citation, which were not checked. The blend factors follow directly from the premultiplied over equation in the W3C text.

Method: documentation only; no commands were run.
