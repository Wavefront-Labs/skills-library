---
id: creative-arts.animation.blender.layer-weight-fresnel
name: layer-weight-fresnel
category: creative-arts
field: animation
product: blender
tags: [blender, shader, layer-weight-fresnel, layer-weight, fresnel-node, facing]
level: practitioner
status: docs-checked
description: "Use Blender Layer Weight (Fresnel, Facing) and Fresnel nodes for rim masks, glancing-angle blends, x-ray effects and custom layered materials."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/fresnel.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/layer_weight.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# layer-weight-fresnel

## Fresnel node

- Inputs **IOR** and **Normal** (for bump or normal maps). Output **Factor**: the Fresnel weight, the probability that light reflects off the layer rather than passing through; reflection grows toward grazing angles.
- Use as the Mix Shader factor between two BSDFs: glossy refraction and reflection for simple glass, or diffuse and glossy for a coated material.

## Layer Weight node

- Inputs **Blend** (biases the output toward all 0 or all 1, for uneven mixing) and **Normal**.
- Outputs **Fresnel** (dielectric Fresnel weight like the Fresnel node, but the input is in the more convenient 0 to 1 range) and **Facing** (weight that blends from the first to the second shader as the surface goes from facing the viewer to a grazing angle).
- Facing is the common artist choice for edge glow, x-ray or hologram looks and fake velvet.

## Recipes

- Hologram: Facing -> Color Ramp -> Emission Strength; Add Shader with Transparent.
- Rim light in stylised shading: Facing -> constant Color Ramp -> mix with base colour.

## Gotchas

- Both depend on the shading normal; feed bump or normal map output into Normal for detailed rims.

## Verify

Sphere preview: Facing separates centre from silhouette, and Blend shifts the gradient.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against input/fresnel and input/layer_weight: inputs, outputs (Factor, Fresnel, Facing), Blend meaning, Normal intent. Removed the IOR 1.45 default, the Principled double-reflection claim and the flat-shading facet claim, none of which the manual states.

Method: documentation only; no commands were run.
