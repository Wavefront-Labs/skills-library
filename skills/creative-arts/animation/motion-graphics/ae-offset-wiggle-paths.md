---
id: creative-arts.animation.motion-graphics.ae-offset-wiggle-paths
name: ae-offset-wiggle-paths
category: creative-arts
field: animation
product: motion-graphics
tags: [wiggle-paths, shape-layers, after-effects, offset-paths, zig-zag, pucker-bloat, twist, roughen, hand-drawn-boil, motion-design]
level: practitioner
status: draft
description: "Distort shape layers procedurally in After Effects: Offset Paths outlines, Wiggle Paths boil, Zig Zag, Pucker and Bloat, Twist; hand-drawn line-boil looks for animation."
sources:
  - https://helpx.adobe.com/after-effects/using/shape-attributes-paint-operations-path.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offset and Wiggle Paths (and friends)

**Goal:** organic or stylised path distortion without hand-animating vertices: line boil like
hand-drawn animation, inflating outlines, electric zig-zags.

## Operators (Contents - Add)

| Operator | Key controls | Use |
|---|---|---|
| Offset Paths | Amount, Line Join, Copies, Copy Offset | outlines, concentric rings, glow-like stacked strokes |
| Wiggle Paths | Size, Detail, Points (corner/smooth), Wiggles/Second, Correlation, Random Seed | line boil, wobbly blobs |
| Zig Zag | Size, Ridges per segment, Points | electricity, serrated edges |
| Pucker & Bloat | Amount | star/flower inflation |
| Twist | Angle, Center | spirals |
| Round Corners | Radius | soften geometric shapes |

Operators apply to paths above them in the group; order changes the result (Offset then Wiggle
differs from Wiggle then Offset).

## Recipe: hand-drawn line boil (stepped)

1. Stroke your shape; add Wiggle Paths: Size 2-4, Detail 3-6, Points Smooth, Wiggles/Second 0.
2. Animate boil on twos: on the Wiggle Paths **Temporal Phase** (or Random Seed) add expression
   `posterizeTime(12); time*360` (for phase) so the wobble steps 12 times a second like redrawn
   drawings.
3. Keep Size small; boil should read as life, not as shaking.

## Recipe: inflating outline rings

Offset Paths: Copies 4, Copy Offset 1, Amount animated 0 to 20: rings expand from the shape (sonar,
emphasis pulses).

## Gotchas

- Wiggle with Points: Corner turns curves jagged; use Smooth for organic shapes.
- Correlation 100% moves all points together (shape slides) - lower it (30-60%) for true wobble.
- Heavy operator stacks re-calc every frame; precompose and render as a cached layer for long comps.

## Verify

Frame-step the boil: changes happen only every second frame (if posterized), amplitude is subtle at
100% viewer size, and the shape silhouette stays readable.
