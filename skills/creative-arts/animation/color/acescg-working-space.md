---
id: creative-arts.animation.color.acescg-working-space
name: acescg-working-space
category: creative-arts
field: animation
product: color
tags: [acescg, aces, ap1, scene-linear, working-space, rendering-space, blender, colour-management, texture-colour-space]
level: practitioner
status: draft
description: "Run CG lighting and rendering in ACEScg: set the scene-linear role, convert textures and colour pickers correctly, and avoid the out-of-gamut and sRGB-albedo traps."
sources:
  - https://docs.acescentral.com/
  - https://opencolorio.readthedocs.io/en/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACEScg working space for CG

**Goal:** lights, materials and renders share one wide-gamut linear space (AP1 primaries, linear) so energy and
colour mix physically and the output transform decides how it looks.

## Set it up

- Load the show OCIO config with `scene_linear` and `rendering` roles set to ACEScg
  (see `creative-arts.animation.color.ocio-config-authoring`).
- **Blender 4.x:** default config is Filmic/AgX with Linear Rec.709 as working space; Blender 4.4+ lets you pick the
  working space in Color Management (*Working Space*) when the config allows it, otherwise set `OCIO` to an ACES
  config before launching Blender. Check *Render Properties > Color Management*.
- Renderers (Cycles, Arnold, RenderMan, Karma) read the scene-linear role; confirm the renderer's own colour
  settings are not overriding it.

## Textures

| Texture type | Colour space tag |
|---|---|
| Albedo/base colour painted in sRGB | sRGB - Texture (converted to ACEScg on read) |
| Roughness, metal, normal, height, masks | Raw / Non-Color (no conversion) |
| HDRI | the space it was captured in (usually Linear Rec.709), converted to ACEScg |

Substance Painter exports in sRGB by default; tag exports correctly at import rather than re-exporting in ACEScg
(see `creative-arts.animation.texturing.painter-export-presets`).

## Picking colours

Colour pickers show ACEScg values. A designer's sRGB hex `#FF4A00` must be converted (OCIO `ocioconvert` or a
small Python conversion with the AP1 matrix); typing the hex as an ACEScg triplet gives a more saturated colour.

## Traps

- **Out-of-gamut values:** AP1 can represent colours a display cannot; highly saturated lights (pure ACEScg red)
  clip or shift hue through the output transform. Keep emissive colours inside Rec.709/P3 where possible.
- **Albedo energy:** an sRGB albedo of 1.0 white becomes > 1 in some conversions; clamp base colour to physical
  ranges (see `creative-arts.animation.texturing.pbr-albedo-ranges`).
- Mixing ACEScg renders with Linear Rec.709 elements in comp without conversion gives colour shifts.

## Verify

A shader ball with an sRGB-tagged chart texture, rendered in ACEScg and viewed through the show view, matches the
same chart viewed in the texture app's sRGB viewer within visible tolerance.
