---
id: creative-arts.design-for-form-and-experience.concept-design.setting-up-render-materials-for-plastics-and-metals
name: setting-up-render-materials-for-plastics-and-metals
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [render-materials, product-rendering, plastics-material, metal-material, keyshot, material-setup]
level: practitioner
status: draft
description: "Set up convincing render materials for plastics, brushed and polished metals, glass and rubber: roughness, reflectivity, texture, bevelled edges and checks."
sources:
  - "Koos Eissen and Roselien Steur, Product Design Rendering (BIS Publishers)"
  - "IDSA (idsa.org) education resources"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Render material setup for plastics and metals

Applies to KeyShot, Fusion render, Blender, V-Ray and similar. Parameter names differ; the physical ideas do not. Numbers below are starting points to adjust by eye.

## Principles
- Real objects have **small bevels**: add roughly 0.2-1 mm fillets (or bevel shaders) so edges catch light.
- **Roughness/gloss** separates materials; **Fresnel** (stronger reflection at glancing angles) is handled by physically based materials.
- Surface texture needs **bump or normal** detail at believable scale; map at real-world size.
- Colour comes from the CMF specification (see `...concept-design.specifying-colour-and-matching-across-materials`).

## Starting points
- **Glossy plastic:** dielectric, base colour, low roughness (about 0.05-0.2), optional clear coat.
- **Matte or textured plastic:** roughness about 0.4-0.7 with fine bump (see `...concept-design.specifying-mould-textures-and-gloss`).
- **Brushed metal:** metallic on, tinted base colour, roughness about 0.2-0.4, anisotropy with the brush direction aligned to the part.
- **Polished metal or chrome:** metallic on, near-zero roughness; the look depends entirely on the environment (see `...concept-design.lighting-with-hdri-environments`).
- **Anodised aluminium:** metallic, coloured tint, slight roughness, fine sandblast bump.
- **Glass and clear plastic:** transmission with an index of refraction (about 1.5 for glass, about 1.49 for acrylic).
- **Rubber:** dielectric, high roughness, low specular.

## Gotchas
- Pure black or pure white base colours clip; keep values off the extremes.
- One material everywhere looks fake; vary roughness slightly between parts.

## Verify
- [ ] Every sharp edge has a highlight.
- [ ] Metals look right under two different environments.
- [ ] Textures read at believable scale at final resolution.
