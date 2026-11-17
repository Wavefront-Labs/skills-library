---
id: creative-arts.animation.blender.link-empty-to-track
name: link-empty-to-track
category: creative-arts
field: animation
product: blender
tags: [blender, motion-tracking, tracks-to-empties, link-empty-to-track, follow-track, camera-tracking]
level: practitioner
status: docs-checked
description: "Anchor CG to tracks in Blender: Link Empty to Track makes Follow Track empties; Follow Track options (3D Position, Undistort, Depth Object, Frame Method)."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/editing/reconstruction.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/motion_tracking/follow_track.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# link-empty-to-track

Goal: place CG exactly where a tracked feature appears (a lamp on a wall, a spot on a table).

## Link Empty to Track

Movie Clip Editor, Tracking mode: **Reconstruction > Link Empty to Track** (also in the Solve tab > Geometry panel). For each selected track of the active tracking object it creates an Empty, named after the track, with a **Follow Track** constraint. The operator sets the constraint to the track and tracking object with **3D Position turned off**, so the empty follows the 2D marker on a plane in front of the camera. Tick **3D Position** on the constraint to use the reconstructed 3D position instead (this needs a camera solve).

## Follow Track constraint (Object Constraints)

- **Active Clip**: tick when the marker is in the scene's active clip; otherwise pick a clip.
- **3D Position**: use the marker's reconstructed world position instead of its position in the flat video. By default the object follows the 2D motion of the marker.
- **Undistort**: use the marker's position after lens-distortion compensation. Not available with 3D Position.
- **Frame Method** (*Stretch*, *Fit*, *Crop*): how to handle an aspect-ratio difference between the footage and the render.
- **Object**: the tracking object holding the marker; if empty, Track lists the markers used to reconstruct the camera.
- **Track**: the marker to follow.
- **Camera**: the camera in whose view the object appears; if empty, the scene's active camera.
- **Depth Object**: the constrained object is projected onto this object's surface (the manual's example is facial makeup). Not available with 3D Position.
- **Constraint to F-Curve** replaces the constraint with equivalent keyframes.
- The manual says following the reconstructed 3D position requires at least eight markers and a solve.

## Gotchas

- An empty from a poor track will follow it wherever it drifts; use good tracks.
- Link Empty to Track makes 2D followers by default; switch on 3D Position when you want the solved bundle.

## Verify

View through the camera over the footage: each empty stays on its feature through the shot.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/editing/reconstruction, animation/constraints/motion_tracking/follow_track) and the 5.2 source (bl_operators/clip.py track_to_empty). Fixed: Link Empty to Track is in the Reconstruction menu and Geometry panel (not Scene Setup), it creates empties with 3D Position off, the constraint field is Active Clip with an Object field, and Depth Object and Undistort need 3D Position off. Removed unconfirmed claims about bundle-position placement and automatic updates after reorienting.
Method: documentation only; no commands were run.
