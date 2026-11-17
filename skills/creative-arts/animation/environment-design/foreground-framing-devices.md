---
id: creative-arts.animation.environment-design.foreground-framing-devices
name: foreground-framing-devices
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, atmospheric-perspective, framing-device, foreground-elements, vignette, repoussoir, depth, composition, background-layout]
level: practitioner
status: draft
description: "Design foreground framing elements (branches, arches, silhouettes, props) that add depth and steer the eye without competing with the subject or blocking animation."
sources:
  - https://books.google.com/books?vid=ISBN9781933492957
  - https://en.wikipedia.org/wiki/Repoussoir
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Foreground framing devices

Goal: near elements at the frame edges (the painter's repoussoir) that push the eye inward to the
subject and create a depth plane.

## Types
- Natural: overhanging branches, foliage, rocks, grass blades.
- Architectural: arches, door frames, pillars, window edges, railings.
- Props/characters: a shoulder, a silhouetted figure, a lamp.

## Design rules
1. **Low detail, strong shape**: usually a dark (or very light) silhouette with soft edges or blur.
2. **Frame edges only**: keep them to the corners/sides; never cross the subject's face or key action.
3. **Shape that points in**: curves and diagonals leading toward the focal point.
4. **Value separation** from the midground.
5. **Parallax**: in camera moves, FG elements move fastest - put them on their own layer (2D) or
   as separate assets (3D); check they do not wipe across key action.

## For animation production
- Note FG elements in layout as overlays (OL) so animators know where characters pass behind.
- Avoid FG elements that require animated interaction (swaying branches) unless budgeted.

## Failure modes
- Detailed, bright FG competing with the subject.
- FG element covering acting during a camera move.
- Overused (every shot through foliage).

## Verify
- [ ] FG element frames, does not overlap, the focal action.
- [ ] Value and detail lower than the subject.
- [ ] Parallax moves checked for coverage of key action.

Related: `creative-arts.animation.storyboarding.frame-within-a-frame`,
`creative-arts.animation.environment-design.depth-planes`.
