---
id: creative-arts.photography-fine-art.adobe-lightroom.adding-subtracting-and-intersecting-masks
name: adding-subtracting-and-intersecting-masks
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, mask-intersect, lightroom-masking, mask-subtract, invert-mask, lightroom-classic]
level: practitioner
status: draft
description: "Combine Lightroom Classic mask components with Add, Subtract and Intersect, invert masks and duplicate them for complex local adjustments."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Masking; combine masks)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adding, subtracting and intersecting masks

Each mask in the Masks panel is a stack of **components**. Its adjustments apply to the combined area.

## Operations (click a mask, then Add / Subtract buttons, or right-click a mask)
- **Add**: union with another tool (e.g. Sky + Brush to include a missed area).
- **Subtract**: remove a region (Subject minus Brush around the hands; Sky minus Luminance range for clouds).
- **Intersect with**: keeps only the overlap (Linear Gradient intersect Luminance 0-40 = darker lower half, shadows only). Created as a subtract component with "Invert" ticked behind the scenes.
- **Invert**: tick Invert on a component (or the whole mask) to flip it. Background = inverted Subject.
- Right-click a mask > **Duplicate and Invert Mask**: get Sky and Not-sky masks with matching edges in one step, for a separate land adjustment.

## Worked example: brighten foreground grasses without touching sky or rocks
1. Create mask: Landscape > Vegetation.
2. Subtract > Luminance Range 80-100 (removes bright highlights).
3. Intersect > Linear Gradient from the bottom to mid-frame.
4. Adjust Exposure +0.3, Texture +10. Name "Foreground grass".

## Gotchas
- Component order does not matter for Add, but subtract components only remove from what is above them in the same mask.
- Too many components slow Develop; merge ideas into fewer masks.
- Synced masks keep component structure; AI components recompute per photo, brush components do not move.

## Verify
- [ ] Overlay shows only the intended region; hovering each component highlights its contribution.
