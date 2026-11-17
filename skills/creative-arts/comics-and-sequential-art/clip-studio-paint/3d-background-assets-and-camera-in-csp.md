---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.3d-background-assets-and-camera-in-csp
name: 3d-background-assets-and-camera-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-3d, csp-3d-background, 3d-camera, perspective-ruler, background-assets, clip-studio-assets]
level: advanced
status: draft
description: "Build comic backgrounds from 3D assets in Clip Studio Paint: placing background models, camera angle and lens, matching panels, creating a perspective ruler and lighting."
sources:
  - https://assets.clip-studio.com/en-us/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 3D background assets and camera

## Place a background
- Material palette > **3D > Background** (classroom, street, rooms) or download from Clip Studio Assets
  (filter: 3D). Drag into the panel; a 3D layer is created inside the frame folder.
- Import your own `.fbx`, `.obj`, `.lwo`, `.lws`, `.pmd`/`.pmx` or `.vrm` models via File > Import > 3D
  data (formats depend on version).

## Camera
- **Object** tool on the 3D layer: the camera manipulator at the top rotates, pans, dollies.
- Tool property > **Camera**: perspective (focal length / field of view); low values = telephoto flat look,
  high = dramatic wide angle. Match the shot type in the script.
- Camera presets in Tool property; save angles via the 3D layer's camera settings to reuse across panels.
- Shift a single model part (desks, chairs) by selecting it in the object list; hide parts that block the shot.

## Perspective ruler
- **Layer > Ruler/Frame > Create perspective ruler** (with the 3D layer selected) makes a perspective ruler
  matching the camera, so hand-drawn characters and props snap to the same perspective.

## Light
- Tool property > Light source: direction and shadow on/off for consistent lighting across panels.

## Finishing
- Use as a reference (low opacity) and ink by hand, or LT conversion (EX) to line and tone.

## Gotchas
- Raw 3D renders look sterile; add hand-drawn clutter, wear, people.
- Large models slow the file; delete unused parts or merge to raster after the panel is final.
- Asset licences differ: check commercial-use terms.

## Verify
- [ ] Camera matches the established eye level across the scene's panels.
