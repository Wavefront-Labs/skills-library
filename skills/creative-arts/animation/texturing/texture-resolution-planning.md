---
id: creative-arts.animation.texturing.texture-resolution-planning
name: texture-resolution-planning
category: creative-arts
field: animation
product: texturing
tags: [texture-resolution, substance-painter, screen-coverage, memory-budget, 2k-4k, upres, working-resolution, export-size]
level: practitioner
status: draft
description: "Pick working and export texture resolutions per asset from screen coverage and memory budget; paint low, export high in Painter without losing detail."
sources:
  - https://helpx.adobe.com/substance-3d-painter/interface/texture-set/texture-set-settings.html
  - https://helpx.adobe.com/substance-3d-painter/texturing/export/export-settings.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Texture resolution planning

**Goal:** enough pixels that textures hold up in the closest shot, not so many that renders or the
engine drown in memory.

## From screen coverage

Rule: the texture should have at least as many texels across an object as the object covers pixels on
screen at its closest framing.
- A character head filling a 1080p close-up (about 1000 px tall) with the head on half the UV space
  needs about 2K for that set; 4K for UHD or extreme close-ups.
- Background props never closer than 200 px on screen: 512-1K.
Group assets in tiers (hero/secondary/background) with fixed resolutions per tier for the show.

## Memory arithmetic

Uncompressed RGBA 8-bit: 4K = 64 MB, 2K = 16 MB, 1K = 4 MB per map (plus ~33% for mipmaps). Five
maps at 4K = 320+ MB per texture set. For real-time, block compression cuts this 4-8x
(`creative-arts.animation.texturing.texture-compression-formats`).

## Working vs export resolution in Painter

Painter is resolution-independent for procedural layers and fills, so:
- Work at 2K (fast viewport), export at 4K: procedurals, generators and fill layers re-compute at 4K.
- Paint strokes are stored as vectors-plus-brush data and re-render at higher resolution, but bitmap
  imports (photos, decals) cap at their own resolution.
- Bake mesh maps at the export resolution (or higher), not the working resolution, for final exports.

## Gotchas

- Upsizing only at export can reveal filter-size differences: blur/noise scales relative to texture
  size; check stylised details after switching.
- Non-square or non-power-of-two sizes break mip generation in some engines; keep powers of two.
- Very small UV shells in a big texture waste memory as much as oversized textures; fix UV space
  so shells get area in proportion to their screen importance.

## Verify

Render the asset at its closest planned framing at delivery resolution: no visible texel blur or
pixelation; memory per asset fits the show budget sheet.
