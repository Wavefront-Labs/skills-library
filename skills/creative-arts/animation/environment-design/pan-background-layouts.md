---
id: creative-arts.animation.environment-design.pan-background-layouts
name: pan-background-layouts
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, layout-art, pan-background, camera-move-layout, field-guide, background-layout]
level: practitioner
status: draft
description: "Lay out pan backgrounds and camera-move layouts: extended BG length from pan distance, start/end field positions, perspective that survives the move, and seams."
sources:
  - https://animationguild.org/
  - https://en.wikipedia.org/wiki/Panning_(camera)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pan backgrounds and camera-move layouts

Goal: a background wide or tall enough for the camera move, with clearly marked start and
end fields and perspective that does not break while panning.

## Sizing the pan
1. Get the move from the board/animatic: direction, distance, duration, eases.
2. BG width = field width + total pan distance (+ safety margin on each side, often
   half a field inch or 5-10% of the field).
3. For a repeating/cycling pan (walk past endless scenery), make the BG a seamless loop:
   the last field matches the first exactly.
4. Diagonal pans: size both dimensions; vertical pans (tilts) need a tall BG.

## Layout drawing
- Draw the start field and end field rectangles (with field guide notation, e.g. 12F) and
  arrows for the move; number the keys of any eases.
- **Perspective for pans**: a true camera pan rotates, so a long pan BG drawn in normal
  linear perspective distorts at the ends. Options: (a) keep the pan short, (b) use
  curvilinear/cylindrical perspective so verticals stay vertical and horizontals bow
  gently, (c) treat it as a truck (camera moves sideways) where linear perspective with
  a constant VP height is valid, (d) build in 3D and render a panoramic plate.
- Avoid strong converging lines at the far ends of long pans.

## Timing check
- Pan speed in field inches per frame; very slow pans on 2s can strobe. Fast pans need
  motion blur or a blur-panned BG.
- Characters walking on a pan need their contact positions moved by the pan increment.

## Failure modes
- BG too short: the camera runs off the art.
- Strobing from repeating vertical elements spaced near the per-frame move.
- Perspective that bends wrongly at the ends.

## Verify
- [ ] BG width = field + pan distance + margin.
- [ ] Start/end fields and eases marked.
- [ ] Loop seam invisible on cycling pans.

Related: `creative-arts.animation.storyboarding.pans-and-tilts`,
`creative-arts.animation.production-design.background-painting`.
