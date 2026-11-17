---
id: creative-arts.animation.blender.volume-step-rate
name: volume-step-rate
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, volume-step-size-render, step-rate, max-steps, volumetrics]
level: practitioner
status: docs-checked
description: "Tune Cycles volume rendering cost: the Biased toggle, step rate for render and viewport, Max Steps, per-object Step Size, material Sampling Method and Interpolation."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/render/cycles/material_settings.html
  - https://docs.blender.org/manual/en/latest/modeling/volumes/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# volume-step-rate

Goal: smoke, fog and clouds that render in reasonable time.

## Render Properties > Volumes (Cycles)
- **Biased** (off by default): the default algorithm is based on null scattering, which is unbiased with fewer artifacts but could be noisier. Biased uses ray marching with controls for step size and max steps. Everything below only exists when Biased is on.
- **Step Rate Render** and **Viewport**: global multipliers on the step size of all volumes (default 1.0). Higher reduces render or viewport time but loses detail; lower renders more detail.
- **Max Steps** (default 1024): maximum steps through a volume before giving up, protecting against huge render times with big objects or small step sizes.
- Cycles estimates step size automatically from voxel size in volume objects and smoke simulations. For procedural shaders that add detail, the manual says step size can be increased per object, material or world.

## Per object and material
- Volume object: Object Data > Render > **Step Size** (0 = automatic from voxel size) and **Space** (Object or World).
- Material Properties > Settings > Volume (Cycles): **Sampling Method** (Distance for dense volumes lit from far away; Equiangular for a light inside or near the volume; Multiple Importance, the default, for a combination) and **Interpolation** (Linear for thin volumes; Cubic is smoother and needed for denser volumes, but slower). **Step Rate** (Biased only): material-level step multiplier, mainly to reduce the step size for procedural shaders whose detail the default step misses.

## Gotchas
- The Step Rate fields are disabled unless Biased is enabled.
- Too high a step rate loses small wisps.

## Verify
With Biased on, render one frame at Step Rate 1 and 2, and compare time and a crop of fine detail.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Cycles Volumes panel and Material Settings, Volume Properties), branch blender-v5.2-release; defaults from the Cycles add-on properties.py on the Blender main branch. Confirmed: Biased toggle and default, Step Rate and Max Steps behaviour and defaults, sampling and interpolation options. Removed the Homogeneous material option (not in the manual or the add-on properties), the Volume Resolution Simplify advice, density clamping tips, and the unconfirmed claim that Step Rate 2 halves the steps.
Method: documentation only; no commands were run.
