---
id: creative-arts.animation.texturing.painter-anchor-points
name: painter-anchor-points
category: creative-arts
field: animation
product: texturing
tags: [anchor-points, painter-layers, substance-painter, height-to-mask, micro-details, referencing-layers, normal-details, edge-wear-on-painted-height]
level: advanced
status: draft
description: "Use Substance 3D Painter anchor points so generators and masks react to painted height and details (seams, panels, scratches) that are not in the baked maps."
sources:
  - https://helpx.adobe.com/substance-3d-painter/painting/masking-and-effects/anchor-point.html
  - https://helpx.adobe.com/substance-3d-painter/painting/masking-and-effects/generator.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anchor points

**Goal:** wear and dirt that respond to details you painted in Painter (panel lines, rivets, stitched
seams, scratches in height), not only to the baked mesh. Generators only see baked maps; an anchor
point exposes a layer's result to masks and generators higher in the stack.

## Procedure

1. Paint or fill height details on a layer (e.g. panel lines in Height channel).
2. Right-click that layer (or an effect in its mask) - **Add anchor point**. Name it (`panel_lines`).
3. In a generator higher up (e.g. Dirt or Metal Edge Wear), enable **Micro details** (or the
   "Micro-Height/Micro-Normal" options) and select the anchor as input. The generator now includes the
   painted details in its curvature/AO-like computation.
4. Alternatively, in any mask add a Fill effect and pick the anchor as the source (grayscale of the
   referenced channel) to reuse the shape directly (e.g. paint inside the panel lines).

## Typical uses

- Edge wear on painted panel seams and embossed text.
- Dirt collecting in painted cracks and stitched lines.
- Reusing one hand-painted mask in several material layers (paint once, reference everywhere).

## Gotchas

- Anchors must be below the layers that reference them; moving them above breaks the reference.
- Referencing heavy anchors in many layers slows the project; reference once in a folder mask when
  possible.
- Micro details respond to Height/Normal channel content; painted colour alone does not create edges.

## Verify

Paint a new panel line on the anchor layer: edge wear and dirt in the referencing layers update to
include the new line without touching their masks.
