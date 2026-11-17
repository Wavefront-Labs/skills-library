---
id: creative-arts.animation.blender.color-attribute-node
name: color-attribute-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader-nodes, color-attribute-node, vertex-color-node, attribute-node, vertex-paint]
level: practitioner
status: docs-checked
description: "Read vertex colours in Blender materials with the Color Attribute node or the Attribute node: attribute selection, alpha output, mask patterns and checks."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/vertex_color.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/attribute.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# color-attribute-node

Goal: drive a material from painted vertex colours.

## Color Attribute node

Input category, **Color Attribute** node. The dropdown lists the Color Attributes of the active object's mesh. A name shown in red is not on the active object's mesh but may exist on other objects that share the material. Outputs **Color** and **Alpha**. No inputs.

## Attribute node (alternative)

**Attribute** node, Attribute Type **Geometry**, Name = the attribute name. Outputs **Color**, **Vector**, **Factor** and **Alpha** (Alpha defaults to 1 when the attribute has no alpha). Other types: **Object** (custom property or RNA path on the object, then its mesh), **Instancer**, **View Layer**. A missing Object or View Layer attribute outputs 0 on all sockets including Alpha.

## Patterns

- Mask: Color Attribute Color > Separate Color R/G/B for three independent masks in one attribute.
- Tint: Mix Color (Multiply) base texture by vertex colour.
- Blend materials: Color Attribute > Mix Shader Factor.

## Gotchas

- Check that every object using the material has the named attribute (the red name warning).
- Export behaviour of vertex colours depends on the exporter; check the glTF or FBX exporter documentation for your version.

## Verify

Plug Color straight into an Emission shader on Material Output Surface to view the raw attribute in the viewport.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against input/vertex_color and input/attribute: dropdown and red-name behaviour, Color and Alpha outputs, Attribute node types and Color/Vector/Factor/Alpha outputs, zero output for missing Object and View Layer attributes. Removed unsupported claims on empty-name render-attribute behaviour, colour space decoding, glTF export settings, renaming and domain behaviour, and vertex-group reads.

Method: documentation only; no commands were run.
