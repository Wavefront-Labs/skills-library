---
id: creative-arts.animation.blender.principled-subsurface
name: principled-subsurface
category: creative-arts
field: animation
product: blender
tags: [blender, shader, principled-bsdf, principled-subsurface, subsurface-scattering, sss, random-walk]
level: practitioner
status: docs-checked
description: "Set up subsurface scattering in Blender's Principled BSDF: weight, radius, scale, random walk vs skin vs Burley methods, IOR and anisotropy."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html
  - https://docs.blender.org/manual/en/5.2/render/eevee/material_settings.html
  - https://developer.blender.org/docs/release_notes/5.0/cycles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# principled-subsurface

## Inputs (Principled BSDF > Subsurface)

- **Weight**: blend between diffuse and subsurface scattering; typically 0 or 1.
- **Radius**: average scattering distance per colour channel; X, Y, Z map to R, G, B (for skin, red scatters deepest).
- **Scale**: scale applied to the radius.
- **IOR** (Cycles only): index of refraction for rays entering the subsurface component, may differ from the global IOR to simulate skin layers.
- **Anisotropy** (Cycles only): zero scatters uniformly, positive forward, negative backward; skin has been measured around 0.8.

## Method

- **Christensen-Burley**: approximation, less accurate than Random Walk but can resolve noise faster in some situations.
- **Random Walk** (Cycles only): true volumetric scattering; accurate on thin and curved objects; works best for closed meshes (overlapping faces and holes cause problems). Since 5.0 it uses multiple bounces, which reduces darkening.
- **Random Walk (Skin)** (Cycles only): optimised for skin; radius adjusts from the colour texture and entry direction uses diffuse and specular transmission with custom IOR.
- **Random Walk (Legacy)** (Cycles only): older albedo mapping, to be deleted.

## Thin wall

With Thin Wall on, Radius, Scale and Method are irrelevant.

## Gotchas

- A glowing or waxy look usually means Scale is too large for the object size; Scale works in scene units.
- EEVEE approximates subsurface using the material Thickness settings (Sphere or Slab mode), so thin parts differ from Cycles.

## Verify

Backlight an ear or thin object: coloured translucency appears; after changing the scene scale, adjust Scale to match.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/principled (Weight, Radius, Scale, IOR and Anisotropy Cycles only, Method list, Thin Wall note), EEVEE material settings (Thickness used for subsurface) and the 5.0 Cycles release notes (multiple-bounce random walk). Removed the unconfirmed default radius, skin scale and recipe numbers and the claim that Random Walk (Skin) is the default.

Method: documentation only; no commands were run.
