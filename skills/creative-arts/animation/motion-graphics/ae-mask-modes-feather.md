---
id: creative-arts.animation.motion-graphics.ae-mask-modes-feather
name: ae-mask-modes-feather
category: creative-arts
field: animation
product: motion-graphics
tags: [mask-feather, masks, after-effects, mask-modes, variable-width-feather, mask-expansion, mask-path-animation, add-subtract-intersect]
level: practitioner
status: draft
description: "Use After Effects masks properly: modes (add/subtract/intersect/difference), feather and variable-width feather, expansion, and animating mask paths cleanly."
sources:
  - https://helpx.adobe.com/after-effects/using/creating-masks.html
  - https://helpx.adobe.com/after-effects/using/mask-modes.html
  - https://helpx.adobe.com/after-effects/using/animating-masks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mask modes and feather

**Goal:** soft, exact isolation of areas on a layer: vignettes, reveals, cutting a character out of a
board, soft-edged spot effects.

## Mask properties (M twice to reveal)

| Property | Purpose |
|---|---|
| Mask Path | shape; animatable |
| Mask Feather | uniform edge softness (X/Y independent if unlinked) |
| Mask Opacity | strength |
| Mask Expansion | grow/shrink without editing the path |
| Mode | how masks combine |
| Inverted | flip the mask |

## Modes (evaluated top to bottom)

- **Add**: union. **Subtract**: removes from masks above. **Intersect**: keeps only overlap with
  masks above. **Lighten/Darken**: max/min of overlapping opacities. **Difference**: union minus
  overlap. **None**: path exists only for effects (e.g. stroke, text on path).
The first mask's mode against nothing: Subtract on the first mask cuts out of the full layer.

## Variable-width feather

Mask Feather tool (under the Pen tool, G): click on the mask edge to add feather points, drag to
set feather per area. Use for organic soft edges (hair, smoke) and when one side must be crisp and
the other soft.

## Animating mask paths

- Keyframe Mask Path; keep the same vertex count and start vertex across keys or the shape
  re-interpolates badly (twisting). Set First Vertex consistently.
- For rotoscoping use several simple masks (one per limb) rather than one complex mask: each moves
  rigidly, fewer keys.
- Mask tracking: right-click a mask - Track Mask for position/scale/rotation/perspective following.

## Gotchas

- Feather spreads equally inside and outside the path; use Expansion negative to keep the feather
  inside the edge.
- Masks on a scaled/rotated layer are in layer space; scaling the layer scales the feather too.
- Effect order: masks apply before effects on the layer unless the effect uses the mask as input;
  use an adjustment layer or precompose for post-effect masking.

## Verify

View over a contrasting solid at 100% and 200%: edges are as soft as intended, no twisting between
mask keyframes, no fringe from feathering out into the background.
