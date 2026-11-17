---
id: creative-arts.animation.blender.hair-node-groups
name: hair-node-groups
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-node-groups, hair-assets, procedural-hair, geometry-nodes]
level: practitioner
status: docs-checked
description: "Use Blender hair nodes as Geometry Nodes modifiers: the Generation, Guides, Deformation, Read, Utility and Write categories and how to stack them."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/index.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/generation/generate_hair_curves.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/utility/attach_hair_curves_to_surface.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/write/set_hair_curve_profile.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/scripts/startup/bl_ui/properties_data_modifier.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hair-node-groups

Hair Nodes are Geometry Nodes assets. The manual groups them as follows (all for curves, typically hair):

- **Generation**: Generate Hair Curves, Interpolate Hair Curves, Duplicate Hair Curves.
- **Guides**: Braid Hair Curves, Clump Hair Curves, Create Guide Index Map, Curl Hair Curves.
- **Deformation**: Blend, Displace, Frizz, Hair Curves Noise, Roll, Rotate, Shrinkwrap, Smooth, Straighten, Trim Hair Curves.
- **Read**: Curve Info, Curve Root, Curve Segment, Curve Tip, Hair Attachment Info.
- **Utility**: Attach Hair Curves to Surface, Redistribute Curve Points, Restore Curve Segment Length.
- **Write**: Set Hair Curve Profile (radius along each curve: Replace Radius, Radius, Shape, Factor Min at root, Factor Max at tip).

## Where
Essentials node assets are offered in the Add Modifier menu for Curves objects, with asset catalogs listed after the built-in submenus; each becomes a Geometry Nodes modifier. Several nodes need a surface mesh and UV map: Generate Hair Curves and Attach Hair Curves to Surface state they require valid Surface input and a Surface UV Map.

## Using them
- Stack modifiers top to bottom; each takes the previous result as its Geometry input.
- Where a node follows Deform Curves on Surface, enable **Resting Surface** (documented as Surface Rest Position in some tips) so pre-deformed coordinates are used.
- Use Viewport Amount inputs to keep viewport density low.
- Share one guide map via Create Guide Index Map across Clump, Curl and Braid.

## Verify
Toggle each modifier: each step adds its look, and render uses the full density inputs.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Compared the category and node lists with the Hair Nodes index pages; Clump and Curl are Guides nodes, Noise is Hair Curves Noise, and Blend Hair Curves is a Deformation node (the old list had them in other categories). The Add Modifier asset menu mechanism was confirmed from the 5.2 modifier UI script, but the catalog label shown there was not, so no label is claimed. Removed the Add > Hair path, the append-versus-link note and the recommended stack order.
Method: documentation only; no commands were run.
