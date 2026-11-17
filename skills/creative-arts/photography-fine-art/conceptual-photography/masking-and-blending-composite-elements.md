---
id: creative-arts.photography-fine-art.conceptual-photography.masking-and-blending-composite-elements
name: masking-and-blending-composite-elements
category: creative-arts
field: photography-fine-art
product: conceptual-photography
tags: [conceptual-photography, photo-compositing, compositing-masks, layer-masks, select-and-mask, refine-hair, decontaminate-colors, photoshop]
level: practitioner
status: draft
description: "Mask and blend composite elements in Photoshop: Select Subject, Select and Mask for hair, layer masks, clipping adjustments and edge decontamination."
sources: ["https://helpx.adobe.com/photoshop/using/select-mask.html", "https://helpx.adobe.com/photoshop/using/masking-layers.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Masking and blending composite elements

## Procedure
1. Place each element as a **Smart Object** (File > Place Embedded) for non-destructive scaling.
2. Initial selection: Select > Subject (or Object Selection tool); for sky, Select > Sky.
3. **Select and Mask** workspace:
   - Refine Hair / Refine Edge Brush over hair and fuzzy edges.
   - Smooth 0-5, Feather 0.3-1 px, Contrast low, Shift Edge -5 to -20% to remove halo.
   - **Decontaminate Colors** (output to new layer with mask) removes background colour fringe.
4. Output to Layer Mask. Refine by painting with a soft brush on the mask (black hides, white reveals);
   use low-opacity brush for transitions.
5. Clip adjustment layers (Alt/Option-click between layers) so Curves/Hue affect only that element.
6. Group each element with its mask and adjustments; name layers.

## Edge tips
- Shoot elements on a background similar in tone/colour to the plate for easier hair blending.
- Use a Channel-based mask (copy the highest-contrast channel, Levels to black/white) for trees and hair.
- Inner edge darkening/halo: Layer > Matting > Defringe 1-2 px (on unmasked layers).

## Verify
- [ ] At 200% no halos, fringes or hard cut edges; mask is editable (non-destructive).
