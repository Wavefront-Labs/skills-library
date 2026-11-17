---
id: creative-arts.animation.blender.object-tracking-stabilization
name: object-tracking-stabilization
category: creative-arts
field: animation
product: blender
tags: [blender, object-tracking, stabilization, 2d-stabilization, motion-tracking, object-solver, movie-clip-editor, screen-replacement, corner-pin, plane-track, track-to-empty, follow-track]
level: advanced
status: docs-checked
description: "Beyond the camera solve in Blender: Object Solver, Plane Track and Plane Track Deform for screen replacement, 2D stabilization, and Follow Track anchors."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/editing/track.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/stabilization/index.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/motion_tracking/follow_track.html
  - https://docs.blender.org/manual/en/latest/compositing/types/tracking/plane_track_deform.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# object-tracking-stabilization

Goal: three jobs the camera solve does not cover: a moving object with its own motion, a flat surface to replace, and footage that shakes.

## Object tracking (Object Solver)

Summary; details in `creative-arts.animation.blender.object-solve-tracking-objects`. Solve the camera first, add a tracking object in the Objects panel, track at least eight markers on the physical object, solve with that object active, then add an **Object Solver** constraint (Active Clip, Object, Camera) to a Blender object and use **Set Inverse**. Setup Tracking Scene does not create the object-solver setup.

## Plane Track (screen, sign or poster replacement)

1. Track point markers on the plane. **Track > Create Plane Track** creates a plane that deforms like the plane defined by all selected point tracks; at least four tracked points on the plane are needed, and more give a better estimate. The points need not be corners and can lie anywhere on the plane, even far from the part to replace. Two neighbouring frames must share at least four tracks.
2. Plane Track panel (Track tab): **Auto Keyframe** (keys corners when you move them), **Image** (a preview image shown in the editor only), **Opacity** (display only), **New Image from Plane Track** and **Update Image from Plane Track** (an unwarped image of the surface, for example for retouching).
3. Compositor: **Plane Track Deform** node (Add > Tracking). Input: Image to put in place. Properties: Movie Clip, Object, Track (plane track). Outputs: *Image* (the input warped to the plane) and *Plane* (a black and white mask of the plane). Use Image with an Alpha Over, or mix the clip and an image using Plane as the factor. Motion Blur has Samples (taken only from the next frame) and Shutter.

## 2D stabilization

See `creative-arts.animation.blender.stabilization-settings`: 2D Stabilization panel (Anchor Frame, Rotation and Scale toggles, location and rotation/scale track lists, Autoscale and Max, Expected values, Influence, Interpolate), Show Stable in Clip Display, and the Stabilize 2D node (Invert re-applies the shake).

## Follow Track (2D anchor to 3D object)

The **Follow Track** constraint makes an object follow a tracking marker. By default it follows the 2D marker on a plane in the 3D world; **3D Position** uses the reconstructed position (at least eight markers and a solve). **Depth Object** projects the object onto another object's surface and **Undistort** uses the undistorted marker position, both only with 3D Position off. **Link Empty to Track** (Reconstruction menu) creates such empties. **Constraint to F-Curve** on Follow Track, Object Solver and Camera Solver constraints replaces the constraint with equivalent keyframes. See `creative-arts.animation.blender.link-empty-to-track`.

## Gotchas

- Plane track corners that do not sit on the surface edges: add more tracks on the surface (the plane needs at least four).
- A Plane Track Deform image is scaled to the plane relative to the clip; keep the scene resolution consistent with the clip (practice, not from the manual).
- Follow Track in 2D mode does not use the solve, so a grounded object will not show parallax.

## Verify

- Object solve: a cube parented to the empty stays locked to the object.
- Plane track: the preview image stays glued to the surface at the start, middle and end frames.
- Stabilization: Show Stable locks the chosen features in place.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/editing/track, sidebar/track/plane_track, sidebar/stabilization/*, animation/constraints/motion_tracking/*, compositing/types/tracking/*) and the 5.2 source (bl_operators/clip.py, space_clip.py). Fixed: Setup Tracking Scene does not add an Object Solver empty, the old Stabilization option names, Follow Track fields (Active Clip), Depth Object and Undistort only with 3D Position off, Plane Track Deform has Object and Track fields (not Tracking Object), and plane track image lives in the Plane Track panel. Removed unconfirmed: blurred edge compositing tips, Refine unavailable for objects, bake via Ctrl A, and smoothing workflows.
Method: documentation only; no commands were run.
