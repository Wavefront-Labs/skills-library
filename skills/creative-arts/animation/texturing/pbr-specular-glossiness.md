---
id: creative-arts.animation.texturing.pbr-specular-glossiness
name: pbr-specular-glossiness
category: creative-arts
field: animation
product: texturing
tags: [specular-glossiness, pbr, spec-gloss, diffuse, glossiness, f0, convert-spec-gloss-to-metal-rough, legacy-assets]
level: advanced
status: draft
description: "Author or convert specular/glossiness PBR maps: diffuse vs specular colour, F0 values, glossiness as inverted roughness, and converting spec/gloss to metal/rough."
sources:
  - https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-2
  - https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Archived/KHR_materials_pbrSpecularGlossiness
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Specular/glossiness workflow

**Goal:** handle the older but still common spec/gloss PBR model correctly, mostly when receiving legacy
assets or targeting a renderer/engine that uses it, and convert to metal/rough when the pipeline requires.

## Maps

| Map | Meaning |
|---|---|
| Diffuse (sRGB) | albedo for dielectrics; **black for raw metals** |
| Specular (sRGB colour) | reflectance F0: dielectrics ~0.04 (sRGB ~56-60 grey), metals coloured and bright |
| Glossiness (linear) | 1 - roughness: white = smooth |

Advantage: explicit control of dielectric F0 (gemstones, water). Disadvantage: easy to break energy
conservation (bright diffuse plus bright specular).

## Conversion to metal/rough (approximate)

- Roughness = 1 - glossiness.
- Metallic: where specular is bright and diffuse is dark (metals); otherwise 0.
- Base colour: diffuse for dielectrics; specular colour for metals.
Tools: Substance 3D Painter/Designer conversion nodes ("Specular/Glossiness to Metallic/Roughness"),
glTF converters for the old `KHR_materials_pbrSpecularGlossiness` extension (archived; metal/rough is the
glTF core).

## Gotchas

- Glossiness vs roughness swaps are the most common error: shiny becomes matte. Check one known-polished
  area.
- Dielectric specular values above ~0.08 (sRGB ~80) look like plastic coating; most non-metals sit
  0.02-0.05 linear.
- Some legacy "spec maps" are just black-and-white intensity masks from non-PBR pipelines, not F0; rebuild
  rather than convert.

## Verify

After conversion, render the asset side by side with the original spec/gloss version under the same HDRI:
highlights and colours match closely; metal areas have metallic 1 and bright base colour.
