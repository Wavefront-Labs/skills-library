---
id: creative-arts.animation.blender.mapping-node
name: mapping-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, mapping-node, texture-mapping, texture-coordinate]
level: practitioner
status: verified
description: "Transform Blender texture coordinates with the Mapping node: Point, Texture, Vector and Normal types, transform order, and how location and scale behave."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/utilities/vector/mapping.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# mapping-node

## Vector types

- **Point**: a straightforward transformation, analogous to transforming a UV map. Translating the coordinates along +X moves the evaluated texture toward -X, and scaling the coordinates up scales the texture down. Order: Scale, Rotate, Translate.
- **Texture**: the inverse transformation, so moving Location moves the texture itself and scaling up scales the texture up (intuitive for placement). Order: Translate, Rotate, Scale.
- **Vector**: a Point transformation with zero translation (for directions). Location is not available.
- **Normal**: the inverse transpose of the transformation, normalised; correct normals after non-uniform scaling.
- Inputs: Vector, Location (Texture and Point types only), Rotation (XYZ order), Scale. Output: Vector. Measured by rendering the output as emission colour (Blender 4.5.14, input vector (1, 2, 3)): Point with Location (10, 0, 0) and Scale 2 gave (12, 4, 6); Texture with the same settings gave (-4.5, 1, 1.5), i.e. (v - Location) / Scale; Vector ignored Location and gave (2, 4, 6); Normal with Scale (4, 1, 1) gave the normalised (0.069, 0.553, 0.830); Point with Rotation Z 90 degrees turned (1, 2, 3) into (-2, 1, 3).

## Usage

Texture Coordinate (UV, Object, Generated) -> Mapping -> texture Vector input.

## Tricks

- Randomise per object: Object Info Random -> Mapping Location.
- Animate Location with a driver for scrolling textures such as conveyor belts or water flow.

## Gotchas

- In Point mode, Scale above 1 makes the texture smaller (more repeats).
- Use Texture mode when you want Location and Scale to act on the texture itself.

## Verify

Set Scale to 2 in Point mode: the texture repeats twice as often; a Location shift moves the pattern the opposite way to the shift.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against utilities/vector/mapping: vector types and their behaviour, transform order, input availability, Rotation XYZ order, and the Point-mode scale and translation direction. Removed the Node Wrangler Ctrl+T shortcut, the degrees remark, the socket auto-expand claim and the object-scale and rest-position remarks.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: node sockets Vector, Location, Rotation, Scale and the vector_type enum POINT, TEXTURE, VECTOR, NORMAL; the four types evaluated as above. Unrun (documentation only): the Tricks section (Object Info Random, driven scrolling) and the Verify render.

Method: manual text confirmed from documentation; node behaviour run headless in Blender 4.5.14.
