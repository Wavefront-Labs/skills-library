---
id: creative-arts.animation.blender.smoke-shader
name: smoke-shader
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, fire, smoke-shader, fire-shader, smoke-material, principled-volume]
level: practitioner
status: docs-checked
description: "Shade Mantaflow smoke and fire with Principled Volume: density, color and temperature attributes, blackbody intensity, Cycles and EEVEE volume settings."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/volume_principled.html
  - https://docs.blender.org/manual/en/latest/render/materials/components/volume.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/volumes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# smoke-shader

## Default material

The Principled Volume node uses the simulation's volume attributes by default (manual: "The Principled Volume shader will use them by default"). Its relevant inputs:

- **Density** and **Density Attribute** (grid defining the density, typically `density`).
- **Color Attribute**: volume grid for colouring; use `color` for smoke simulations.
- **Temperature Attribute**: grid for blackbody emission, typically `temperature`; **Temperature** is in kelvin and higher values emit more.

Custom volume shaders can read density, color and temperature through the Attribute node. The Volume shader output must be connected to the Volume input of the Material Output.

## Fire

- **Blackbody Intensity** drives blackbody emission for fire; the manual says to set it to 1 for physically accurate intensity. **Blackbody Tint** colours it.
- For artist control use the **Emission Strength** and **Emission Color** inputs of the same node (or an Emission shader added to the volume), driven by a texture or attribute (practice).

## Render

- Cycles: the default volume algorithm is based on null scattering (unbiased, fewer artifacts, possibly noisier). **Step Rate** (Render and Viewport) and **Max Steps** in Render > Volumes exist only with **Biased** ray marching enabled; a larger step rate renders faster but can lose detail. Step size can also be increased per object, material or world.
- EEVEE: Render > Volumes has **Resolution**, **Steps**, **Distribution**, **Max Depth** and an optional **Custom Range**; volumes use 3D textures with high video memory cost. The material Volume > **Intersection** setting (Fast or Accurate) decides which inner part of a mesh produces the volume.
- Practice: dense smoke needs a much higher Density than wispy smoke; tune against the render.

## Gotchas

- Fire looks pink or washed out: check the view transform (practice: compare Standard and AgX).
- The domain shows as a box: the material has no volume output, or only the Surface output is connected.
- Mesh volumes must be closed and manifold with outward normals.
- Noise grids render only if the noise cache is baked (practice).

## Verify

Viewport Rendered mode: smoke is dark and soft, fire glows with a temperature gradient.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Principled Volume input names (Density, Density Attribute, Color Attribute, Temperature, Temperature Attribute, Blackbody Intensity/Tint, Emission Strength/Color) and the "color" attribute note; Cycles null-scattering default with Step Rate and Max Steps only under Biased; EEVEE Volumes panel entries and material Intersection options; closed-manifold mesh volume rule. Removed: the `flame` Attribute recipe, the "Quick Smoke creates Principled Volume" statement, Step Rate 1 / Max Steps 1024 defaults, density figures, and the "Volume shadows" light setting (no doc coverage).
Method: documentation only; no commands were run.
