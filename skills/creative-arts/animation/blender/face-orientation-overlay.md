---
id: creative-arts.animation.blender.face-orientation-overlay
name: face-orientation-overlay
category: creative-arts
field: animation
product: blender
tags: [blender, normals, face-orientation-overlay, face-orientation, normals-display, overlays, backface-culling]
level: practitioner
status: docs-checked
description: "Inspect normals in Blender's viewport: Face Orientation overlay (blue/red), Normals overlay for vertex, split and face normals with size, and Backface Culling for checking."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/shading.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# face-orientation-overlay

Goal: see normal problems before they show up in renders, bakes or game engines.

## Face Orientation (Overlays popover > Geometry)

- Face Orientation highlights the backside of faces in red (the front side is shown in blue in the default theme, practice). A face shown red on the outside of a mesh is most likely oriented incorrectly and needs its normal flipped.
- Fix with the Flip or Recalculate Outside normals operators for meshes (the manual names both); Surface objects use the Switch Direction operator.

## Normals overlay (Edit mode, Mesh Edit Mode overlays popover > Normals)

- Display **Vertex Normals**, **Split Normals** (the manual's "face normals at vertices"), or **Face Normals**.
- **Size** sets the displayed length; *Constant Screen Size Normals* keeps the size constant relative to zoom.
- Split Normals are useful for checking sharp edges and custom normals (practice).

## Backface Culling (Viewport Shading popover > Options)

- *Backface Culling* hides the backsides of faces in the viewport, so flipped faces and interiors drop out of view (practice).

## Related overlays

- *Statistics* for counts, *Mesh Analysis* (Edit mode) for intersect/distortion/thickness/sharp, *Wireframe* to read topology.

## Gotchas

- A single-sided plane (a leaf card) shows red from its back side by design.
- The overlay shows the face orientation of the mesh, not shader normal maps or bump (practice).

## Verify

Toggle Face Orientation on a finished asset and orbit it: no red should be visible from the outside.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against editors/3dview/display/overlays.rst (Face Orientation wording and the flip/recalculate operators, Normals overlay with Size and Constant Screen Size Normals) and editors/3dview/display/shading.rst (Backface Culling). Removed the theme path, the 4.x gate, the EEVEE material claim and the negative-scale claim as unconfirmed.

Method: documentation only; no commands were run.
