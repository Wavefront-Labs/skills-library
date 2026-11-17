---
id: creative-arts.animation.principles.form-construction
name: form-construction
category: creative-arts
field: animation
product: principles
tags: [animation, solid-drawing, form-construction, volumes, spheres, boxes, cylinders, cross-contours, construction-drawing, 2d, drawing]
level: practitioner
status: draft
description: "Build characters and props from 3D volumes (spheres, boxes, cylinders) with cross-contour lines so they stay solid and consistent when turned and animated."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://books.google.com/books?vid=ISBN9781560100843
  - https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Form construction

Goal: drawings that feel like solid objects in space with weight and volume, so they can be
turned, squashed and animated without "flattening". This is principle 11, solid drawing, and
Preston Blair's construction method.

## Method
1. **Gesture first**: a line of action and a quick gesture for the pose.
2. **Primary masses**: head as a sphere (with a jaw/muzzle mass), ribcage as an egg or box,
   pelvis as a box or bowl. Draw them **in perspective** - ellipses for cross-sections, boxes
   with converging edges.
3. **Cross-contours**: wrap center lines and cross lines around each mass (the vertical
   centre line and the eye line on the head). They show the turn and tilt.
4. **Connectors**: cylinders for neck, arms and legs; draw the ellipse at each end so you know
   which way the cylinder faces.
5. **Overlaps**: let near forms overlap far forms with a clear T-junction (the near contour
   continues, the far one stops).
6. **Detail last**: features placed on the cross-contours, so they wrap.

## Consistency checks
- Volume: the same mass is the same size in every drawing (compare on light box/onion skin).
- Centre line: follows the turn smoothly through a head turn.
- Ellipse degree: consistent with the eye level (ellipses open up below the horizon, flatten near it).

## Failure modes
- Outline-first drawing: shapes look like cut-outs and shift volume each frame.
- Ellipses at the wrong degree: limbs look twisted.
- Features drawn flat on a turning head.

## Verify
- [ ] Construction layer shows masses with cross-contours on every key.
- [ ] Flipping keys, volumes stay constant.
- [ ] Features follow the head's cross-contours through turns.

Related: `creative-arts.animation.principles.avoiding-twinning`,
`creative-arts.animation.principles.figure-foreshortening`,
`creative-arts.animation.character-design.model-sheet-turnaround`.
