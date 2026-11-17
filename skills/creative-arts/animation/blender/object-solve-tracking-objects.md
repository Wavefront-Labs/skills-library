---
id: creative-arts.animation.blender.object-solve-tracking-objects
name: object-solve-tracking-objects
category: creative-arts
field: animation
product: blender
tags: [blender, object-tracking, object-solve, tracking-object, camera-tracking]
level: practitioner
status: docs-checked
description: "Solve a moving real object in Blender footage: tracking objects in the Objects panel, solving, the Object Solver constraint and Set Inverse, and object scale."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/objects.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/motion_tracking/object_solver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# object-solve-tracking-objects

Goal: CG attached to a moving real object (a prop, a vehicle) with full 3D motion.

## Steps

1. Solve the camera first if it moves (see `creative-arts.animation.blender.camera-tracking`). Camera data is shared between all tracking objects, and refining camera intrinsics happens only when solving camera motion.
2. Sidebar > Track tab > **Objects** panel: the list always holds the camera object (it cannot be deleted and is the only one used for camera solving). Add another object with +; added objects are for object tracking and solving only.
3. With that object active, track at least eight markers on the physical object (the Object Solver manual asks for at least eight).
4. Run **Solve Camera/Object Motion** with the object active. Tracks added to the wrong object can be moved with Track > Copy Tracks and Paste Tracks.
5. For a non-camera object, the Solve tab shows an **Object** panel with **Scale** and **Set Scale** (with an object distance setting) for the object's scale.
6. In the 3D scene add the **Object Solver** constraint to a Blender object (an Empty works): **Active Clip**, **Object** (the tracking object) and **Camera** (leave empty for the active camera; if the real camera moved, the Blender camera needs a Camera Solver constraint). Then use **Set Inverse**.

## Set Inverse (from the manual)

Set Inverse records that the object's current location (with the constraint disabled) is correct for the current frame. When adding the constraint: bring the object into position for the current frame, add the constraint, click Set Inverse. To tweak later: Apply Visual Transform, disable the constraint, adjust, click Set Inverse, enable the constraint. **Clear Inverse** resets the stored transform. **Constraint to F-Curve** replaces the constraint with keyframes.

## Notes

- Setup Tracking Scene does not create object-solver empties; it builds the camera, reference objects and compositing setup (see `creative-arts.animation.blender.setup-tracking-scene`).
- The solved object motion is relative to the camera. Rigid features help; faces and other deforming surfaces are poor candidates (practice, not from the manual).

## Verify

Parent a test cube to the solved empty at the object. Over the footage it stays locked to the object as it moves.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/sidebar/track/objects, animation/constraints/motion_tracking/object_solver, movie_clip/tracking/clip/editing/track) and the 5.2 source (space_clip.py Solve tab Object panel). Confirmed the Objects panel rules, eight-marker minimum, Object Solver fields, Set Inverse and Clear Inverse. Removed unconfirmed claims about rotation requirements and drift deletion. Corrected the constraint field name (Active Clip, not Clip).
Method: documentation only; no commands were run.
