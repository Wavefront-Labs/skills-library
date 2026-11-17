---
id: creative-arts.animation.storyboarding.focal-length-choice
name: focal-length-choice
category: creative-arts
field: animation
product: storyboarding
tags: [storyboarding, camera-angles, focal-length-choice, lens, wide-lens, telephoto, compression, perspective-distortion, layout, cg-camera]
level: practitioner
status: draft
description: "Pick lens focal lengths in boards and CG layout: wide for space and distortion, long for compression and isolation, and keeping lens language consistent."
sources:
  - https://books.google.com/books?vid=ISBN9781933492957
  - https://en.wikipedia.org/wiki/Focal_length
  - https://docs.blender.org/manual/en/latest/render/cameras.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Focal length choice

Goal: choose the lens look per shot so space feels the way the story needs. In 2D boards this is
drawn perspective; in CG layout it is the camera's focal length.

## Lens effects (35 mm full-frame equivalents)
| Lens | Look | Use |
|---|---|---|
| 14-24 mm (wide) | deep space, strong convergence, distortion near edges | establishing, action, comedy distortion, claustrophobia when close |
| 35-50 mm (normal) | natural perspective | most coverage, neutral |
| 85-135 mm (portrait/long) | flattened faces, soft backgrounds | close-ups, emotion |
| 200 mm+ (telephoto) | compressed depth, background feels close | heat-haze crowds, isolation, chase "stacking" |

## Drawing the look
- Wide: vanishing points close together relative to frame, exaggerated size change between near
  and far objects.
- Long: vanishing points far apart (near-parallel lines), little size change with distance.
- Note the intended lens on the panel for the layout department (e.g. "wide - 24 mm").

## Rules
- Close-ups of faces on wide lenses distort noses and foreheads - use deliberately (comedy, menace).
- Lens consistency: a scene often has a lens family; changing lens mid-scene should mean something.
- Dolly + zoom (vertigo) requires both lens and position change.

## CG notes
- Blender camera: Focal Length in mm with Sensor Fit/size set (default 36 mm sensor); Maya
  similar. Match the board's convergence by eye.
- Depth of field strength depends on focal length and f-stop - long lenses give shallower focus.

## Failure modes
- Default 50 mm on every CG shot (flat, unconsidered).
- Wide-angle close-ups making the lead character look grotesque unintentionally.
- Boards drawn with inconsistent perspective that layout cannot match with any lens.

## Verify
- [ ] Lens noted for key shots.
- [ ] Perspective in boards matches the noted lens.
- [ ] Lens changes within a scene are motivated.

Related: `creative-arts.animation.storyboarding.zoom-vs-dolly`,
`creative-arts.animation.environment-design.set-building`.
