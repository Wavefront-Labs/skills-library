---
id: creative-arts.animation.color.creative-look-luts
name: creative-look-luts
category: creative-arts
field: animation
product: color
tags: [creative-lut, look-lut, show-lut, lmt, lut, colour-grading, resolve, ocio-looks, look-and-matching]
level: practitioner
status: draft
description: "Design and apply a creative look LUT for an animated show: build it from a grade, place it after correction, keep a technical/creative split and avoid LUT clipping."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://opencolorio.readthedocs.io/en/latest/guides/authoring/looks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Creative look LUTs

**Goal:** a consistent show look that lighting, comp and grading all see, applied as one transform.

## Creative vs technical LUT

- **Technical LUT:** converts colour spaces (log to Rec.709, ACES output). Exact and reversible in intent.
- **Creative LUT:** a look (filmic crossover, muted greens, warm highlights). It should operate in the working
  space (scene-referred, e.g. ACEScct) **before** the output transform, so it survives multiple deliverables (SDR,
  HDR). ACES calls this an LMT.

## Building one

1. Grade a set of hero frames (day, night, interior, character close-ups) with only global operations: curves,
   hue-vs curves, saturation, split toning. No windows or qualifiers; a LUT cannot track them.
2. Resolve: right-click the clip thumbnail > *Generate LUT* > 33 or 65 point cube. Generate from the look nodes
   only, with the input and output in the same working space.
3. Name it with show, version and spaces: `show_look_v003_ACEScct_to_ACEScct.cube`.
4. Distribute via OCIO looks (see `creative-arts.animation.color.ocio-looks-per-shot`) so DCC viewers preview it.

## Applying

Place it after balance/contrast, before the output transform (node 09 in
`creative-arts.animation.color.grade-node-tree-structure`). Use the node's *Key Output Gain* to dial the strength.

## Gotchas

- 3D LUTs clip input outside 0-1; a LUT built in a log space handles HDR range far better than one in linear.
- A 17-point LUT bands on smooth gradients; use 33 or 65 for grading.
- Stylized cel looks often rely on exact palette colours; check the master palette swatches through the LUT
  (`creative-arts.animation.art-direction.master-palette-specification`) and keep brand/character key colours
  within a small delta.

## Verify

A reference chart and palette swatch frame through the LUT match the approved look frame; SDR and HDR outputs both
show the same look intent.
