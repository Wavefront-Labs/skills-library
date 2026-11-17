---
id: creative-arts.graphic-design.adobe-photoshop.dodge-and-burn
name: dodge-and-burn
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photo-retouching, image-repair, dodge-and-burn, curves-dodge-burn, soft-light-layer, helper-layers, luminosity-check, contouring, product-retouching]
level: advanced
status: draft
description: "Dodge and burn non-destructively for skin, products and composites: curves-based and soft-light grey layers, helper/check layers, low-flow brushing, and macro vs micro D&B."
sources:
  - https://helpx.adobe.com/photoshop/using/tool-techniques/dodge-tool.html
  - https://helpx.adobe.com/photoshop/using/curves-adjustment.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dodge and burn

**Goal:** shape light and remove unevenness by lightening and darkening locally, fully reversible.

## Setup options
**A. Two curves (preferred for control)**
1. Curves adjustment layer named `Dodge`: pull the midpoint up (brighter). Fill its mask black (Ctrl/Cmd+I).
2. Curves layer `Burn`: pull midpoint down. Mask black.
3. Set both to **Luminosity** blend mode if colour shifts appear (burning increases saturation).
4. Paint white on the masks with a soft brush, **flow 1-5%**, opacity 100%, building up.

**B. Soft Light grey layer (quick)**
New layer, Mode **Soft Light**, tick "Fill with Soft-Light-neutral color (50% gray)". Paint with
white/black at low flow, or use the Dodge/Burn tools (Range: Midtones, Exposure 5-10%) on it.

## Helper (check) layers
Group of view-only adjustments at the top, toggled on while working:
- Black & White adjustment (or Solid Color black in Color mode) - shows luminance only, so you see
  blotches as tone, not colour.
- Curves with strong contrast (S-curve) to exaggerate unevenness.
Turn the group off before saving outputs.

## Micro vs macro
- **Micro D&B:** zoom 100-200%, a brush the size of the blemish; lighten small dark spots and
  darken small light spots until skin (or a product surface) is even. Slow but the most natural result.
- **Macro D&B:** large soft brush at 25-50% zoom; enhance form - burn under cheekbones and along
  edges, dodge highlights on nose bridge, cheekbones; on products, enhance reflections and edges.
  Follow the existing light direction.

## Gotchas
- Too much flow leaves visible patches; keep flow very low and build.
- Burning shadows can oversaturate; Luminosity mode or a Hue/Saturation layer fixes it.
- Not a substitute for good lighting - big shape changes look painted.

## Verify
- [ ] With helper layers on, tonal unevenness reduced without new blotches.
- [ ] Toggling the D&B group shows refinement, not a different face/product.
