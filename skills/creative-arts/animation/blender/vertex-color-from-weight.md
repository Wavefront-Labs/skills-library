---
id: creative-arts.animation.blender.vertex-color-from-weight
name: vertex-color-from-weight
category: creative-arts
field: animation
product: blender
tags: [blender, vertex-paint, vertex-color-from-weight, weight-to-color, convert-attribute, geometry-nodes]
level: practitioner
status: docs-checked
description: "Convert vertex group weights to colour attributes and back in Blender: Vertex Color from Weight, Convert Color Attribute, Geometry Nodes Store Named Attribute."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/vertex_paint/editing.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attributes_reference.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attribute/store_named_attribute.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# vertex-color-from-weight

Goal: reuse a painted weight map as a colour mask (shaders, export) or turn colour into weights.

## Weight to colour (built-in)
1. Make the vertex group you want the active group.
2. Create or select a colour attribute (Object Data > Color Attributes > plus).
3. Vertex Paint mode > Paint > **Vertex Color from Weight**: converts the active weight into grayscale colours.

## Any group to a colour attribute (Geometry Nodes)
Vertex groups are available in Geometry Nodes as float attributes on the point domain, referred to by name. Read it with a Named Attribute node and write it with **Store Named Attribute** (Data Type Color, Domain Point, a Name). Converting between float and colour gives the grayscale equivalent. Store Named Attribute needs the Name, Value, Data Type and Domain set; it can write Byte Color, which has no socket.

## Colour to weight
Store Named Attribute with Data Type **Float** and the vertex group's name, fed from a colour field (converted to grayscale). If a vertex group attribute's type is changed from Float, it is no longer a vertex group. The manual also warns that Geometry Nodes does not always produce vertex groups when a node such as Join Geometry is used.

## Gotchas
- Naming collisions between a vertex group and a UV map or colour attribute of the same name leave only one accessible in Geometry Nodes; use distinct names.
- Byte Color is always stored in sRGB and Color is linear (per the manual), so values can differ between the two types after conversion; use *Color* when the exact value matters.
- The operator result depends on the active vertex group and attribute, so confirm both before running it.

## Verify
Solid shading with Color set to Attribute shows the same gradient as Weight Paint mode for the group.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Vertex Paint editing, Geometry Nodes attributes reference and Store Named Attribute, Color Attributes), branch blender-v5.2-release. Confirmed: Paint menu operator name and behaviour, vertex groups as point-domain float attributes by name, float to colour grayscale conversion, name collisions, Byte Color sRGB versus Color linear, Convert Color Attribute name. Removed unconfirmed claims: Combine and Separate Color node chain, the greyed-out state without a group, an sRGB value example, the Data Transfer modifier tip and export-with-Apply-Modifiers details.
Method: documentation only; no commands were run.
