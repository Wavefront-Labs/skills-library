---
id: creative-arts.graphic-design.adobe-photoshop.text-effects-and-image-in-text
name: text-effects-and-image-in-text
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-type, image-in-text, clipping-mask, layer-styles, text-effects]
level: practitioner
status: draft
description: "Create image-filled type and stylised text effects in Photoshop with clipping masks, layer styles and smart objects while keeping text editable."
sources:
  - https://helpx.adobe.com/photoshop/using/revealing-layers-clipping-masks.html
  - https://helpx.adobe.com/photoshop/using/layer-effects-styles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text effects and image in text

**Goal:** headline type filled with a photo or texture, plus effects, all editable.

## Image inside type (clipping mask)
1. Set the type: heavy weights (Black, Ultra) at large size show the image best.
2. Place the image as a smart object **directly above** the type layer.
3. Alt/Opt-click the line between them in Layers (or Ctrl/Cmd+Alt+G) = **clipping mask**.
   The image shows only within the letters; arrow indent marks the clipped layer.
4. Move/scale the image independently; edit text freely.
5. Several layers can clip to one base (image + adjustment layer + texture).

## Layer styles for effects
- Double-click the type layer: Stroke (outside, for knockout outlines), Drop Shadow, Inner
  Shadow, Bevel & Emboss (sparingly), Gradient/Pattern Overlay.
- Effects on the base type layer apply to the clipped group's shape.
- Save as a style in the Styles panel for reuse; Layer > Layer Style > Scale Effects when resizing.

## Knockout alternative
- Group type and image, use Advanced Blending > Knockout: Shallow to punch type through layers.

## Gotchas
- Fill opacity 0% + stroke style = outline type that keeps effects.
- Large text effects export to PDF as rasters; for print headline type, check that the vector
  outline survives (Save As PDF with "Preserve Photoshop Editing Capabilities" off for smaller files).
- Ensure font licence allows use in images if the result is sold as a template.

## Verify
- [ ] Text remains editable and spell-checked.
- [ ] Image framing still works after text edits.
