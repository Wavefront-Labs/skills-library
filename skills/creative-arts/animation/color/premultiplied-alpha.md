---
id: creative-arts.animation.color.premultiplied-alpha
name: premultiplied-alpha
category: creative-arts
field: animation
product: color
tags: [premultiplied-alpha, scene-linear, linear-workflow, straight-alpha, unpremult, over-operation, dark-fringes, halos, compositing, png-alpha]
level: advanced
status: draft
description: "Handle premultiplied vs straight alpha correctly through render, comp, grade and export: when to unpremultiply, and fixing dark fringes and halos."
sources:
  - https://openexr.com/en/latest/TechnicalIntroduction.html#premultiplied-vs-un-premultiplied-color-channels
  - https://www.w3.org/TR/PNG/#6AlphaRepresentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Premultiplied alpha

**Goal:** clean edges on every layered element. Premultiplied ("associated") colour has RGB
already multiplied by alpha; straight ("unassociated") stores colour independent of alpha.

## Conventions by format

| Format | Convention |
|---|---|
| OpenEXR | premultiplied |
| Render engines' beauty | premultiplied |
| PNG | straight (by spec) |
| TIFF | either; flagged by ExtraSamples tag |
| ProRes 4444 | usually straight in Apple/Adobe tools; check the app's "interpret" setting |

## Rules

1. The **over** operation `A + B*(1-a)` expects premultiplied A. Merge premultiplied images.
2. **Colour corrections** that are not linear multiplies (gamma, curves, saturation, grades) must
   be applied to unpremultiplied colour: unpremult, grade, premult. Otherwise semi-transparent edge
   pixels get graded as if they were darker colours.
3. Blurs and transforms work on premultiplied images (filtering straight colour bleeds the
   background colour of transparent pixels into the edge).
4. Convert once at the boundary: when writing PNG, unpremultiply; when reading PNG into a linear
   comp, premultiply.

## Symptoms

| Symptom | Cause |
|---|---|
| dark fringe around element | premultiplied image treated as straight (double premult) |
| bright/white halo | straight image treated as premultiplied, or grading premult colour |
| edge colour from the BG (green spill from transparent pixels) | filtering straight colour |

## Nuke / Blender / AE specifics

- Nuke: Grade/ColorCorrect have an `(un)premult by` alpha option; Read node `premultiplied` checkbox
  for straight sources.
- Blender compositor: Alpha Convert node; "Convert Premultiplied" in Alpha Over.
- After Effects: Interpret Footage, Alpha: Straight vs Premultiplied (matted with colour).

## Verify

Place the element over pure white and pure black at 400%: no dark ring on white, no light ring on
black, and edges hold the same width on both.
