---
id: creative-arts.animation.blender.glass-refraction-bsdf
name: glass-refraction-bsdf
category: creative-arts
field: animation
product: blender
tags: [blender, shader, glass-refraction-bsdf, glass-bsdf, refraction-bsdf, transparent-bsdf]
level: practitioner
status: docs-checked
description: "Choose between Blender Glass, Refraction and Transparent BSDFs: distribution, IOR, roughness, fake glass via Light Path and shadow tricks."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/glass.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/refraction.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/transparent.html
  - https://docs.blender.org/manual/en/5.2/render/cycles/optimizations/reducing_noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# glass-refraction-bsdf

## Nodes

- **Glass BSDF**: mixes refraction and reflection at grazing angles. Inputs Color, Roughness, IOR (1.0 passes rays straight through), Normal, plus Thin Film (Cycles only: Thickness in nm, 0 disables, and IOR). Distribution: GGX, Multiscatter GGX, Beckmann (Cycles only).
- **Refraction BSDF**: refraction only; use as a building block mixed with a glossy node using a Fresnel factor, otherwise glossy refraction is dark at the edges. Inputs Color, Roughness, Normal; Distribution GGX or Beckmann (Cycles only).
- **Transparent BSDF**: passes straight through the surface with no refraction, as if there were no geometry; useful with alpha maps.

## Fake glass for fast clean renders (Cycles)

The Glass BSDF causes noise from caustics, and with caustics disabled glass shadows can look too dark. Use a Light Path node to pick Glass BSDF when viewed directly and Transparent BSDF when viewed indirectly (for example Mix Shader Fac from Is Shadow Ray, glass on the first input and Transparent on the second). This gives properly coloured shadows without caustics.

## Gotchas

- The Glass BSDF is only transparent where Color is white; colour tints the transmitted light.
- Thin Film is available on Glass BSDF and Principled BSDF in Cycles; for other Principled layers (coat, sheen) use the Principled BSDF with Transmission.

## Verify

Window test scene: the direct/indirect trick lights the interior with brighter, cleaner shadows than the plain Glass BSDF at the same sample count.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/glass, shader/refraction, shader/transparent and the Cycles noise-reduction page (glass and transparent shadows): inputs, distributions and Cycles-only markers, Thin Film, the Light Path trick. Removed the claim that Glass BSDF lacks thin film, the thin-window and double-tint advice, and the rough-glass noise remark.

Method: documentation only; no commands were run.
