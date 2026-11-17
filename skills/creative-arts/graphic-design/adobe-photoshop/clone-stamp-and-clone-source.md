---
id: creative-arts.graphic-design.adobe-photoshop.clone-stamp-and-clone-source
name: clone-stamp-and-clone-source
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photo-retouching, image-repair, clone-stamp, clone-source-panel, aligned-sampling, sample-current-and-below, hard-edge-retouching, pattern-repair]
level: practitioner
status: draft
description: "Retouch edges and structured textures with Clone Stamp on an empty layer: sampling modes, Aligned, hardness, Clone Source offsets, scale and rotation."
sources:
  - https://helpx.adobe.com/photoshop/using/retouching-repairing-images.html
  - https://helpx.adobe.com/photoshop/using/clone-source-panel-overview.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clone Stamp and the Clone Source panel

**Goal:** repairs along edges and structured detail (architecture, text-free signage, fabric
patterns) where healing tools smear.

## Set up
- New empty layer `Clone`. Clone Stamp (S): **Sample: Current & Below** (or All Layers; then
  ignore adjustment layers with the icon next to it so they are not baked in twice).
- **Aligned** on: the source moves with your strokes (continuous repair). Off: every stroke restarts
  from the original sample (repeat one element in several places).
- Brush hardness matched to the detail: 70-90% on hard edges, 0-30% on soft areas. Flow 100%,
  opacity 100% for structure; lower opacity to blend tone.

## Technique
1. **Alt/Option+click** to sample a source that matches texture, lighting and perspective.
2. Hold Alt/Option+Shift and the overlay (Show Overlay in Clone Source panel, Clipped) to line up
   edges before clicking.
3. Clone **along** edges: sample a point on the edge, paint along the same edge further down.
4. Re-sample often from different places to avoid recognisable repeats.
5. Fix the tonal mismatch afterwards with a soft Healing Brush on the same layer, or a low-opacity clone.

## Clone Source panel (Window > Clone Source)
- Store up to 5 sources (even from other open documents).
- **Offset, scale (W/H %), rotation** of the source: clone a window onto a wall in perspective,
  mirror by -100% width, or fix a slightly smaller repeated element.
- Frame offset for video layers.

## When to use which
Clone = exact copy (structure, edges, patterns). Healing/Spot healing/Remove = texture with tone
blending (skin, sky, walls). Content-Aware Fill = large areas (see that skill). Often combine: clone
the structure first, heal the transition.

## Gotchas
- Cloning on the original layer is destructive; always use an empty layer.
- Cloning noise/grain from a different area mismatches; add matching grain at the end if needed.
- Repeating patterns (bricks, tiles) must line up with the grid: use Aligned and precise sampling.

## Verify
- [ ] At 100% and at output size, no doubled textures or broken lines.
- [ ] `Clone` layer toggles cleanly; original untouched.
