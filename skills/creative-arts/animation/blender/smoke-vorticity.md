---
id: creative-arts.animation.blender.smoke-vorticity
name: smoke-vorticity
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, gas-sim, smoke-vorticity, vorticity, turbulence]
level: practitioner
status: docs-checked
description: "Add curl to Mantaflow smoke with vorticity, plus turbulence fields and velocity settings to break up columns into billowing plumes."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/turbulence.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# smoke-vorticity

## Vorticity (Domain > Gas)

- **Vorticity**: controls the amount of turbulence in the gas. Higher values make lots of small swirls, lower values make smoother shapes (the manual compares 0.0 and 0.2).
- Fire has its own **Vorticity** in the Fire panel, added to the global value (fire-settings).

## Velocity sources

- Flow Initial Velocity (Source, Normal, Initial X/Y/Z) for jets and explosions (fluid-initial-velocity).
- **Turbulence** force field: random chaotic 3D noise; **Size** is the noise scale and **Global** makes size and strength relative to the world. Turn up Field Weights > Turbulence on the domain if it is reduced there.
- **Wind** to bend plumes; **Vortex** for swirling columns.

## Recipe: billowing explosion

A sphere flow with a Normal initial velocity for a few frames, a positive Buoyancy Heat, some Vorticity, a Turbulence field, and Noise upres for detail.

## Verify

Compare Vorticity 0 against a small positive value on the same setup: the latter shows more small swirls instead of a smooth column.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/settings (Vorticity) and physics/forces/force_fields/types/turbulence; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc, rna_object_force.cc). Confirmed: Vorticity description, fire Vorticity added to the global value, Turbulence field Size and Global options, existence of the Turbulence field weight.

Method: documentation only; no commands were run.
