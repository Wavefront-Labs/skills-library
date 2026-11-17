---
id: creative-arts.graphic-design.adobe-photoshop.content-aware-fill-workspace
name: content-aware-fill-workspace
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photo-retouching, image-repair, content-aware-fill, sampling-area, output-to-new-layer, object-removal, content-aware-move, fill-dialog]
level: practitioner
status: draft
description: "Remove larger objects with the Photoshop Content-Aware Fill workspace: padded selections, sampling area control, fill settings and output to a new layer."
sources:
  - https://helpx.adobe.com/photoshop/using/content-aware-fill.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Content-Aware Fill workspace

**Goal:** remove a large object (a person, a car, a sign) and have the background rebuilt
convincingly, with control over where Photoshop borrows from.

## Steps
1. Select the object loosely with Lasso or Object Selection, then **Select > Modify > Expand**
   5-10 px so the selection includes the object's edge and shadow.
2. **Edit > Content-Aware Fill**. The workspace shows:
   - **Sampling area** (green overlay) - where Photoshop may copy from. Use the Sampling Brush
     to **remove** areas that should not be sampled (other people, the subject, a different
     surface) and add the right ones. Options: Auto, Rectangular, Custom.
   - Live preview of the fill.
3. **Fill Settings:**
   - **Color Adaptation** (default/high) for gradients like skies or walls with lighting changes.
   - **Rotation Adaptation** for curved/radial patterns.
   - **Scale** for repeating patterns at different sizes (perspective), **Mirror** for symmetrical scenes.
4. **Output To: New Layer** (always). Click Apply to keep working with a new selection, or OK.
5. Clean leftovers on another empty layer with Clone Stamp and Healing (see those skills).

## Alternatives
- Quick: Shift+Backspace/Delete > Contents: Content-Aware (no sampling control, destructive on the
  active layer - duplicate first).
- **Remove tool** for medium objects painted over in one stroke.
- **Generative Fill** (see that skill) for complex backgrounds with structure Photoshop cannot copy.
- **Content-Aware Move** tool to move or extend an object (Move or Extend mode, Structure/Color settings).

## Gotchas
- Fills along strong perspective lines (floor tiles, railings) often break - rebuild lines with
  Clone Stamp or Vanishing Point (Filter > Vanishing Point).
- Repeated chunks (the same cloud twice) - restrict the sampling area or re-run on smaller selections.
- Large fills in one go fail more than several smaller fills from the edges inward.

## Verify
- [ ] Result on its own layer; original intact.
- [ ] No repeated recognisable patches, no broken straight lines at 100%.
