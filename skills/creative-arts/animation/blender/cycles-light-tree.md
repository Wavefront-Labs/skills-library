---
id: creative-arts.animation.blender.cycles-light-tree
name: cycles-light-tree
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, light-tree, many-lights, emission-sampling, light-threshold]
level: practitioner
status: docs-checked
description: "Render many-light scenes in Cycles with the light tree: what it accounts for, light threshold, emission sampling per material, and when to compare it off."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/cycles/material_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-light-tree

Goal: keep noise down in scenes with many lights (city nights, string lights, emissive panels).

## Settings

- Render Properties > Sampling > Lights > **Light Tree**: samples lights more effectively by taking distance and estimated intensity into account. It can significantly reduce noise, at the cost of a somewhat longer render time per sample.
- **Light Threshold**: probabilistically terminates light samples whose contribution is below the threshold, to avoid wasting time on lights that contribute little. Zero disables the test.
- Material Properties > Settings > **Emission Sampling** (only has an effect if the material has an emissive node):
  - None: do not use the surface as a light for sampling.
  - Auto: decide from emission intensity.
  - Front: only the front side acts as a light; useful for closed meshes whose interior is not visible.
  - Back: only the back side.
  - Front and Back: both sides.

## Limits of the light tree

The manual states that some lighting properties are not accounted for in the tree: custom falloff, ray visibility, and complex shader node setups including textures. Noise can increase in scenes that rely on these.

## Workflow

- Because the tree adds per-sample cost, compare Light Tree on and off at equal render time in simple scenes with few lights.
- Set Emission Sampling to None on emitters that only need to be seen directly, and Front on closed emissive meshes.
- Use light linking when a fixture should only light selected objects.

## Verify

Render the same frame with Light Tree on and off at equal time and compare noise in areas lit by small lights.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Sampling, Material settings). Confirmed: Light Tree and Light Threshold descriptions, light tree limits, Emission Sampling options. Removed unconfirmed: default values, version gate, memory/sync-time claims, "instanced lights" claim, world-light statement.
Method: documentation only; no commands were run.
