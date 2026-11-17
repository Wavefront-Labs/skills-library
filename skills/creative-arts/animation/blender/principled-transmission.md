---
id: creative-arts.animation.blender.principled-transmission
name: principled-transmission
category: creative-arts
field: animation
product: blender
tags: [blender, shader, principled-bsdf, principled-transmission, transmission, ior, thin-film]
level: practitioner
status: docs-checked
description: "Make glass, liquids and thin-film iridescence with the Principled BSDF: transmission weight, IOR values, roughness, thin film thickness and IOR."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html
  - https://docs.blender.org/manual/en/5.2/render/eevee/material_settings.html
  - https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/light_paths.html
  - https://developer.blender.org/docs/release_notes/4.2/cycles/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# principled-transmission

## Transmission

- **Weight**: 0 is fully opaque, 1 fully transmissive (glass, liquids). Mix values for frosted or partial transmission.
- **IOR**: the default 1.5 approximates glass; the manual gives 1.0 (air) to about 4.0 (germanium) as the range for most materials. Look up values for specific materials in a reference.
- **Roughness**: microfacet roughness for reflection and transmission.
- **Thin Wall**: for papers, leaves and window sheets; the surface is a zero-thickness slab (in EEVEE set Thickness 0 and Thickness Mode Slab).
- Depth-dependent colour: use Volume Absorption on the Volume output.

## Thin Film (Cycles only; added in 4.2)

- **Thickness** (nm; 0 disables; the effect is strongest roughly between 100 and 1000 nm) and **IOR** (default 1.33, about water; at 1.0 or equal to the main IOR the effect disappears). Iridescence of soap bubbles, oil films, coatings. Glass BSDF has the same inputs.

## EEVEE

Material Settings: with the **Dithered** render method, **Raytraced Transmission** uses raytracing for transmitted colour instead of light probes only. **Thickness** (Sphere or Slab, with a Material Output thickness value) approximates inner geometry; refraction does not refract objects inside the thickness distance.

## Gotchas

- Black glass in Cycles: too few Transmission bounces (Light Paths > Transmission); transmission shaders usually need the most bounces.
- Glass shadows can look too dark without caustics; see glass-refraction-bsdf for the direct/indirect trick.

## Verify

Render a glass sphere over a checker: the image is inverted through the sphere, with magnification set by IOR.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/principled (Transmission Weight, IOR default 1.5 and range, Thin Wall, Thin Film Thickness/IOR and Cycles-only marker), EEVEE material settings (Raytraced Transmission under Dithered, Thickness), Cycles light paths and the 4.2 Cycles release notes (thin film added in 4.2). Removed the material IOR table, the bubble thickness example, the 12-bounce figure and the Solidify advice.

Method: documentation only; no commands were run.
