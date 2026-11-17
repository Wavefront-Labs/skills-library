---
id: creative-arts.animation.blender.volume-display-settings
name: volume-display-settings
category: creative-arts
field: animation
product: blender
tags: [blender, volume-object, openvdb, vdb, volume-display, volume-slice, volume-wireframe, viewport-performance]
level: practitioner
status: docs-checked
description: "Keep heavy OpenVDB volumes responsive in Blender's viewport: Viewport Display Wireframe, Detail, Density, Interpolation and Slice settings."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/volumes/properties.html
  - https://projects.blender.org/blender/blender/src/branch/main/source/blender/makesrna/intern/rna_volume.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# volume-display-settings

Goal: work with large VDB caches without the viewport crawling, and inspect their interior.

## Object Data > Viewport Display (volume object)
- **Wireframe**: how the volume is represented in wireframe shading. For heavy volumes the manual suggests setting the object to always display as wireframe: the viewport stays responsive and the volume still appears in the final render. Options: *None*, *Bounds* (single bounding box for the entire grid), *Boxes* (boxes for nodes in the volume tree), *Points* (points for nodes in the tree).
- **Detail** (for Boxes or Points): *Coarse* shows one box or point per intermediate tree node; *Fine* shows one per leaf node containing 8x8 voxels.
- **Density**: thickness of the volume in the 3D Viewport only; render density comes from the shader (Principled Volume). The property range starts just above zero.
- **Interpolation**: *Linear* (good smoothness and speed), *Cubic* (smoother, slower), *Closest* (no interpolation, raw voxels).
- **Slice** (checkbox with **Axis** and **Position**): shows a single 2D section of the volume. Axis: *Auto* (follows the view direction), X, Y, Z. Position (0 to 1) is relative to the length of that side.

## Gotchas
- A very low viewport Density makes the volume nearly invisible in the viewport while the render is unchanged.
- Viewport Display settings never change the render.

## Verify
Enable Slice and move Position through the volume: interior values look as expected.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Volume Properties page, branch blender-v5.2-release; enum labels and ranges from rna_volume.cc on the Blender main branch. Confirmed: all options and meanings above. Removed unconfirmed claims: Preferences Limit Size advice, partial grid loading, proxy VDB workflow, fps targets, Workbench Solid colour remarks, and the Slice Depth label (the UI label is Position).
Method: documentation only; no commands were run.
