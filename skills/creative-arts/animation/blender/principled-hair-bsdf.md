---
id: creative-arts.animation.blender.principled-hair-bsdf
name: principled-hair-bsdf
category: creative-arts
field: animation
product: blender
tags: [blender, hair, principled-hair-bsdf, hair-bsdf, hair-shader, melanin]
level: practitioner
status: docs-checked
description: "Shade hair in Blender with Principled Hair BSDF (Chiang and Huang models): melanin, redness, tint, roughness, coat, IOR, offset and random variation."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/hair_principled.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/hair.html
  - https://developer.blender.org/docs/release_notes/4.0/cycles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# principled-hair-bsdf

Cycles only.

## Models

- **Chiang**: Gaussian-distribution model with separate roughness along and orthogonal to the hair. Inputs Roughness, Radial Roughness, Coat.
- **Huang** (4.0+, the previous node became the Chiang variant): microfacet-based reflection and transmission, supports elliptical hair. Inputs Aspect Ratio, Roughness, Reflection, Transmission, Secondary Reflection (keep the last three at 1.0 for physical correctness).

## Colour parametrization

- **Melanin Concentration**: **Melanin** (0 to 1), **Melanin Redness** (0 to 1, ratio of pheomelanin to eumelanin), **Tint** (dyes after the melanin; not randomised; white disables it), **Random Color**. With Redness at 1 the manual lists white 0, blonde 0.25, reddish 0.5, brown 0.75, black 1.
- **Direct Coloring**: pick a colour (**Color**); the shader approximates the absorption coefficient.
- **Absorption Coefficient**: Beer-Lambert attenuation coefficient for technical users.

## Common inputs

**IOR** (default 1.55), **Offset** (tilts the glint by raising the cuticle scale angle; human hair usually low), **Random Color**, **Random Roughness**, **Random** (random source; defaults to Hair Info Random when unconnected).

## Huang aspect ratio

Recommended 0.8 to 1 for Asian hair, 0.65 to 0.9 for Caucasian, 0.5 to 0.65 for African. The major axis follows the curve normal, which can be created with Geometry Nodes but is not supported in legacy particle hair.

## Hair BSDF (simple)

Cycles only. **Component** Reflection or Transmission (usually mixed with a Mix Shader), inputs Color, Offset, Roughness U/V, Tangent.

## Gotchas

- Principled Hair BSDF is Cycles only; check the look in the engine you will render with.
- Too low Roughness makes hair look metallic with firefly-like glints; too high looks Lambertian.

## Verify

Render under a sun light: the Melanin ladder (0 to 1) runs from white to black hair.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/hair_principled (Cycles Only, models and inputs, parametrizations, Melanin ladder at Redness 1, IOR 1.55, Random source, Aspect Ratio guidance), shader/hair and the 4.0 Cycles release notes (Huang added, previous model renamed Chiang). Removed the EEVEE approximation claim, the 'raise Transmission bounces' advice, typical roughness/coat/offset values and the non-linear melanin colour mapping (which contradicted the manual's ladder).

Method: documentation only; no commands were run.
