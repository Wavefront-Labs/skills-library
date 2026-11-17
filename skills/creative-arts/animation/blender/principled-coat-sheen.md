---
id: creative-arts.animation.blender.principled-coat-sheen
name: principled-coat-sheen
category: creative-arts
field: animation
product: blender
tags: [blender, shader, principled-bsdf, principled-coat-sheen, coat, sheen, clearcoat]
level: practitioner
status: verified
description: "Use the Principled BSDF Coat and Sheen layers in Blender: coat weight, roughness, IOR, tint and normal; sheen weight, roughness and tint for cloth."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/sheen.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# principled-coat-sheen

## Layer order

The Principled BSDF is based on OpenPBR. The glossy **Coat** sits on top of all base layers and the **Sheen** layer sits on top of everything. Emission is emitted from below the coat and sheen layers.

## Coat

Simulates clearcoat, lacquer or car paint. Sockets in Blender 4.5.14: Coat Weight (default 0), Coat Roughness (0.03), Coat IOR (1.5), Coat Tint (white), Coat Normal.
- **Weight**: intensity of the coat, both reflection and tinting; typically 0 or 1 for physically based materials, but can be textured.
- **Roughness**: roughness of the coat layer.
- **IOR**: index of refraction of the coat; affects reflectivity and the falloff of tinting.
- **Tint**: coloured tint modelled as absorption in the layer; saturation increases at shallower angles because light travels farther through the medium.
- **Normal**: normal for the coat layer, for example a smooth coat over a rough surface.

## Sheen

Simulates very small fibres: a soft velvet-like reflection near edges on cloth, or dust on arbitrary materials.
- **Weight**: intensity. **Roughness**: roughness of the sheen reflection. **Tint**: colour of the sheen. Sockets: Sheen Weight (default 0), Sheen Roughness (0.5), Sheen Tint (white). The separate Sheen BSDF node has Color, Roughness, Normal and Weight inputs.

## Recipes

- Car paint: Metallic base with flakes in the base Normal, Coat Weight 1, low Coat Roughness.
- Velvet: dark base, Sheen Weight 1, Sheen Tint lighter than the base colour.

## Gotchas

- The separate Sheen BSDF node is Cycles only; the Principled Sheen inputs are the layer described here.
- Sheen on its own does not make cloth; the surface also needs fibre normal or texture detail.

## Verify

Rotate a sphere under an HDRI: the coat gives a sharp secondary reflection over a blurrier base, and sheen brightens edges.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/principled (layer order, OpenPBR basis, Coat Weight/Roughness/IOR/Tint/Normal, Sheen Weight/Roughness/Tint) and shader/sheen (Cycles only). Removed the unconfirmed '4.0+ replaces Clearcoat' gate, typical numeric values (IOR 1.5, roughness 0.03, 0.3-0.5), the 3.x conversion note and the tint-strength remark.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Principled BSDF socket names and defaults listed above, and the Sheen BSDF node's sockets. Unrun (documentation only): OpenPBR layer order, tint absorption behaviour, Cycles-only status of the Sheen BSDF node, the recipes and Verify render.

Method: manual text confirmed from documentation; socket names run headless in Blender 4.5.14.
