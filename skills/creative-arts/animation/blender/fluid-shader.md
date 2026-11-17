---
id: creative-arts.animation.blender.fluid-shader
name: fluid-shader
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, fluid-shader, water-shader, liquid-material, glass-bsdf, absorption]
level: practitioner
status: docs-checked
description: "Shade Mantaflow liquid meshes as water: Principled BSDF transmission, Volume Absorption depth colour, Cycles caustics options, and EEVEE Raytraced Transmission."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/volume_absorption.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
  - https://docs.blender.org/manual/en/latest/render/eevee/material_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fluid-shader

## Base water

- Principled BSDF: in the Transmission group set **Weight** to 1 (zero is a fully opaque surface, one fully transmissive; the manual lists transmission as the setting for glass and liquids). Set **IOR** to about 1.33 for water (physical value; the node accepts 1.0 to 4.0 for most materials) and keep Roughness low (practice).
- Add a **Volume Absorption** node on the Volume input of the Material Output: its inputs are Color and Density. The manual gives water and coloured glass as the typical use. Practice: a pale blue-green colour and a density tuned to the scene scale make deep water tint while thin splashes stay clear.
- Practice: for juice, milk or coffee increase density and colour; milk also wants scattering (Subsurface or Volume Scatter).

## Cycles settings

- Light Paths panel, Max Bounces: **Total**, **Transmission** and **Volume** limit those bounce types. Practice: allow enough transmission bounces for glass plus liquid, and keep volume bounces low unless scattering matters.
- **Caustics** checkboxes (Reflective, Refractive) are off switches for noisy caustics. For a cheaper clean result, use the MNEE approach: enable **Shadow Caustics** on the light (or world shader), **Cast Shadow Caustics** on the water object and **Receive Shadow Caustics** on the floor (Caustics section of the Cycles object settings).
- MNEE limits from the manual: only refractive caustics inside shadows are rendered, the caster needs smooth normals, volumetric materials are ignored, bump and normal maps are ignored.

## Foam and whitewater

Render secondary particles (spray, foam, bubbles) as small instances or points with a white diffuse or scatter material (practice).

## Gotchas

- Meshes used for glass refraction and volume rendering should be closed and manifold with normals pointing outwards, otherwise the renderer cannot tell inside from outside.
- EEVEE: set the material **Render Method** to **Dithered** and enable **Raytraced Transmission** (Material > Settings > Surface), with raytracing on in the render settings. Dithered layers can only refract what lies in layers below them; otherwise they fall back to light probes. The EEVEE material **Thickness** setting approximates inner geometry for refraction.
- Water inside glass: practice is to leave a slight gap or overlap at the glass-water interface rather than coincident surfaces.

## Verify

Render over a checker floor: refraction bends the pattern, deeper areas tint, splashes stay clear.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Principled BSDF Transmission Weight meaning; Volume Absorption inputs and typical use; Cycles Light Paths Total/Transmission/Volume bounce names and the Reflective/Refractive Caustics toggles; MNEE caustics object and light toggles and limitations; EEVEE Dithered render method with Raytraced Transmission. Removed: numeric colour/density/bounce values and the Light Path "Is Shadow Ray" trick (no doc coverage), version gates (3.2+, 4.2+), and the claim that fluid meshes are outward by default.
Method: documentation only; no commands were run.
