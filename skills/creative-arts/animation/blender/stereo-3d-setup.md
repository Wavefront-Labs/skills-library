---
id: creative-arts.animation.blender.stereo-3d-setup
name: stereo-3d-setup
category: creative-arts
field: animation
product: blender
tags: [blender, stereoscopy, stereo-3d, stereo-views-setup, views-format, stereo-convergence, interocular]
level: practitioner
status: docs-checked
description: "Render stereo 3D in Blender: enabling Stereoscopy, Stereo 3D vs Multi-View, camera convergence mode, interocular distance, convergence plane, pivot and output formats."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/stereoscopy/usage.html
  - https://docs.blender.org/api/current/bpy.types.CameraStereoData.html
  - https://docs.blender.org/api/current/bpy.types.Stereo3dFormat.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# stereo-3d-setup

Goal: left and right eye renders for stereo delivery.

## Turn it on

Output Properties > enable **Stereoscopy**. Views format (`scene.render.views_format`):
- **Stereo 3D**: a single stereo camera system; adjust the stereo settings in the camera panel.
- **Multi-View**: a multi-camera system where you adjust the cameras individually.
Enabling Stereoscopy also gives a 3D preview in the viewport and extra panels across the interface.

## Camera (Camera properties > Stereoscopy)

- **Convergence Mode**: **Off-Axis** (default; the manual calls it the ideal format, closest to human vision: the pair is separated by the interocular distance and shifted inward to converge on the plane), **Parallel** (parallel cameras with no convergence, needs manual convergence, common when combining real footage with CG), **Toe-in** (rotated cameras; the manual says it is rarely used in modern 3D productions).
- **Interocular Distance**: distance between the cameras. Python default 0.065. Different values change what each eye sees through occlusion, so it cannot be fully fixed in post.
- **Convergence Plane Distance**: where the pair converges; Python default 1.95. Often the projector-to-screen distance. Visualise it in the 3D Viewport.
- **Pivot**: Left, Right or Center. Center builds a new camera for each eye around the active camera; Left or Right keeps the existing camera for one eye (used when only one eye is needed for an existing mono project). Python default is Left.
- Viewport: the 3D Viewport Sidebar stereoscopy panel shows the cameras, convergence plane and volume.

## Output (Output Properties > Views Format)

- **Individual**: separate files per view.
- **Stereo 3D** with a mode: Anaglyph (red-cyan, green-magenta, yellow-blue), Interlace, Side-by-Side (cross-eyed option), Top-Bottom.
Which one to deliver is set by the mastering workflow; ask for the spec (practice).

## Comfort (practice)

- Keep strong out-of-screen effects brief and away from frame edges.
- Animate convergence to follow the subject in long shots.

## Verify

Render one frame as Anaglyph and view it with matching glasses; depth should look natural.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release) render/output/properties/stereoscopy/usage.rst (setup, convergence modes, pivot, interocular, convergence plane, views format modes, viewport panel) and the current Python API (views_format values, interocular default 0.065, convergence distance default 1.95, pivot default Left). Removed: `_L`/`_R` filename suffix claim, vertical-disparity claim for Toe-in, the "convergence at infinity" wording, the multi-view-exr cross-reference detail. Method: documentation only; no commands were run.
