---
id: creative-arts.animation.blender.camera-shift
name: camera-shift
category: creative-arts
field: animation
product: blender
tags: [blender, camera, camera-shift, lens-shift, shift-x, architectural-visualization]
level: practitioner
status: verified
description: "Use Blender camera lens shift for perspective correction: two-point architectural verticals, reframing without rotation, shift units and matching tilt-shift."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/camera.html
  - https://docs.blender.org/api/current/bpy.types.Camera.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# camera-shift

Goal: straight verticals in architecture, and reframes that keep the camera's perspective.

## Shift X / Y
Camera Data > Lens > **Shift X / Shift Y**: adjusts the vanishing points: the frame slides while perspective does not change. The manual notes that lens shift is equivalent to rendering a larger FOV and cropping off-center. Horizontal and vertical shift default to 0.0 (Python `shift_x` / `shift_y`). Measured (Blender 4.5.14): in a 64 px frame Shift X 0.25 moved a cube 16 px left and Shift Y 0.25 moved it 16 px down; in a 128x64 frame Shift X 0.25 moved it 32 px, so shift is a fraction of the larger image dimension, and positive values move the subject left / down. An orthographic camera shifted the same way.

## Two-point perspective (architecture)
1. Camera rotation X = 90 deg exactly (level, no tilt), so verticals stay parallel.
2. Building too high in frame -> raise **Shift Y** instead of tilting up: the frame slides without rotating the camera (in a 4.5.14 test the cube kept the same size and shape in pixels, only its position changed), whereas tilting changes the projection.
3. Composition retains parallel verticals like a tilt-shift lens.

## Other uses
- Reframing a locked-off camera tracked solve without changing the solve.
- Matching real lenses with shift (tilt-shift) in VFX.

## Gotchas
- In Orthographic mode lens shift is equivalent to translating the camera.
- Tracking solves use the Optical Center (principal point) set in the clip Camera panel; confirm it matches any lens shift.

## Verify
Camera view with the Center composition guide: verticals parallel to frame edges.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Shift description, lens shift vs rotation figure note, orthographic note); movie_clip camera panel (Optical Center); Python API 5.2 Camera.shift_x/shift_y default 0.0. Removed unconfirmed shift units, example values, stretching limit and focus-plane claims.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: shift_x/shift_y defaults 0.0; Workbench renders of a cube at 64x64 and 128x64 gave the pixel shifts above (perspective and orthographic). Unrun (documentation only): the 'equivalent to a larger FOV and cropping' note, the tracking Optical Center remark, and tilt-shift matching.

Method: manual text confirmed from documentation; shift behaviour run headless in Blender 4.5.14.
