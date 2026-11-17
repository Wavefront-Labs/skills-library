---
id: creative-arts.animation.blender.particle-physics-newtonian
name: particle-physics-newtonian
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-physics-newtonian, newtonian, brownian, drag, damp]
level: practitioner
status: docs-checked
description: "Set Blender Newtonian particle physics: forces (brownian, drag, damp), integrators, timestep and subframes, and deflection options for stable motion."
sources:
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/physics/newtonian.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/physics/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# particle-physics-newtonian

## Physics Type

Particle System > Physics > Type: None, **Newtonian**, Keyed, Boids, Fluid. Newtonian particles start with the specified initial velocities and move according to external forces, computed with the chosen integrator.

## Newtonian settings

- **Size**, **Random Size**, **Mass** exist as particle settings (Python: `particle_size`, `size_random`, `mass`).
- **Forces** panel: **Brownian** (random motion from a Brownian noise field, nice for small random wind forces), **Drag** (reduces velocity in relation to speed and size; air or water drag), **Damp** (reduces velocity: deceleration, friction).
- **Integration**:
  - Euler: simplest and fastest, least exact; without damping energy grows over time. For short or heavily damped simulations.
  - Verlet: very fast and stable, energy conserved with little numerical dissipation.
  - Midpoint: second-order Runge-Kutta, slower than Euler but much more stable, and the manual's general-purpose choice.
  - RK4: slower than Midpoint and in most cases more accurate; only needed when Midpoint is not accurate enough.
- **Timestep**: simulation time in seconds per frame. **Subframes**: simulation steps per frame; use higher values for faster particles.
- **Adaptive** subframes with **Threshold**: the manual lists these as available only for Fluid type physics.
- **Deflection** panel: **Size Deflect** (use particle size in deflections), **Die on Hit**, **Collision Collection** (limit colliders to a collection).

## Gotchas

- Particles passing through thin colliders: raise Subframes and enable Size Deflect.
- High Brownian values give jittery motion; a Turbulence force field gives a smoother wander (practical advice, not from the manual).

## Verify

Trajectories are smooth (show paths or trails) and particles do not pass through the floor on playback. Bake before rendering (see cache-step).

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and rna_particle.cc on main.
Confirmed: panel names and options, integrator descriptions, Adaptive being Fluid-only per the manual, Deflection panel, RNA names for size, random size and mass, physics type list.
Removed as unconfirmed: "Midpoint (default)", drag proportional to velocity squared, "Mass affects force fields, not gravity", subframes 5-10 and the Snow and Embers recipe numbers, "Fluid (SPH, legacy)" wording, and the Rotation item.
Method: documentation only; no commands were run.
