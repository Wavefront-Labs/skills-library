---
id: creative-arts.animation.pipeline.camera-interchange
name: camera-interchange
category: creative-arts
field: animation
product: pipeline
tags: [camera-interchange, interchange-formats, focal-length, film-back, sensor-size, camera-export, nuke-camera, after-effects-camera, alembic-camera, fbx-camera]
level: advanced
status: draft
description: "Move shot cameras between Maya/Blender/Houdini, Nuke and After Effects without drift: focal length plus film back, fit modes, overscan, frame offsets and formats."
sources:
  - https://learn.foundry.com/nuke/content/reference_guide/3d_nodes/camera.html
  - https://docs.blender.org/manual/en/latest/render/cameras.html
  - https://docs.alembic.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera interchange

**Goal:** comp, motion graphics and lighting all see through exactly the same camera as layout and animation,
so 3D elements, projections and tracked graphics line up to the pixel.

## What must match

| Parameter | Note |
|---|---|
| Focal length | mm |
| Film back / sensor size | width and height in mm (or inches in Maya: 1.417 x 0.945 in = 36 x 24 mm) |
| Fit / gate mode | horizontal vs vertical fit (Blender Sensor Fit, Maya Film Fit) |
| Resolution and pixel aspect | output raster, overscan if used |
| Transform per frame | baked, world space |
| Frame numbering | start frame (1001 vs 1) and time offsets |
| Near/far clip, focus distance, f-stop | for DOF and depth comps |

Focal length alone is not enough: angle of view depends on film back and fit.

## Formats

- **Alembic camera** (best for Maya/Houdini/Nuke/Blender): carries transform and lens data per frame.
- **FBX camera**: works with After Effects (via importers), engines; check film back conversions.
- **Nuke**: ReadGeo/Camera node reads Alembic/FBX cameras directly.
- **After Effects**: no native Alembic camera; import via the Cinema 4D route, an FBX/JSON importer script,
  or export AE-compatible keyframes (zoom in pixels = focal length x comp width / film back width).

## Overscan

When rendering overscan (extra pixels for distortion or camera shake), adjust film back proportionally
(film back x overscan factor) and resolution, or comp cameras won't match the plate.

## Gotchas

- Blender's sensor fit "Auto" switches axis with aspect; set explicit Horizontal to avoid surprises.
- Maya "Fill" vs "Horizontal" fit changes the angle of view on non-matching aspect ratios.
- Unbaked cameras with constraints or parents export only their local animation; bake to world space.

## Verify

Render a frame of a reference grid/cube in the source app and re-render the same object through the imported
camera in the target app: overlay difference shows no offset at frame start, middle and end.
