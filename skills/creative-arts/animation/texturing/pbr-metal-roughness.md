---
id: creative-arts.animation.texturing.pbr-metal-roughness
name: pbr-metal-roughness
category: creative-arts
field: animation
product: texturing
tags: [metal-roughness, pbr, metallic, roughness, base-color, physically-based, principled-bsdf, standard-surface, energy-conservation]
level: practitioner
status: draft
description: "Author metal/roughness PBR maps correctly: binary metallic, base colour meaning for metals vs dielectrics, roughness ranges, and common mistakes that look plastic."
sources:
  - https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-2
  - https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#metallic-roughness-material
  - https://autodesk.github.io/standard-surface/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metal/roughness workflow

**Goal:** materials that respond believably to any lighting, because maps encode physical meaning, not
painted lighting.

## The three core maps

| Map | Meaning | Values |
|---|---|---|
| Base colour (sRGB) | dielectrics: diffuse albedo; metals: specular reflectance colour | dielectric 30-240 sRGB; metals 180-255 (bright, often tinted) |
| Metallic (linear) | is it metal? | 0 or 1; grey only for transitions (dust on metal, AA edges) |
| Roughness (linear) | microsurface spread | 0 mirror to 1 matte; most real surfaces 0.2-0.8 |

Dielectrics get a fixed ~4% reflectance (F0 0.04) from the shader; you don't paint specular.

## Rules of thumb

- Metallic is binary. Mid-grey metallic over large areas looks like dirty plastic.
- Painted rust/paint on metal: those areas are non-metal (metallic 0) with their own colour.
- Base colour must have no lighting baked in: no AO shadows, no highlights. Put AO in its own map/channel.
- Roughness carries most of the visual interest: smudges, fingerprints, wear polish (edges polished =
  lower roughness), dust (higher).
- Dark metals still have bright base colour; dark appearance comes from environment reflection.

## Stylised animation

PBR still helps stylised shows (consistent response under varied lighting), but many cel/toon pipelines
use custom shaders; then maps mean whatever the shader defines. Decide per show which applies and
document it.

## Common failures

| Look | Cause |
|---|---|
| everything looks plastic | metals marked non-metal, or roughness uniform |
| dark, muddy colours | base colour too dark (below ~30 sRGB) or AO baked in |
| chrome-like everything | roughness too low across the board |

## Verify

Check in Painter or the renderer under two or three different HDRIs: materials keep their identity; a
base colour validator (Painter's PBR validate filter or a histogram) shows values in range
(`creative-arts.animation.texturing.pbr-albedo-ranges`).
