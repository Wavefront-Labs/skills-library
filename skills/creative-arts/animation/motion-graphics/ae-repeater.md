---
id: creative-arts.animation.motion-graphics.ae-repeater
name: ae-repeater
category: creative-arts
field: animation
product: motion-graphics
tags: [repeater, shape-layers, after-effects, radial-pattern, copies, offset, start-end-opacity, procedural-shapes, motion-design]
level: practitioner
status: draft
description: "Build procedural patterns with the After Effects shape Repeater: copies, offset, transform per copy, radial bursts, grids, and animating the offset."
sources:
  - https://helpx.adobe.com/after-effects/using/shape-attributes-paint-operations-path.html
  - https://helpx.adobe.com/after-effects/using/overview-shape-layers-paths-vector.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The shape Repeater

**Goal:** many copies of a shape from one source: sunbursts, dotted grids, flower petals, spoke
wheels, stacked rings. Editing the source updates every copy.

## Basics

Contents - Add - Repeater. It copies everything above it in the same group.
- **Copies**: count.
- **Offset**: shifts which copy is first (fractional values animate smoothly through the sequence).
- **Composite**: Above/Below stacking order.
- **Transform: Repeater**: Anchor Point, Position, Scale, Rotation applied cumulatively per copy;
  Start Opacity / End Opacity fade across copies.

## Recipes

Radial burst (12 rays):
1. Group with a thin rectangle offset from centre (Position Y -150).
2. Repeater: Copies 12, Position 0,0, Rotation 30 (360/12).
3. Group anchor at the comp centre so rotation is around the centre.

Dot grid:
1. Ellipse group. Repeater 1: Copies 10, Position 40,0.
2. Second Repeater below: Copies 10, Position 0,40. Two repeaters multiply: 100 dots.

Animated build-on: animate Copies from 0 to 12 (snaps per copy) or animate Offset with a Trim Paths
inside for a smooth growth.

## Expression links

Drive Rotation from Copies so changing count keeps a full circle:
`360 / content("Repeater 1").copies`.

## Gotchas

- Repeater only affects contents above it within its group; put the repeated element and the
  repeater in their own group to avoid copying unrelated paths.
- Scale in Transform: Repeater compounds per copy (90% gives rapid shrink); small values cascade.
- Many copies of complex shapes are slow to render; precompose and use a single repeated layer or
  turn on Draft 3D off for previews.

## Verify

Change Copies to an odd value and check the pattern still closes (no gap in radial), and the source
edit propagates to all copies.
