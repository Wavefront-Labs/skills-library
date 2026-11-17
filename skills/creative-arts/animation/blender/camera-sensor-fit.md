---
id: creative-arts.animation.blender.camera-sensor-fit
name: camera-sensor-fit
category: creative-arts
field: animation
product: blender
tags: [blender, camera, camera-sensor-fit, sensor-fit, sensor-width, match-real-camera]
level: practitioner
status: verified
description: "Match Blender cameras to real cameras: sensor width/height, sensor fit Auto/Horizontal/Vertical, focal length equivalence and portrait-resolution pitfalls."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/camera.html
  - https://docs.blender.org/api/current/bpy.types.Camera.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# camera-sensor-fit

Goal: identical field of view to the physical camera or another DCC.

## Sensor
Camera Data > Camera > **Sensor Fit** + **Size** (Width/Height). The Python API gives sensor width default 36 mm and sensor height default 24 mm. Take the sensor size from the camera's specification; the Camera panel has **Presets** to match real-world cameras.

## Sensor Fit
- **Auto**: a square sensor of the single Size value (Python `sensor_width`; `sensor_height` is ignored) is applied to the larger of the Resolution dimensions. For landscape outputs the horizontal field of view therefore stays the same when the aspect changes (50 mm lens, 36 mm: 39.6 degrees at 1920x1080 and 1440x1080; only the vertical view changes). It jumps when the larger dimension flips, e.g. 1080x1920 portrait gives 22.9 degrees horizontal.
- **Horizontal**: you set the sensor Width; the height follows the output aspect ratio. **Vertical**: you set the Height; the width follows the aspect ratio.

## Matching
- Use the recorded/active sensor area at the shooting resolution (video modes can crop the sensor).
- Focal length + sensor width -> horizontal FOV = 2 * atan(w / (2 f)).
- Tracking: the Movie Clip editor Track tab > Camera panel holds Sensor Width, Focal Length and Optical Center; its presets do not include distortion coefficients or principal point.

## Gotchas
- Wrong sensor width with correct focal length = wrong FOV; solves drift.
- When exporting cameras to other applications, check that the film back (sensor size) matches.
- With Auto fit, switching between landscape and portrait changes the horizontal FOV (39.6 to 22.9 degrees for 50 mm / 36 mm); landscape-to-landscape aspect changes keep it. Pick Horizontal or Vertical explicitly when delivering both.

## Verify
Render a frame and overlay the plate: straight lines and object scale match edge to edge.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Sensor Fit, Size) and movie_clip/tracking/clip/sidebar/track/camera; Python API 5.2 Camera.sensor_width default 36, sensor_height default 24. Replaced unconfirmed sensor-size table and Auto-fit description (manual: square sensor from larger dimension), removed DCC-convention and Setup Tracking Scene claims.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: defaults sensor_width 36, sensor_height 24; Sensor Fit enum AUTO, HORIZONTAL, VERTICAL; camera.view_frame() gave 2*atan(36/(2*50)) = 39.6 degrees and the Auto/Horizontal/Vertical field-of-view figures above for 1920x1080, 1440x1080 and 1080x1920; Workbench renders of a cube: Auto ignored sensor_height (5 mm or 24 mm gave 18 px), Vertical used it (24 mm gave 14 px, 12 mm gave 28 px), Horizontal used sensor_width (36 mm 18 px, 18 mm 38 px); the Camera panel source shows Size for Auto, Width for Horizontal, Height for Vertical. Unrun (documentation only): the Movie Clip Camera panel and presets, sensor-crop advice and DCC export remarks.

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
