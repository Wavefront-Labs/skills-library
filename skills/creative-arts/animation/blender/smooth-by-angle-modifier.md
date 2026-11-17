---
id: creative-arts.animation.blender.smooth-by-angle-modifier
name: smooth-by-angle-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, normals, smooth-by-angle, shade-auto-smooth, smooth-by-angle-modifier, sharp-edges-attribute, auto-smooth-migration]
level: practitioner
status: docs-checked
description: "Replace legacy Auto Smooth in Blender 4.1+: Shade Auto Smooth (Smooth by Angle modifier), Mark Sharp, sharp_edge and sharp_face data, and why modifier order matters."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/smooth_by_angle.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/shading.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/edge_data.html
  - https://developer.blender.org/docs/release_notes/4.1/modeling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# smooth-by-angle-modifier

Goal: smooth shading with crisp hard edges in Blender 4.1+, where mesh *Auto Smooth* no longer exists.

## What changed in 4.1

- The mesh *Auto Smooth* checkbox was removed. Sharpness is now data: boolean attributes `sharp_edge` (edges) and `sharp_face` (flat faces). Custom normals no longer need auto smooth enabled.

## Two ways to get angle-based smoothing

1. **Object > Shade Auto Smooth**: adds the *Smooth by Angle* modifier (a geometry nodes asset from the bundled Essentials library) with *Angle* and *Ignore Sharpness* options. The modifier is pinned to the last position in the stack, and the operator's *Auto Smooth* checkbox removes it again.
2. **Mark sharp edges yourself**: *Edge > Mark/Clear Sharp* in Edit Mode writes the `sharp_edge` attribute. Edges marked Sharp are left alone by the Smooth by Angle and Weighted Normal modifiers (unless *Ignore Sharpness* smooths them). The 4.1 release notes also list *Set Sharpness by Angle* (Edit Mode) and *Shade Smooth by Angle* operators; the 5.2 manual and Object menu do not list them, so check your version.

## Manual control

- Edit mode: `Ctrl E` (Edge menu) > *Mark/Clear Sharp*.
- Face mode: *Shade Flat/Smooth* per face (sets `sharp_face`).
- Geometry Nodes can write the same data with the *Set Shade Smooth* node (edge and face smoothness correspond to `sharp_edge` and `sharp_face`).

## Gotchas

- *Shade Smooth* and *Shade Flat* also remove any Smooth by Angle modifier on the object; *Keep Sharp Edges* keeps the Sharp marks so a revert stays possible.

## Verify

Toggle the modifier: shading changes on only the intended edges; Overlays > *Split Normals* show split lines at sharp edges.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Shading, Smooth By Angle modifier, Edge Data and Set Shade Smooth pages), the 5.2 Object menu script (space_view3d.py) and the Blender 4.1 modeling release notes. Confirmed: Auto Smooth replaced by a modifier node group asset in 4.1; Shade Auto Smooth adds the pinned Smooth by Angle modifier with Angle and Ignore Sharpness; Mark/Clear Sharp stores sharp_edge; Set Shade Smooth node maps to sharp_edge and sharp_face; Shade Smooth and Shade Flat remove the modifier and have Keep Sharp Edges. Corrected: the Attributes panel does not list built-in attributes such as sharp_edge, and Shade Smooth by Angle is not in the 5.2 Object menu. Removed as unconfirmed: automatic modifier insertion for old files, exporter normals behaviour and duplicate node groups.

Method: documentation only; no commands were run.
