---
id: creative-arts.animation.blender.hair-surface-attachment
name: hair-surface-attachment
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-surface-attachment, surface-deform-hair, snap-to-surface-hair, deform-curves-on-surface]
level: practitioner
status: docs-checked
description: "Attach Blender Curves hair to a surface mesh: Surface and UV Map, Deform Curves on Surface, rest position, Attach Hair Curves to Surface and snapping."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/deform_curves_on_surface.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/utility/attach_hair_curves_to_surface.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/introduction.html
  - https://docs.blender.org/api/current/bpy.types.Curves.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hair-surface-attachment

## Requirements
- Curves Data > **Surface** panel: **Surface** (the mesh object) and **UV Map** (UV map on that mesh used for attachment).
- **Deform Curves on Surface** node: translates and rotates each curve from the change in its root position, using the UV coordinates stored per curve (attribute surface_uv_coordinate) and the surface settings. It compares the original mesh (before shape keys and modifiers) with the final mesh, so it only works for Curves objects, and it reads a rest_position attribute for consistent tangents.
- Mesh Object Data > Shape Keys panel: **Add Rest Position** option (property add_rest_position_attribute) stores the rest position on the mesh.
- If a Subdivision Surface modifier is on the surface, set its UV Smooth to None, otherwise the surface UV map is subdivided in a way that can invalidate stored attachment points.

## Attach Hair Curves to Surface node
Inputs: Surface Source (Attached, Object, Input), Surface Geometry or Object (its transforms must match the modifier object), Surface UV Map, Resting Surface (enable if Deform Curves on Surface comes later), Use Existing Attachment; Snap to Surface group with Blend along Curve and Align to Surface Normal. Outputs Surface UV Coordinate and Surface Normal.

## Snapping in Sculpt Mode
Curves menu: **Snap to Deformed Surface** re-attaches using existing attachment info (works only if the surface topology did not change); **Snap to Nearest Surface** moves each root to the nearest surface point and is needed after topology changes.

## Verify
Pose the rig: roots stay on the scalp; changing the surface UV map breaks attachment, confirming the UV dependency.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed the Deform Curves on Surface implicit inputs and warning, Attach Hair Curves to Surface inputs, the Snap to Deformed/Nearest Surface descriptions, and the Surface and UV Map fields plus the mesh Add Rest Position property in the 5.2 UI scripts. Removed unconfirmed overlapping-UV and modifier-order claims.
Method: documentation only; no commands were run.
