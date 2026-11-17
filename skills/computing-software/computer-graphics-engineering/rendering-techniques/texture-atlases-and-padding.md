---
id: computing-software.computer-graphics-engineering.rendering-techniques.texture-atlases-and-padding
name: texture-atlases-and-padding
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, texture-atlas, atlas-padding, gutter, uv-packing, sprite-sheets]
level: practitioner
status: draft
description: "Pack textures into atlases without bleeding: gutters per mip level, half-texel insets, derivative-safe sampling, and when texture arrays are the better choice."
sources: ["https://developer.nvidia.com/sites/default/files/akamai/tools/files/Texture_Atlas_Whitepaper.pdf", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Texture atlases and padding

## 1. Why bleeding happens
Bilinear filtering reads neighbours; mip levels average neighbours. A 1-texel gutter at mip 0
becomes 0 texels at mip 1. Rule: **gutter = 2^(number of mips used)** texels, or limit mips.

## 2. Packing rules
- Place sub-textures at power-of-two aligned offsets (each tile on a 2^k grid) so mip boundaries
  line up: a 256 tile at a 256-aligned offset stays a clean 128 tile at mip 1.
- Fill gutters by **edge extrusion** (repeat border texels / dilate), not with a flat colour.
- Inset UVs by half a texel of the smallest used mip for clamp-like behaviour.

## 3. Sampling issues
- Tiling/wrapping inside an atlas tile: `uv = tileOrigin + fract(localUV) * tileSize` causes a
  derivative jump at the wrap; pass derivatives from the unwrapped UV:
  `textureGrad(atlas, uv, dFdx(localUV) * tileSize, dFdy(localUV) * tileSize)`.
- Anisotropic filtering reads further than bilinear; increase gutters or reduce aniso on atlases.

## 4. Alternatives
- **Texture arrays** (`sampler2DArray`, same size and format per layer): no bleeding, full
  wrap modes, own mips. Best when sub-textures share dimensions.
- Bindless textures / descriptor indexing: no atlas needed on modern APIs.
- Atlases still win for sprites, glyphs, lightmaps and decals of mixed sizes.

## Gotchas
- Block-compressed atlases (BC/ASTC): tiles and gutters aligned to 4x4 blocks, or compression
  bleeds colours across tiles.
- Packing tools (TexturePacker, xatlas for UVs) have "extrude" and "padding" options; use both.

## Verify
- [ ] Zoom out to the smallest mip: no colour bleeding between tiles.
