---
id: creative-arts.animation.blender.camera-lens-types
name: camera-lens-types
category: creative-arts
field: animation
product: blender
tags: [blender, camera, camera-lens-types, orthographic-camera, panoramic-camera, fisheye]
level: practitioner
status: docs-checked
description: "Choose Blender camera types: perspective focal length vs FOV, orthographic scale, and Cycles panoramic (equirectangular, fisheye, mirror ball) setups."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/cameras.html
  - https://docs.blender.org/api/current/bpy.types.Camera.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# camera-lens-types

Goal: the right projection for the deliverable (shot, ortho asset render, 360/fulldome).

## Perspective
Lens Unit: **Millimeters** (focal length) or **Field of View** (angle). Longer focal lengths give a smaller field of view (more zoom). The manual notes that decreasing Focal Length while the camera moves toward an object produces a Dolly Zoom effect.

## Orthographic
**Orthographic Scale** controls the apparent size of objects; objects keep their size regardless of distance and parallel lines stay parallel. Per the manual it is effectively the only setting that applies, and lens shift is equivalent to translating the camera. Uses: isometric game art, technical drawings, UI renders.

## Panoramic (Cycles only)
Panorama Type:
- **Equirectangular**: always the full 360 degrees horizontally and 180 vertically, compatible with the world Environment Texture (camera rotation (90, 0, -90) matches the default mapping); has Latitude/Longitude Min/Max.
- **Equiangular Cubemap Face**: more uniform pixel distribution than equirectangular, suited to VR; no latitude/longitude limits.
- **Mirror Ball**: renders as a photo of a reflective ball.
- **Fisheye Equidistant** (ignores sensor info, good for full-dome) / **Fisheye Equisolid** (best matches real cameras: Lens mm and Field of View, uses sensor size) / **Fisheye Lens Polynomial** (4th-degree polynomial coefficients to mimic a real lens).
- **Central Cylindrical**: projection onto a virtual cylinder from its centre.

## Gotchas
- Panoramic cameras are Cycles only and cannot be displayed in non-rendered viewport modes such as Solid.
- The Camera API lists the panorama default as Fisheye Equisolid.

## Verify
Render a test with a ground grid: ortho shows parallel lines; an equirectangular render wraps left to right.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Perspective, Orthographic, Shift note) and render/cycles/object_settings/cameras (panorama types and notes); Python API 5.2 Camera.panorama_type enum and default. Removed unconfirmed typical focal lengths, isometric angles, resolution and EEVEE/DOF claims.
Method: documentation only; no commands were run.
