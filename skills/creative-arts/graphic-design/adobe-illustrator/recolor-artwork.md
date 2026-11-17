---
id: creative-arts.graphic-design.adobe-illustrator.recolor-artwork
name: recolor-artwork
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-color, illustrator-swatches, recolor-artwork, colour-variations, color-harmony, generative-recolor, assign-colors, reduce-colours, colourways]
level: practitioner
status: draft
description: "Recolour Illustrator artwork systematically with Recolor Artwork: colour wheel, Assign table, mapping to brand colour groups, reducing to one ink, colourways."
sources:
  - https://helpx.adobe.com/illustrator/using/recolor-artwork.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recolor Artwork

**Goal:** apply a new palette to complex artwork (illustrations, patterns, icon sets) in minutes, mapping colours deliberately.

## Open it
Select the artwork, then **Edit > Edit Colors > Recolor Artwork** (or the Recolor button in the
Properties panel). The simple panel shows a colour wheel with all colours in the art; click **Advanced
Options** for the classic dialog.

## Simple panel
- **Color wheel:** drag the main handle to rotate all hues together (harmony link on), or unlink to move one colour.
- **Prominent colors** bar: drag dividers to change how much each colour is used; click a swatch to edit.
- **Color Library**: pick a colour group or library to map onto.
- **Generative Recolor** (Firefly, recent versions): describe a palette in words to get variations - check results for contrast and brand fit.

## Advanced: Assign tab
- **Current Colors** (left) -> **New** (right). Each row maps one or more current colours to one new colour.
- Drag current colours between rows to merge them; the arrow toggles a row on/off.
- **Colors:** set the number (e.g. 3) to reduce automatically; **Recolor method**
  (Exact, Preserve Tints, Scale Tints, Tints and Shades, Hue Shift) for how shades of a colour are mapped.
- Choose a **colour group** from the Color Groups list (e.g. your brand group) to use as targets.
- **Recolor Art** checkbox to preview; **Save** a new colour group from the result.

## Common jobs
- **Brand colourway:** select art, choose brand colour group, map each row; Preserve Tints keeps shading.
- **One-colour version** for screen printing or embossing: Colors = 1, Recolor method Scale Tints,
  target a spot swatch - shading becomes tints of one ink.
- **Pattern colourways:** recolour a pattern swatch (select an object filled with it) to produce
  variations; save each as a new swatch.

## Gotchas
- Gradients, meshes and symbols are included; raster images are not.
- Black and white are excluded by default in some modes (Preserve options) - check when they should change.
- Global swatches get remapped to non-global values unless you target swatches; re-link afterwards if needed.

## Verify
- [ ] Every new colour comes from the intended palette (sample-check with Select > Same > Fill Color).
- [ ] Contrast and hierarchy still read (view in greyscale: Edit > Edit Colors > Convert to Grayscale on a copy).
