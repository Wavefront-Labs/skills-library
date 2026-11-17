---
id: creative-arts.animation.blender.camera-solver-constraints
name: camera-solver-constraints
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, camera-solver-constraint, follow-track-constraint, object-solver-constraint, motion-tracking, matchmove]
level: practitioner
status: docs-checked
description: "Apply Blender motion-tracking solves with constraints: Camera Solver, Object Solver (set inverse) and Follow Track (2D track to 3D, depth object, 3D position)."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/motion_tracking/camera_solver.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/motion_tracking/object_solver.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/motion_tracking/follow_track.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# camera-solver-constraints

Goal: connect a Movie Clip solve to the 3D scene. Solving itself is in `camera-tracking` / `object-tracking-stabilization`.

## Camera Solver

- Track at least eight markers in the Movie Clip Editor, run Solve Camera Motion, then add the constraint to a Blender camera so it imitates the real camera.
- **Active Clip**: follow the scene's active clip; unchecked, a selector appears for another clip.
- **Constraint to F-Curve** replaces the constraint with an equivalent set of keyframes, for hand editing.

## Object Solver

- For a physical object registered in the clip's tracking objects, with at least eight markers tracked on it and the solve run. Add the constraint to a Blender object: **Object** = the physical object to imitate, **Camera** = the Blender camera that matches the recording camera (empty uses the scene's active camera; give it a Camera Solver if the real camera moved).
- **Set Inverse**: tells the constraint that the object's current location (constraint disabled) is correct for the current frame. Add flow: position the object, add the constraint, click Set Inverse. To tweak later: Apply Visual Transform, disable the constraint, adjust the object, click Set Inverse, enable the constraint. **Clear Inverse** resets the stored relative transform.

## Follow Track

- Makes an object imitate a tracking marker. By default it follows the marker's 2D motion on a plane in the 3D world; **3D Position** uses the reconstructed world position of the marker (needs at least eight markers and a solve).
- Fields: **Active Clip**, **Object** (empty lists the markers used for the camera), **Track**, **Camera** (empty uses the scene's active camera), **Depth Object** (projects the object onto its surface, for example facial makeup; not with 3D Position), **Undistort** (compensate lens distortion; not with 3D Position), **Frame Method** (Stretch, Fit, Crop) for aspect ratio differences between the footage and the render.
- A Movie Clip Editor button (the track-to-empty operator) creates an Empty with this constraint in one click.

## Gotchas

- Constraint to F-Curve replaces the constraint with keyframes, so the link to the clip is gone; keep an unbaked copy.
- Frame Method on the constraint should match the camera background's Frame Method (set from Set as Background in the Movie Clip Editor).

## Verify

Viewport camera view with clip background: 3D markers (bundles) sit on features through the shot; inserted objects don't slide.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Camera Solver, Object Solver and Follow Track constraint pages: eight-marker requirement, Active Clip, Constraint to F-Curve, Object, Camera, Set Inverse procedure, Clear Inverse, Follow Track fields (3D Position, Undistort, Frame Method, Depth Object) and Track to Empty. Removed the unconfirmed Setup Tracking Scene, orientation tools, clip start frame and sensor remarks.

Method: documentation only; no commands were run.
