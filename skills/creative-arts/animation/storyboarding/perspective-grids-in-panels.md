---
id: creative-arts.animation.storyboarding.perspective-grids-in-panels
name: perspective-grids-in-panels
category: creative-arts
field: animation
product: storyboarding
tags: [storyboarding, story-drawing, panel-perspective, perspective-grid, horizon-line, vanishing-point, figure-scaling, storyboard-pro, 3d-set]
level: practitioner
status: draft
description: "Set up perspective in board panels quickly: horizon placement, vanishing points outside the panel, scaling figures to the horizon, and using 3D sets or grid tools."
sources:
  - https://books.google.com/books?vid=ISBN9781933492957
  - https://en.wikipedia.org/wiki/Perspective_(graphical)
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Perspective grids in panels

Goal: consistent, believable space in every panel without slowing down.

## Quick setup
1. **Horizon line** = camera height. Place it first (low for heroic/low angle, high for high angle).
2. **Vanishing points** usually sit outside the panel for natural perspective; points inside
   the panel give dramatic, wide-angle distortion.
3. **Ground plane grid**: a few converging lines to the VP plus horizontal lines spaced closer
   as they recede.
4. **Figure scaling**: with an eye-level camera, all standing adults' heads sit on the horizon;
   for a different camera height, mark one figure and project others' heights using lines to
   the VP.

## Tools
- Storyboard Pro: perspective guides (1-, 2-, 3-point and 4/5-point) per panel; 3D camera and
  imported 3D sets.
- Krita/Clip Studio/Photoshop: perspective rulers/assistants.
- Blender/SketchUp blockouts: render a grey set from the panel camera and draw over it -
  ensures consistency across panels of the same location.

## Consistency within a setup
- Same horizon and VPs for all panels of the same camera setup; copy the guide layer.
- Keep a location floor plan with camera positions.

## Failure modes
- Horizon drifting between panels of the same setup.
- Figures floating (feet not on the ground plane at the right scale).
- Vanishing points crowded inside the panel unintentionally (distortion).

## Verify
- [ ] Each setup has one horizon and VP set reused across its panels.
- [ ] Figure heights consistent with the horizon.
- [ ] Layout can match the panels with a real lens.

Related: `creative-arts.animation.environment-design.depth-cues`,
`creative-arts.animation.storyboarding.focal-length-choice`.
