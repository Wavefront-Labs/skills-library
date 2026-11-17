---
id: creative-arts.animation.motion-graphics.ae-trim-paths
name: ae-trim-paths
category: creative-arts
field: animation
product: motion-graphics
tags: [trim-paths, shape-layers, after-effects, write-on, line-draw, stroke-animation, simultaneously, individually, offset, motion-design]
level: practitioner
status: draft
description: "Animate strokes drawing on with After Effects Trim Paths: start/end/offset, simultaneous vs individual trimming, path direction, and dashed and looped effects."
sources:
  - https://helpx.adobe.com/after-effects/using/shape-attributes-paint-operations-path.html
  - https://helpx.adobe.com/after-effects/using/overview-shape-layers-paths-vector.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trim Paths

**Goal:** lines that draw themselves on: route lines, underlines, logo traces, icon reveals.
Trim Paths is a shape-layer path operation that shows only a segment of each path.

## Basics

1. Shape layer with a stroked path (fill off for line draws).
2. Contents - Add - Trim Paths. Place it below the paths it should affect in the group.
3. Animate **End** 0% to 100% for a draw-on (Start stays 0). Animate **Start** 0 to 100 afterwards
   for a draw-off. **Offset** rotates the visible segment around closed paths (loops, spinners).
4. Ease the keyframes; draw-ons look mechanical with linear timing.

## Multiple paths

`Trim Multiple Shapes`:
- **Simultaneously**: each path trims at the same time (all lines draw together).
- **Individually**: paths are trimmed one after another in stacking order, as if they were one long
  path (sequential drawing of a logo).

## Direction and start point

- Path direction decides where drawing starts. Reverse it: right-click the Path - Reverse Path
  Direction (or the toggle button on the path).
- For closed paths, the first vertex is the start point; set it with the pen (right-click vertex -
  Set First Vertex) on a mask/shape path.

## Useful combinations

- Dashed travelling line: stroke dashes + animate dash Offset with an expression (`time*-50`).
- Spinner: closed circle, Start 0 End 25, Offset expression `time*360`.
- Round caps (Stroke - Line Cap: Round) avoid square ends that look unfinished.
- Text outline draw: Layer - Create - Create Shapes from Text, then Trim Paths with Individually.

## Gotchas

- Trim Paths placed above a path in the stack does nothing to it: order matters.
- Strokes with variable width (taper) taper relative to the full path, not the trimmed segment,
  unless you use the Taper settings on the stroke (AE 2020+); test the look.
- Illustrator artwork must be converted (Create Shapes from Vector Layer) before shape operators work.

## Verify

Frame-step the draw-on: it starts at the intended end, draws in the intended order, and the final
frame is exactly 100% with no gap or overlap.
