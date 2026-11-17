---
id: creative-arts.animation.blender.flip-particle-settings
name: flip-particle-settings
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, mantaflow, flip, flip-particle-settings, particle-radius, narrow-band]
level: practitioner
status: docs-checked
description: "Tune Mantaflow FLIP liquid particles: simulation method, particle radius, sampling, randomness, narrow band width and FLIP ratio."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/liquid/index.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# flip-particle-settings

## Liquid settings (Domain > Liquid)

- **Simulation Method**: FLIP (very splashy, many particles in the air) or APIC (very energetic but more stable; preserves vortices better than FLIP).
- **FLIP Ratio** (FLIP only): how much FLIP velocity is used when updating particle velocities. 1.0 is fully FLIP, with more chaotic splashes that suit large quantities of liquid; smaller values are less turbulent with subtler splashes, suited to small-scale scenes.
- **System Maximum**: cap on the total number of fluid particles; 0 lets the solver always sample new particles.
- **Particles Maximum / Minimum**: upper and lower thresholds of liquid particles per grid cell.
- **Particle Radius**: radius of one particle in grid cell units. If liquid seems to disappear, raise it; if too much liquid appears, lower it.
- **Sampling**: factor used when sampling particles; higher samples more particles. Resampling happens at every simulation step.
- **Randomness**: random offset when sampling new particles; 0 samples uniformly inside cells; lower for laminar inflow, higher for turbulent.
- **Narrow Band Width**: width in grid cells of the band in which liquid particles flow. Keep it thin unless you need to visualise particles; raising it can help when the sim leaks volume.
- **Fractional Obstacles**: finer resolution in fluid/obstacle regions, reducing the stepping effect on inclined obstacles. **Obstacle Distance** (negative lets fluid move into the obstacle) and **Obstacle Threshold** (smaller reduces stepping but may make particles stick).
- Enabling Liquid creates a particle system for the simulation; disabling it deletes that system and its settings.

## Gotchas

- Volume gain or loss: adjust Particle Radius first (larger radius if liquid disappears).
- A wide narrow band slows the sim because more particles are simulated.

## Verify

Compare liquid volume at the first and last frames of a settling sim; adjust Particle Radius if it drifts.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/settings (Liquid section); branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Simulation Method FLIP/APIC descriptions, FLIP Ratio, System Maximum, Particles Minimum/Maximum, Particle Radius, Sampling, Randomness, Narrow Band Width, Fractional Obstacles with Obstacle Distance and Threshold, and that enabling Liquid creates a particle system.

Method: documentation only; no commands were run.
