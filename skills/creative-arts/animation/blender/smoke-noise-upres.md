---
id: creative-arts.animation.blender.smoke-noise-upres
name: smoke-noise-upres
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, gas-sim, smoke-noise-upres, noise-upres, wavelet-noise]
level: practitioner
status: docs-checked
description: "Add detail to Mantaflow smoke with the Noise upres pass: upres factor, strength, scale, time anim, and baking noise separately in Modular cache."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/gas/noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# smoke-noise-upres

## How it works

Noise adds finer detail on top of the base gas simulation without changing the overall fluid motion (an implementation of Wavelet Turbulence for Fluid Simulation). With the Modular cache it is baked separately: Bake Data first, then Bake Noise.

## Settings (Domain > Noise)

- **Noise** checkbox: lets the cache know which data to read. With no baked noise it shows an empty domain; it does not reset the cache and switches the view between base resolution and noise.
- **Upres Factor**: factor by which the noise resolution is enhanced, coupled to Resolution Divisions.
- **Strength**: higher values give more turbulent vortices.
- **Scale**: greater values give larger vortices.
- **Time**: animation time of the noise; it can be used as a seed so two otherwise identical domains look slightly different.
- **Bake Noise / Free Noise**: Modular cache only; Esc pauses, and a bake can be resumed.

## Workflow

1. Settle the motion with the base resolution and bake Data.
2. Enable Noise, bake Noise and review.
3. Adjust Upres Factor, Strength and Scale and rebake the noise only.

## Gotchas

- Resolution Divisions and Upres Factor are not equivalent: different combinations give different styles of smoke. A low base resolution with a high Upres Factor generally looks smaller in real-world scale.
- Noise cannot add large-scale motion; swirls must come from the base sim (vorticity, resolution).

## Verify

Compare the same frame with and without Noise: the silhouette stays similar and the internal detail increases.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/gas/noise; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Noise checkbox behaviour, Upres Factor, Strength, Scale (greater = larger vortices), Time as seed, the resolution note, and Bake Noise availability.

Method: documentation only; no commands were run.
