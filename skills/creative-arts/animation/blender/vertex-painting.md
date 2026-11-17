---
id: creative-arts.animation.blender.vertex-painting
name: vertex-painting
category: creative-arts
field: animation
product: blender
tags: [blender, vertex-paint, vertex-color, color-attributes, color-attribute, sculpt-vertex-colors, ao-bake-to-vertex, game-masks, attribute-node, byte-color, id-masks]
level: practitioner
status: docs-checked
description: "Paint and use colour attributes in Blender: Vertex Paint brushes and menu, Byte/Float and Vertex/Face Corner types, Solid view, shaders, baking, glTF and FBX export."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/vertex_paint/introduction.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/object_data.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/vertex_color.html
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# vertex-painting

Goal: store per-vertex colour data (masks, IDs, tints) without UVs or images, paint it quickly, and read it elsewhere.

## Colour attributes (Object Data > Color Attributes)
The plus button opens a pop-up with **Name**, **Domain**, **Data Type** and **Color** (the default fill). Domain: *Vertex* (stored per vertex) or *Face Corner* (per corner of a face). Data Type: *Color* (RGBA, floating point; the Geometry Nodes reference says 32-bit float, linear colour space) or *Byte Color* (RGBA 8-bit, always sRGB; the reference suggests *Color* for wide-gamut or linear work). The menu beside the list has Duplicate Color Attribute and **Convert Color Attribute** (change domain and data type), and the panel has a render-active setting (`color_attribute_render_set`).

## Painting
- **Vertex Paint** mode paints the colour attribute and writes a gradient between connected vertices; occluded faces are not modified. Colour attributes are managed in the palette pop-over in the middle of the header. Enabling the **paint mask** in the header paints per face corner, which gives sharp colour edges on low-poly meshes.
- **Sculpt mode** can also paint colour attributes and suits much higher vertex counts.
- Brushes (Essentials library): Paint Hard, Paint Soft, Paint Hard Pressure, Paint Soft Pressure, Airbrush (brush type Paint Vertex), Blur, Average, Smear.
- Paint menu: Smooth Vertex Colors, Dirty Vertex Colors (Blur Strength, Blur Iterations, Highlight Angle, Dirt Angle, Dirt Only, Normalize), Vertex Color from Weight, Invert, Levels, Hue/Saturation/Value, Brightness/Contrast, **Set Vertex Colors** (Ctrl-X; fills the active attribute with the paint colour; option Affect Alpha), Sample Color (Shift-X; Shift-Ctrl-X samples the merged viewport colour).

## Viewing and using colour
- Viewport: Solid shading, Color set to *Attribute* (Workbench engine).
- Shader: the **Color Attribute** node reads a colour attribute and its alpha; the attribute list is that of the active object's mesh.
- Geometry Nodes: vertex groups, UV maps and colour attributes are all readable by name; a vertex group is a float attribute on the point domain; Store Named Attribute writes any type (Byte Color and UV only through that node). Colour-to-float conversion yields the grayscale equivalent.

## Baking
Cycles Bake: **Target** *Active Color Attribute* bakes into the active colour attribute of the active mesh object. The manual states baking requires a UV map plus a colour attribute or an image to bake to.

## Exporting
- glTF: **Use Vertex Color** options are Material (default: exported when used in the node tree as a Base Color multiplier), Active, Name, None; *Export all vertex colors* writes extra sets as COLOR_1, COLOR_2 and so on.
- FBX: the exporter has a **Vertex Colors** option (None, sRGB, Linear; default sRGB) and *Prioritize Active Color*. Check what your engine expects.

## Gotchas
- Nothing visible: check the active attribute, and that Solid shading Color is set to Attribute.
- Dirty Vertex Colors writes to the active attribute; use a dedicated attribute.

## Verify
Spreadsheet shows the attribute on the intended domain and type; Solid shading with Attribute colour matches what you painted.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Vertex Paint, Object Data, Color Attribute node, Cycles baking, glTF, Geometry Nodes attributes), branch blender-v5.2-release, and the FBX exporter source on the Blender main branch. Confirmed: all names, options and shortcuts above. Removed unconfirmed claims: a Shift-K Set Vertex Colors shortcut (it is Ctrl-X), the extended blend-mode list, sculpt colour filter and mask by colour, S and X paint shortcuts, OBJ, PLY, USD and Alembic export details, engine import behaviour, decimation effects, the eight-attribute FBX limit and the dark-value round-trip claim.
Method: documentation only; no commands were run.
