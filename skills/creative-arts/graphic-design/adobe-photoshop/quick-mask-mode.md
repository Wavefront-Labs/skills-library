---
id: creative-arts.graphic-design.adobe-photoshop.quick-mask-mode
name: quick-mask-mode
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-selections, selection-tools, quick-mask, paint-selection, quick-mask-options, gradient-selection, feathered-selection]
level: intro
status: draft
description: "Refine or create selections by painting in Photoshop Quick Mask mode: toggling with Q, mask options, painting with brushes and gradients, and filters on the temporary mask."
sources:
  - https://helpx.adobe.com/photoshop/using/create-temporary-quick-mask.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quick Mask mode

**Goal:** see and paint a selection directly, with full brush control, then return it to a marching-ants selection.

## Use
1. Make a rough selection (or none).
2. Press **Q** (or the button under the colour swatches). Unselected areas show as a red overlay
   (rubylith) by default.
3. Paint with **black** to add overlay (deselect), **white** to remove overlay (select), grey for
   partial selection. Use any brush: hard for hard edges, soft for feathering. X swaps colours.
4. Press **Q** again - the painted mask becomes a selection.
5. Turn it into a layer mask or save it (Select > Save Selection).

## Quick Mask Options (double-click the Quick Mask button)
- **Color Indicates: Masked Areas** (default) or **Selected Areas** - pick the one that reads
  naturally to you, and note it on shared machines.
- Overlay colour and opacity: change red to green/blue when the image is red (skin, products).

## Tricks
- Draw a **gradient** in Quick Mask to make a graduated selection (e.g. fade a sky adjustment).
- Run filters on the quick mask: Gaussian Blur to feather, Filter > Pixelate or Brush Strokes for
  rough edges, Minimum/Maximum to shrink/grow.
- Combine with the Lasso: lasso an area in Quick Mask, fill with black/white (Alt/Option+Backspace).

## Quick Mask vs layer mask
Quick Mask is temporary and produces a selection; a layer mask is permanent and non-destructive.
For final work, convert to a layer mask and refine there (mask Properties, see mask density skill).

## Gotchas
- Painting with the wrong mode indicator inverted is the classic mistake - check the option.
- Quick Mask is a temporary channel; saving the document while in Quick Mask stores it as a
  channel, which can confuse others.

## Verify
- [ ] Exiting Quick Mask gives the expected marching ants; overlay matched the intended area.
- [ ] Final selection stored as a layer mask.
