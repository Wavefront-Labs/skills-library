---
id: creative-arts.animation.blender.particle-emission
name: particle-emission
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-emission, particle-lifetime, emission-source, emitter]
level: practitioner
status: docs-checked
description: "Configure Blender emitter particles: Number, Seed, Frame Start/End, Lifetime and randomness, Emit From vertices/faces/volume, Distribution, Random Order, Even Distribution."
sources:
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/emission.html
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/vertex_groups.html
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/display.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# particle-emission

## Emission panel (Particle System > Emission)

- **Number**: the maximum amount of parent particles used in the simulation.
- **Seed**: starting point for the random numbers of the simulation; use different seeds for duplicated systems.
- **Frame Start / End**: emission window. Start may be negative so the simulation begins before the rendered range.
- **Lifetime**: lifespan in frames. **Lifetime Randomness**: the shortest lifetime is Lifetime x (1 - Random); values above 1.0 are not allowed (Lifetime 50 with Random 0.5 gives 25 to 50 frames).

## Source

- **Emit From**: *Vertices*, *Faces*, *Volume* (volume needs a manifold mesh; modifiers such as Edge Split that break up the surface break volume emission).
- **Use Modifier Stack**: takes modifiers above the Particle modifier into account; otherwise the original mesh is used. Particles may differ in the render if modifiers generate different geometry in viewport and render.
- **Distribution** (Faces or Volume):
  - *Jittered*: Particles/Face (0 = automatic) and Jittering Amount.
  - *Random*: random locations on the emitter elements.
  - *Grid*: particles in a 3D grid, those near or in the elements kept; Invert Grid, Hexagonal, Resolution, Random.
- **Random Order**: go through emitter element indices in random order (not available for Grid).
- **Even Distribution**: even density based on the surface area of the elements, so small elements emit fewer particles.
- Vertex Groups panel: **Density** (density of the particle distribution) and **Length** (length of the hair) vertex groups, plus child-related groups; each can be negated.

## Recipes

Choose Frame Start/End and Lifetime to shape the effect: a burst uses a short window (End close to Start), a continuous stream a long window; negative Start gives a pre-roll.

## Gotchas

- Render > Show Emitter off hides the emitter mesh in renders.
- Viewport Display > **Amount** is the percentage of particles shown in the viewport (all particles are still rendered); lower it for heavy systems.

## Verify

Scrub the timeline: particles appear between Frame Start and End and disappear after Lifetime frames. To count live particles in a script, read `alive_state` on `ParticleSystem.particles` of the evaluated object (the enum includes `ALIVE`).

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Particle Emission, Vertex Groups, Viewport Display, Render) and 5.2 source enum for `alive_state`. Confirmed: all Emission and Source options above, Lifetime Randomness formula, Show Emitter, Amount, Density/Length vertex groups. Corrected: Number is the maximum count of parent particles (not a per-window total with a documented rate formula); Random Order was missing. Removed as unconfirmed: sample recipe numbers, "changing Number reseeds positions", and the exact status-bar particle count method.
Method: documentation only; no commands were run.
