---
id: creative-arts.animation.vector-graphics.shape-tweens-and-shape-hints
name: shape-tweens-and-shape-hints
category: creative-arts
field: animation
product: vector-graphics
tags: [shape-tween, shape-hints, animate, tweening, morphing, vector-animation, adobe-animate]
level: practitioner
status: draft
description: "Morph vector shapes in Adobe Animate with shape tweens: when they apply, shape hints, easing and blend settings, and the cases where frame-by-frame is better."
sources:
  - https://helpx.adobe.com/animate/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Shape tweens and shape hints (Adobe Animate)

A shape tween morphs one raw vector shape into another across a span of frames.

## When it applies
- Shape tweens work on **drawing shapes**, not on symbols, groups or text (convert text with Modify > Break Apart first, twice for multi-letter text).
- Put keyframes at start and end, each with its own shape on the same layer, then create the tween (right-click the span > Create Shape Tween, or the Insert menu).
- One layer holds one tweening shape; use layers for separate morphs.

## Properties
- **Ease**: values from -100 to 100 (ease in / ease out).
- **Blend**: **Distributive** (smoother intermediate shapes) or **Angular** (keeps corners and straight lines); pick Angular for shapes with sharp corners.

## Shape hints
Shape hints tell Animate which points on the start shape match points on the end shape.
1. Select the tween's first keyframe, then Modify > Shape > Add Shape Hint (Ctrl+Shift+H). A circle labelled "a" appears; up to 26 hints (a to z) are available.
2. Drag the hint onto the edge or corner of the start shape; at the end keyframe, drag the matching hint to the corresponding point.
3. Start hints show yellow, end hints green, and a hint that is not on an edge is red.
4. Place hints in a consistent order (counter-clockwise around the shape works well) and on corners and curve extrema.
5. View them with View > Show Shape Hints.

## When not to use
- Complex character mouths and body moves often morph badly. Use frame-by-frame drawings or symbol swaps instead for control (`animate-symbols-tweens.md` in this product).
- Large changes between very different shapes tweak into messy intermediates; add an in-between keyframe.

## Verify
- [ ] Scrub the tween: no flips, twists or collapsing parts.
- [ ] Hints sit on matching edges, in order.
