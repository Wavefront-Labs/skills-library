---
id: creative-arts.animation.principles.pose-silhouette-test
name: pose-silhouette-test
category: creative-arts
field: animation
product: principles
tags: [animation, staging-principle, pose-silhouette-test, silhouette, readability, posing, key-poses, black-fill]
level: intro
status: draft
description: "Test key poses as solid black silhouettes: limbs clear of the body, action readable without interior detail, and how to fix poses that fail."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pose silhouette test

Goal: every key pose is readable when filled solid black. Disney animators in the 1930s
checked staging by looking at the silhouette; if the action reads in silhouette it reads in
any lighting, at any size, at a glance.

## How to run the test
- **2D**: fill the drawing with black on a separate layer, or flip to a solid fill view.
- **CG**: render or viewport with a flat black material/unlit and a white background (Blender:
  Solid shading with flat lighting and a black object color; Maya: viewport "use default
  material" with lights off).
- Look at it from the actual shot camera, at thumbnail size (about 200 px tall).

## What must pass
1. The action is identifiable: pointing, carrying, reaching, cowering.
2. Hands are outside the body mass when they matter to the action.
3. The line of action reads as one clear curve.
4. Props read (a held cup is a shape off the hand, not inside the torso).
5. Two characters do not merge into one blob.

## Fixes for failing poses
- Rotate the character relative to camera (three-quarter rather than front view usually
  opens the silhouette).
- Move hands and arms out of the torso shape; raise the elbow.
- Increase the line of action curve.
- Separate overlapping characters by depth or height, or move the camera.
- Cheat: rotate the hand toward camera even if physically off - staging beats accuracy.

## Failure modes
- Testing from the wrong angle (front orthographic instead of shot camera).
- Testing only the final pose, not anticipations and extremes.
- Accepting a pose that reads only because of interior line or color.

## Verify
- [ ] Each key and extreme passes in black from the shot camera.
- [ ] A viewer can name the action from the silhouette alone.

Related: `creative-arts.animation.character-design.character-design-craft` (design-level
silhouette), `creative-arts.animation.principles.anticipation-and-follow-through-staging`.
