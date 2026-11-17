---
id: creative-arts.animation.environment-design.3d-layout-camera-and-set-blocking
name: 3d-layout-camera-and-set-blocking
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, layout-art, 3d-layout, camera-layout, set-blocking, previs]
level: practitioner
status: draft
description: "Do 3D layout: build camera, lens and set placement per shot from the animatic, block characters, and hand off locked cameras to animation."
sources:
  - https://www.khanacademy.org/computing/pixar
  - https://docs.blender.org/manual/en/latest/render/cameras.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 3D layout: camera and set blocking

Goal: each shot from the story reel translated into a 3D scene with a final camera, lens,
set dressing and rough character positions, so animation starts from locked framing.

## Inputs
- Approved animatic/story reel with shot lengths.
- Set model or blockout, characters at correct scale (size comparison sheet).
- Lens and aspect ratio rules from the style guide (e.g. 2.39:1, lens range 24-85 mm).

## Method
1. Set scene frame range from the reel; import the reel as a camera background/image plane.
2. Place the camera and choose the lens to match the board composition and the
   psychological distance (wide = space and isolation, long = compression and intimacy).
3. Block characters as stepped key poses at board positions; check eyelines and the
   180-degree line across the sequence.
4. Cheat the set per shot: move props or walls out of the way (and note cheats so set
   dressing knows); never cheat what continuity will catch in the reverse shot.
5. Animate camera moves with the same eases as the board; avoid moves the reel did not ask for.
6. Playblast, cut into the reel, review for continuity and timing.
7. Lock the camera (and note any cheats) and publish to animation.

## Failure modes
- Lens chosen to "fit everything", flattening the drama.
- Cheats that break continuity between angles.
- Camera changed in animation after layout lock, breaking downstream lighting.

## Verify
- [ ] Every shot's playblast cut into the reel.
- [ ] Lens and aspect within the style guide.
- [ ] Cheats documented, camera locked.

Related: `creative-arts.animation.blender.layout-blocking`,
`creative-arts.animation.storyboarding.focal-length-choice`,
`creative-arts.animation.blender.camera-cinematography`.
