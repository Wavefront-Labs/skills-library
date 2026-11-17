---
id: creative-arts.visual-art.digital-illustration.selections-and-selection-masks
name: selections-and-selection-masks
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-layers, selection-masks, selections, lasso, magic-wand, quick-mask, krita, clip-studio-paint, photoshop, feathering]
level: practitioner
status: draft
description: "Use selections in digital painting: lasso, contiguous and colour selection, adding/subtracting, feathering, saving selections as masks, painting selections directly, and global selection masks."
sources: ["https://docs.krita.org/en/user_manual/selections.html", "https://helpx.adobe.com/photoshop/using/making-selections.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selections and selection masks

**Goal:** constrain painting and adjustments to exact areas, with soft or hard
edges, and store those areas for reuse (Krita Manual, Selections; CSP and Photoshop docs).

## Selection tools
- **Freehand/polygonal lasso**: hand-drawn shapes; hard-edged planes, quick masses.
- **Contiguous (magic wand) / similar colour**: select flats by colour; set
  tolerance/threshold; "sample: all layers" vs current.
- **Rectangle / ellipse**: basics.
- **Select opaque**: Krita: right-click layer > Select Opaque; Photoshop:
  Ctrl/Cmd-click a layer thumbnail; CSP: Selection from layer.
- Modifiers: **Shift** add, **Alt/Option** subtract (Photoshop and Krita; Krita also
  has mode buttons).

## Edges
- Feather (Krita: Select > Feather Selection; Photoshop: Select and Mask / Feather)
  for soft transitions; grow/shrink to tidy edges against line art.
- Anti-aliasing on for smooth edges; off for pixel art.

## Painting a selection
- **Quick Mask (Photoshop: Q)** or **Global Selection Mask** (Krita: Select >
  Show Global Selection Mask) shows the selection as a paintable layer: paint with
  brushes to make complex, soft selections.
- CSP: Quick Mask (Selection > Quick mask).

## Saving
- Krita: convert to a **local selection mask** on a layer (stays attached) or save
  as a layer; Photoshop: Select > Save Selection (alpha channel); CSP: selection
  layers / save selection. Reuse later for the same object.

## Uses
- Paint shadows within a form with a hard edge on one side and soft on the other.
- Apply adjustments (curves, hue) only to one area.
- Make clean shapes for graphic styles; then paint inside freely.

## Gotchas
- Forgetting an active selection: brushes "don't work" outside it.
- Selecting on the wrong layer or sample mode.

## Verify
- [ ] Selections stored for repeated use.
- [ ] Edge quality matches the form (feathered vs crisp).
