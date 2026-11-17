---
id: creative-arts.animation.blender.principled-emission-alpha
name: principled-emission-alpha
category: creative-arts
field: animation
product: blender
tags: [blender, shader, principled-bsdf, principled-emission-alpha, alpha-transparency, emission-strength, render-method]
level: practitioner
status: docs-checked
description: "Use Principled BSDF emission colour and strength and alpha transparency in Blender, including EEVEE render method, alpha hashed vs blended."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html
  - https://docs.blender.org/manual/en/5.2/render/eevee/material_settings.html
  - https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/light_paths.html
  - https://developer.blender.org/docs/release_notes/4.2/eevee/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# principled-emission-alpha

## Emission

- **Emission Color** and **Emission Strength**. A Strength of 1.0 makes the object appear in exactly the Emission Color (shadeless). Emission is emitted from below the coat and sheen layers.
- Use an emissive texture by plugging an image into Emission Color and keeping Strength a scalar.

## Alpha

- **Alpha** controls transparency, 1.0 fully opaque; usually linked to the Alpha output of an Image Texture node. The image Color output is premultiplied when the Alpha output is used.
- Cycles: transparency bounces are limited separately from other bounces (Light Paths > Transparent max bounces); raise them for stacked leaves.
- EEVEE (Material Properties > Settings): **Render Method** **Dithered** (grayscale hashed transparency, compatible with render passes and raytracing) or **Blended** (coloured transparency, incompatible with render passes and raytracing; sorted per object by origin, not per face or pixel). **Transparent Shadows** enables transparent shadows for a material with a Transparent BSDF (disabling renders faster). **Backface Culling** has Camera, Shadow and Light Probe Volume options. In 4.2 EEVEE, Dithered behaves like the former Alpha Hashed method; to emulate the former Alpha Clip add a Math node set to Greater Than.

## Gotchas

- Blended materials sort per object, so inner faces of one mesh may draw in the wrong order; Transparency Overlap off renders only the front-most fragments to fix some cases.
- Dithered with raytracing can be noisy around transparent edges; the manual's alpha clip set-up (Greater Than) cleans them.

## Verify

A leaf card renders with a clean cutout; an emissive screen shows its colour at Strength 1.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/principled (Emission Strength 1.0, Alpha), EEVEE material settings (Render Method, Transparent Shadows, Backface Culling, Transparency Overlap, alpha clip set-up), Cycles light paths (separate transparent bounce limit) and the 4.2 EEVEE release notes (Dithered replaces Alpha Hashed, Alpha Clip via Greater Than). Removed the unconfirmed default strength 0, typical strength values, bounce counts, Dithered-as-default claim and halo advice.

Method: documentation only; no commands were run.
