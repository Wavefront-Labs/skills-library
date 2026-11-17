---
id: creative-arts.animation.blender.solve-keyframes
name: solve-keyframes
category: creative-arts
field: animation
product: blender
tags: [blender, camera-solve, solve-keyframes, keyframe-a-b, camera-tracking]
level: practitioner
status: docs-checked
description: "Choose solver keyframes for a Blender camera solve: automatic Keyframe selection vs Keyframe A/B, the eight-track and parallax requirements, Tripod, and reading the solve error."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/solve.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/editing/track.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# solve-keyframes

Goal: a stable initial reconstruction, which needs two frames with enough camera movement between them.

## Settings (toolbar Solve tab > Solve)

- **Keyframe**: automatically selects keyframes for the initial reconstruction. The manual says it uses algorithms that try to find the keyframe pair with minimal reconstruction error and the best scene scale guess.
- **Keyframe A / Keyframe B**: the start (A) and end (B) frame of the range used for reconstruction (a new clip starts with 1 and 30 in the 5.2 source).
- **Tripod**: for footage where the camera does not move and only rotates. It solves only relative camera rotation and projects the feature points onto a sphere at the same distance from the camera. The manual notes 5 to 10 tracks per frame is typical for it and that more tracks do not mean a more accurate solution.
- **Refine**: see `creative-arts.animation.blender.refine-solve-intrinsics`.

## Requirements for the two keyframes (from the manual)

- At least eight common tracks on both keyframes.
- Noticeable parallax between them.

## Reading the result

**Solve Camera/Object Motion** reports the average reprojection error (the average distance between each reconstructed 3D track projected back into the footage and its tracked position) in the Info area and the editor header. The manual reads below 0.3 as accurate, 0.3 to 3.0 as quite nice and still usable, and above 3 as a sign that tracks need to be more accurate or that focal length or distortion values are wrong.

Clean Up (Solve tab) can select or delete tracks above a **Reprojection Error** (Error field) or shorter than a number of **Frames** (see `creative-arts.animation.blender.detect-features-autotrack`).

## Gotchas

- If the solve fails, check for too few shared tracks or too little parallax between A and B, then move B or try automatic selection (practice, not from the manual).
- A low error does not guarantee correct focal length; check the result in 3D.

## Verify

Add a test object on the floor: played over the footage, it does not slide against the real ground.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/toolbar/solve, movie_clip/tracking/clip/editing/track) and the 5.2 source (tracking.cc defaults for keyframes, space_clip.py Solve panel). Fixed: error thresholds (manual says 0.3 and 3.0, not 0.3 and 1), the eight-track requirement applies to both keyframes, and the old figure of 20 plus shared tracks. Removed unconfirmed claims about frame separation, error message text and sorting tracks by error in the Graph view.
Method: documentation only; no commands were run.
