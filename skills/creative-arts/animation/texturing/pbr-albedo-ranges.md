---
id: creative-arts.animation.texturing.pbr-albedo-ranges
name: pbr-albedo-ranges
category: creative-arts
field: animation
product: texturing
tags: [albedo-range, pbr, base-color, pbr-validate, charcoal-snow, srgb-values, histogram, physically-based, texture-qc]
level: practitioner
status: draft
description: "Keep base colour/albedo in physically plausible ranges (about 30-240 sRGB for dielectrics), check with PBR validation, and know when stylised shows break the rule on purpose."
sources:
  - https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-2
  - https://helpx.adobe.com/substance-3d-painter/filters/pbr-validate.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Albedo value ranges

**Goal:** base colours that light correctly. Albedo outside plausible ranges breaks energy behaviour: too
dark absorbs everything (dead, black patches under bright light), too bright reflects more light than
it receives (glowing, blown out).

## Ranges (sRGB 8-bit)

| Material | Approximate albedo |
|---|---|
| Darkest dielectric (charcoal, fresh asphalt) | ~30-50 |
| Typical surfaces (wood, concrete, skin, fabric) | 50-200 |
| Brightest dielectric (fresh snow, white paint) | ~240 |
| Metals (specular colour) | 180-255 (70-100% reflectance) |

Allegorithmic's PBR guide recommends dielectric base colour between about 50 and 240 sRGB (a stricter
30 lower bound allowed for very dark materials).

## Checking

- Substance Painter: add a **PBR Validate** filter layer (or the Metal/Roughness validation in the
  viewport): it highlights out-of-range base colour and metallic areas in red.
- Any image tool: histogram of base colour; sample darkest and brightest areas.
- Renderer: an albedo AOV and false colour.

## Fixing

- Raise blacks of dark materials with a Levels output range (e.g. 0 -> 35) instead of painting them darker.
- Remove baked-in AO/shadow from photo-sourced colour (delighting, or high-pass
  flattening).
- Bright whites: cap at about 240.

## Stylised exceptions

Toon and flat-colour styles often use pure black lines and saturated fills outside PBR ranges, rendered
with non-physical shaders; that is fine when the shader is not energy-conserving PBR. The mistake is mixing:
PBR shaders with stylised out-of-range colours light inconsistently. Decide per asset type.

## Verify

PBR Validate shows no red on dielectric areas (or only on intentional stylised areas documented in the
look guide); renders under bright and dim lighting keep material identity without blown or dead patches.
