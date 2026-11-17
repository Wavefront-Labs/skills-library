---
id: creative-arts.animation.motion-graphics.ae-3d-camera-tracker
name: ae-3d-camera-tracker
category: creative-arts
field: animation
product: motion-graphics
tags: [camera-tracker, motion-tracking, after-effects, 3d-camera-tracker, solve-camera, ground-plane, track-points, matchmove, 3d-text]
level: advanced
status: draft
description: "Solve a camera with the After Effects 3D Camera Tracker, set a ground plane and place 3D text/solids that stick to the scene; diagnose bad solves."
sources:
  - https://helpx.adobe.com/after-effects/using/tracking-3d-camera-movement.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 3D Camera Tracker

**Goal:** place 3D graphics (titles, labels, shadows) into live action or rendered plates so they move
with the camera's parallax.

## Procedure

1. Select the footage layer, Animation - Track Camera (or Tracker panel - Track Camera). Analysis
   runs in the background, then solves.
2. Settings (Advanced): Shot Type (Fixed angle of view, Variable zoom, Specify angle of view if the
   focal length/film back are known), Solve Method (Auto, Typical, Mostly Flat Scene, Tripod Pan).
   Specify the real angle of view when known; it improves solves considerably.
3. After solving, coloured track points appear. Select 3+ points on a plane (Shift-click or lasso),
   a target circle shows the plane orientation.
4. Right-click - **Set Ground Plane and Origin**, then **Create Text and Camera** (or Solid,
   Null). AE adds a 3D Tracker Camera and a 3D layer aligned to the plane.
5. Replace the placeholder text/solid with your artwork; keep it a 3D layer.

## Diagnosing

- Average error (in Advanced) under ~0.5 px is good; above ~1 px expect sliding.
- Delete bad points (on moving objects: people, water, reflections) and re-solve: select them,
  Delete, AE re-solves automatically.
- Tripod pans have no parallax; choose Tripod Pan so AE does not invent depth.

## Rendered animation

For CG plates, export the actual camera from the 3D app (FBX/Alembic or a script into AE via an
importer) instead of solving: exact focal length and movement, no error. Use the tracker for
live-action plates or flattened 2D animation with camera moves.

## Gotchas

- Rolling-shutter footage solves badly; fix rolling shutter first (Rolling Shutter Repair effect).
- Motion blur on the comp must match the plate: enable layer motion blur and match the shutter angle.
- Tracker camera units are arbitrary; scale is unknown unless you set a reference distance.

## Verify

Play at speed and scrub frames with large camera moves: the placed layer stays fixed to its ground
position without sliding; check against a track point near it.
