---
id: creative-arts.animation.blender.velvet-toon-bsdf
name: velvet-toon-bsdf
category: creative-arts
field: animation
product: blender
tags: [blender, shader, velvet-toon-bsdf, sheen-bsdf, toon-bsdf, metallic-bsdf, specialised-bsdfs]
level: practitioner
status: docs-checked
description: "Use Blender's specialised BSDFs: Sheen (velvet), Toon, Metallic with F82 tint, Translucent, Ray Portal and Specular BSDF, and when they beat Principled."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/sheen.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/toon.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/metallic.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/translucent.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/ray_portal.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/specular_bsdf.html
  - https://developer.blender.org/docs/release_notes/4.2/cycles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# velvet-toon-bsdf

## Sheen BSDF (Cycles only)

Layer it on top of other shaders, such as dielectric or metallic set-ups, for cloth or dust. Inputs Color, Roughness (higher values reflect more colour and look dusty; lower look fuzzy and darker), Normal. Distribution: **Microfiber** or **Ashikhmin** (the classic velvet used before 4.0). The Principled BSDF has its own Sheen layer.

## Toon BSDF (Cycles only)

Component **Diffuse** or **Glossy**; **Size** (0 to 1, an angle of reflection between 0 and 90 degrees), **Smooth** (angle over which the transition from full to no reflection happens). For an EEVEE toon look use Shader to RGB (see shader-to-rgb-ramp).

## Metallic BSDF

Fresnel Type **F82 Tint** (Base Color, plus Edge Tint seen at 82 degrees; uses the Adobe F82-Tint formula) or **Physical Conductor** (IOR as n and Extinction as k per colour channel, for measured metals; the manual points to the physicallybased.info and refractiveindex.info databases). Roughness, Distribution (GGX, Multiscatter GGX, Beckmann on Cycles), Anisotropy and Rotation (Cycles only). Gives more accurate coloured metals than Principled in the Physical Conductor mode.

## Translucent BSDF

Lambertian diffuse transmission for paper, lampshades and thin leaves; input Color and Normal.

## Ray Portal BSDF (Cycles only; added in 4.2)

Transports entering rays to another position and direction (inputs Color, Position, Direction). Acts like a Transparent BSDF for render passes and is limited by the transparent bounce limit. It works in one direction only, so add a second portal at the target for the other direction. Light sampling through portals is inefficient, so lights on the far side can be noisy.

## Specular BSDF (EEVEE only)

A specular-workflow shader similar to the Principled BSDF.

## Gotchas

- Sheen, Toon and Ray Portal are Cycles only; match engines when previewing.
- Physical Conductor needs per-channel n and k values; take them from the databases above.

## Verify

Sphere under an HDRI: Metallic F82 Tint shows the Edge Tint at grazing angles; Toon shows banded lighting that changes with Size and Smooth.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/sheen, toon, metallic, translucent, ray_portal and specular_bsdf, and the 4.2 Cycles release notes (Ray Portal added in 4.2). Removed the gold n/k numbers, the RGB wavelength-average advice, the 0.3 translucent mix value, and the 'legacy game assets' claim.

Method: documentation only; no commands were run.
