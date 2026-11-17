---
id: creative-arts.animation.blender.camera-clipping
name: camera-clipping
category: creative-arts
field: animation
product: blender
tags: [blender, camera, camera-clipping, clip-start, clip-end, z-fighting, depth-precision]
level: practitioner
status: verified
description: "Set Blender camera and viewport clip start/end correctly: z-fighting and depth precision, large-scale scenes, mist range, and cut-away clipping tricks."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/sidebar.html
  - https://docs.blender.org/api/current/bpy.types.Camera.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# camera-clipping

Goal: no missing geometry, no flickering surfaces, and controlled cut-aways.

## Two different clip settings
- **Camera** Data > Lens > **Clip Start / Clip End**: used in camera view and renders.
- **Viewport** N panel > View > **Clip Start / End**: for non-camera views (user perspective).
Camera defaults per the Python API: Clip Start 0.1, Clip End 1000.

## Depth precision
EEVEE/viewport use a depth buffer: precision depends mostly on the **start/end ratio**, and is dominated by Clip Start. The manual warns that a large clipping range reduces depth precision and causes artifacts, so for viewport rendering keep the range limited; ray-traced renders do not suffer from this issue so much and tolerate more extreme values. For flicker on distant surfaces, raise Clip Start first, then lower Clip End.

## Large scenes
Landscapes/space: raise Clip Start as far as the framing allows, or split into foreground/background cameras and composite.

## Cut-away renders
Clip Start larger than the distance to a wall: the wall is not directly visible (interior shots). Measured (Workbench, Blender 4.5.14): a cube 9.5 to 10.5 m from the camera vanished with Clip Start 11 or Clip End 9, and was cut through (smaller silhouette) with Clip Start 10. Per the manual, objects outside the clip range still influence the image indirectly, as further light bounces are not clipped.

## Mist
Mist pass range is set in World > Mist Pass (`world.mist_settings`: Start default 5, Depth default 25, Falloff Quadratic/Linear/Inverse Quadratic), not by camera clipping.

## Gotchas
- Geometry disappearing when zooming in the viewport = viewport Clip Start; change it in the N panel (View tab), not on the camera.
- Enable Camera Data > Viewport Display > **Limits** to see the clip bounds on the camera.

## Verify
Fly through the scene in camera view: no popping near or far, no flicker on distant coplanar surfaces.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Clip Start/End note, Show Limits, Mist), editors/3dview/sidebar (viewport Clip Start/End, precision warning); Python API 5.2 Camera.clip_start default 0.1, clip_end default 1000. Removed unconfirmed unit-scale and EEVEE shadow claims and example ranges.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: Camera clip_start 0.1, clip_end 1000, Show Limits property (labelled Limits in the UI source); clipping renders as above; WorldMistSettings defaults and the Mist Pass panel from the UI source. Unrun (documentation only): the depth-precision warning, ray-tracing tolerance, indirect-light note, viewport N-panel Clip fields.

Method: manual text confirmed from documentation; clipping run headless in Blender 4.5.14.
