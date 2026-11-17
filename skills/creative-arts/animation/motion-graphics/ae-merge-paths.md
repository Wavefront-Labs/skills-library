---
id: creative-arts.animation.motion-graphics.ae-merge-paths
name: ae-merge-paths
category: creative-arts
field: animation
product: motion-graphics
tags: [merge-paths, shape-layers, after-effects, boolean, subtract, intersect, exclude-intersections, compound-paths, motion-design]
level: practitioner
status: draft
description: "Combine shape paths with After Effects Merge Paths modes (add, subtract, intersect, exclude) for animatable boolean shapes like donuts, cut-outs and reveals."
sources:
  - https://helpx.adobe.com/after-effects/using/shape-attributes-paint-operations-path.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Merge Paths

**Goal:** live boolean shapes: a donut whose hole grows, a logo cut by a moving circle, an icon
morph via intersections. Merge Paths combines every path above it in a group into one compound path.

## Modes

| Mode | Result |
|---|---|
| Merge | union, all paths combined (overlaps not cut) |
| Add | union |
| Subtract | top paths cut out of the bottom path (order dependent) |
| Intersect | only the overlap remains |
| Exclude Intersections | overlap removed, rest kept |

Stacking order: in Subtract, the path at the bottom of the group (first created, lowest in the
Contents list order within the group) is the base; paths above it are subtracted.

## Recipe: animated donut / ring reveal

1. Group: Ellipse Path 1 (size 300), Ellipse Path 2 (size 200), then Merge Paths (Subtract), then
   one Fill.
2. Animate Ellipse 2 size from 0 to 290: a disc becomes a thin ring.
3. Fill and stroke must come after Merge Paths in the group so they render the merged result.

## Recipe: cut-out wipe

Logo shape path + a rectangle path moving across, Merge Paths Intersect: the logo appears only
where the rectangle is: a clean shape-based wipe without a track matte.

## Gotchas

- Merge Paths needs paths, not separate filled sub-groups each with their own fills; put raw paths
  (and the operator) in one group, then one fill/stroke below.
- Text must become shapes first (Create Shapes from Text).
- Complex animated booleans can produce flickering slivers at coincident edges; offset paths by a
  pixel.
- Illustrator compound paths imported as shapes already carry their own merge operations; inspect
  before adding more.

## Verify

Toggle the Merge Paths operator off and on: off shows overlapping originals, on shows the intended
boolean result at the first, middle and last frame of the animation.
