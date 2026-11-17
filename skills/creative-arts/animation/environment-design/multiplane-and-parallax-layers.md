---
id: creative-arts.animation.environment-design.multiplane-and-parallax-layers
name: multiplane-and-parallax-layers
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, layout-art, multiplane, parallax, depth-planes, compositing]
level: practitioner
status: draft
description: "Separate backgrounds into multiplane layers for parallax: plane distances, relative move speeds, overlap margins and painting each level for depth."
sources:
  - https://en.wikipedia.org/wiki/Multiplane_camera
  - https://en.wikipedia.org/wiki/Parallax_scrolling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiplane and parallax layer separation

Goal: 2D environments with real depth when the camera moves, by splitting art into planes
that move at different speeds (Disney's multiplane camera, digital equivalent in
compositing or 2.5D scenes).

## Plane speeds
For a camera truck, apparent speed is inversely proportional to plane distance.
- Practical ratios: FG 1.5-2x the character plane, MG 1x, BG 0.3-0.5x, sky 0-0.1x.
- In a 3D compositor (After Effects, Nuke, Toon Boom, Blender) place planes at real Z
  depths and let the camera produce correct parallax; scale each plane up by its distance
  to keep its framed size.
- A **zoom** (lens change) produces no parallax; a **truck in** does. Choose deliberately.

## Method
1. In layout, assign each element to a plane; aim for 3-5 planes.
2. Paint each plane with extra width (overlap margin) so its edges never show after moving
   further than the plane behind.
3. Paint behind foreground elements: the BG under a moving tree must be complete.
4. Apply aerial perspective per plane (value, saturation, detail decrease with distance).
5. Test the move as a quick comp before final paint; adjust distances until parallax feels right.
6. Optionally add depth of field per plane for focus pulls.

## Failure modes
- Holes revealed behind moving FG elements.
- Planes too few or too close in speed: parallax reads as sliding cards.
- Plane edges visible at the end of the move.

## Verify
- [ ] Each plane has overlap margin for its move.
- [ ] Hidden areas painted.
- [ ] Test comp approved before final paint.

Related: `creative-arts.animation.environment-design.depth-planes`,
`creative-arts.animation.environment-design.pan-background-layouts`.
