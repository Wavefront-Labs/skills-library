---
id: creative-arts.animation.blender.xray-wireframe-shading
name: xray-wireframe-shading
category: creative-arts
field: animation
product: blender
tags: [blender, workbench, xray-wireframe, x-ray, wireframe-opacity, viewport-shading]
level: practitioner
status: docs-checked
description: "Use X-ray and wireframe display in the Blender 3D viewport: Alt Z and Shift Z toggles, X-ray opacity slider, wireframe overlay threshold and opacity."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/shading.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# xray-wireframe-shading

Goal: see and select through geometry when modelling, rigging or reviewing.

## Toggles

- **Alt Z**: X-Ray, in the shading popover Options. It makes objects transparent so you can see and select items that would otherwise be occluded; the slider controls object opacity.
- **Shift Z**: switches between the current shading mode and Wireframe.
- **Z** opens the pie menu for changing shading mode.
- Wireframe shading shows only object edges; *Wireframe Color* (theme, object, random and so on) affects both the Wireframe shading mode and the overlay.

## Wireframe overlay

Viewport Overlays, Geometry, **Wireframe**: displays mesh edges on top of existing shading. The value slider picks which edges show (lower values hide edges on almost flat surfaces, 1 shows all). **Opacity** runs from 0 (invisible) to 1 (opaque).

Bone Wireframe Opacity sets the maximum opacity of bones drawn in Wireframe shading or in Solid shading with X-Ray active, which helps reduce clutter and focus on the mesh.

## Gotchas

- Workbench final renders have their own X-Ray option in Render properties, separate from the viewport; left on, it renders the whole scene transparent.
- The Wireframe overlay is not the same as Wireframe shading: it draws on top of existing shading.

## Checked

Method: 2026-11-09 read the Blender manual source for Viewport Shading and (via search of) Overlays; removed per-mode X-ray state, In Front, Retopology overlay and use-case claims not stated there.
