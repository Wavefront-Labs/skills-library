---
id: creative-arts.animation.blender.eevee-material-render-method
name: eevee-material-render-method
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-material-settings, render-method, dithered, blended, transparency]
level: practitioner
status: docs-checked
description: "Set EEVEE material settings: Dithered vs Blended render method, transparency overlap, transparent shadows, thickness, backface culling, displacement and sorting fixes."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/material_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-material-render-method

Goal: correct transparency, refraction and shadows for each EEVEE material.

## Material Properties > Settings

- **Render Method**: controls blending and compatibility with features.
  - *Dithered* (deferred rendering): grayscale hashed transparency, compatible with render passes and raytracing. Materials are rendered in layers, and each layer can only transmit light emitted from earlier layers; with no intersection below, transmissive BSDFs fall back to light probes. **Raytraced Transmission** uses raytracing to find the transmitted colour instead of probes only, which stops the surface contributing to the lighting of surfaces not using the setting.
  - *Blended* (forward rendering): allows coloured transparency but is incompatible with render passes and raytracing. EEVEE has no per-pixel or per-triangle sorting: only per-object sorting, automatically, based on object origin, on transparent surfaces. Opaque surfaces always sort correctly. Per-object sorting has a performance cost, and thousands of objects greatly degrade performance. Face order can be adjusted with Sort Elements in Edit Mode or a Sort Elements geometry node.
- **Transparency Overlap** (Blended only; older Python name `show_transparent_back`, UI label "Show Backface"): when on, all transparent fragments render; when off, only the front-most surface fragments render, which can fix blend-order sorting issues.
- **Transparent Shadows**: uses transparent shadows if the material contains a Transparent BSDF; disabling renders faster but shadows are not accurate.
- **Backface Culling**: hides the back side of faces, with Camera, Shadow and Light Probe Volume toggles (the last treats the material as single sided when baking light probe volumes and helps reject probes inside the object). The manual advises turning it on whenever possible, as it affects performance.
- **Displacement**: Bump Only, Displacement Only (not supported; falls back to Displacement and Bump), or Displacement and Bump (modifies vertex positions). Not precomputed, so its cost is multiplied by the render sample count. **Max Distance** is the maximum distance a vertex can be displaced; larger displacements may cause visibility and shadow-update problems.
- **Thickness** mode (Sphere or Slab) and **From Shadow**: see below.

## Thickness (Material Properties > Thickness)

Approximates inner geometry for Subsurface Scattering, Translucent and Refraction BSDFs. With no value plugged into the Material Output Thickness socket, a default based on the smallest object dimension is used; a connected value is object-space; zero disables the approximation. Sphere suits rounder objects, Slab suits flat or thin ones (glass panels, grass blades). For compound meshes like vegetation, set the thickness of the individual parts.

## Fixes

- Noisy edges around transparent areas with raytracing and Dithered: quantise alpha to 0 or 1 with a Greater Than math node (the manual's Alpha Clip Setup).
- Blended object sorts wrongly against another: sorting is per object origin; split the mesh, adjust face order, try Transparency Overlap off, or use Dithered.
- Glass does not refract as expected: set Thickness, and enable Raytraced Transmission under Dithered if probes are not enough.

## Verify

Render a leaf card, a glass object and a hologram decal. Leaf shadows should show the leaf shape (Transparent Shadows), glass should refract, and the decal should be smooth.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Materials). Confirmed: Render Method behaviours, Raytraced Transmission, Transparency Overlap, Transparent Shadows, Backface Culling toggles, Displacement options and Max Distance, Thickness mode and defaults, Alpha Clip Setup. Corrected naming: the current setting is Transparency Overlap (Show Backface is its deprecated alias) and Backface Culling > Light Probe Volume (the probe volume page calls it Single Sided). Removed unconfirmed: "Dithered is default", per-use-case advice for leaves/hair.
Method: documentation only; no commands were run.
