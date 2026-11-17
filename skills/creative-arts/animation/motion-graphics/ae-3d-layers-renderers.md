---
id: creative-arts.animation.motion-graphics.ae-3d-layers-renderers
name: ae-3d-layers-renderers
category: creative-arts
field: animation
product: motion-graphics
tags: [3d-layers, ae-3d, after-effects, advanced-3d, classic-3d, cinema-4d-renderer, 3d-models, camera-layer, depth-of-field, extrusion]
level: practitioner
status: draft
description: "Work with After Effects 3D layers: choosing Classic 3D, Cinema 4D or Advanced 3D renderers, cameras and depth of field, imported 3D models, and common depth sorting issues."
sources:
  - https://helpx.adobe.com/after-effects/using/3d-layers.html
  - https://helpx.adobe.com/after-effects/using/3d-renderers.html
  - https://helpx.adobe.com/after-effects/using/cameras-lights-points-interest.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 3D layers and renderers

**Goal:** parallax, depth and simple 3D in motion graphics without leaving AE: 2.5D layered scenes,
extruded type, imported 3D models.

## Renderers (Composition Settings - 3D Renderer)

| Renderer | Strengths | Limits |
|---|---|---|
| Classic 3D | fast, flat layers in 3D space, shadows from lights | no extrusion, no real geometry |
| Cinema 4D | extruded/bevelled text and shapes | slower, deprecated in favour of Advanced 3D |
| Advanced 3D | GPU, imported GLB/GLTF/OBJ/FBX models, image-based lighting, extrusion, DOF | some effects/blend modes behave differently |

## 2.5D parallax setup

1. Make layers 3D (cube switch). Place backgrounds far (Z +2000), midground, foreground near (Z -500).
2. Add a Camera (Layer - New - Camera), 35-50 mm preset. Animate the camera, not the layers.
3. Scale far layers up to compensate for distance so they fill frame.
4. Depth of field: camera options - Depth of Field on, Focus Distance (link to a null via expression
   or "Link Focus Distance to Layer"), Aperture for blur amount.

## Camera rig

Parent the camera to a null for dolly/pan; use a second null for rotation pivots. Two-node cameras
(with Point of Interest) flip when crossing straight up/down; one-node cameras plus nulls avoid that.

## Gotchas

- Precomps break 3D unless Collapse Transformations is enabled; collapsed precomps join the parent's 3D
  space.
- Adjustment layers and some blend modes split the 3D render order (layers above/below a 2D layer are
  rendered in separate 3D groups); intersections between groups don't sort.
- Continuously rasterised vector layers in 3D can render soft at extreme Z; check final resolution.
- Large Z distances with motion blur increase render time sharply.

## Verify

Orbit with the camera in a custom view to check layer order and gaps, then render a frame at full
quality: correct depth sorting, DOF focused on the intended layer.
