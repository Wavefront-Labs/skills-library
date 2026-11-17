---
id: creative-arts.animation.blender.fluid-initial-velocity
name: fluid-initial-velocity
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, mantaflow, fluid-initial-velocity, initial-velocity, flow-source]
level: practitioner
status: docs-checked
description: "Give Mantaflow fluids initial velocity: source velocity, normal velocity, explicit XYZ initial velocity and inheriting object motion."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/flow.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fluid-initial-velocity

## Settings (Flow > Initial Velocity)

- **Initial Velocity** checkbox: the fluid inherits the momentum of the flow source.
- **Source**: factor for the inherited velocity; 1 emits fluid moving at the same speed as the source, so an animated bucket throws its water.
- **Normal**: how much velocity fluid gets along face normals. Initial velocities always apply along all face normals, so a closed flow mesh emits in many directions; use a plane (all normals the same way) for one direction.
- **Initial X, Y, Z**: initial velocity along the world axes, usable in addition to Normal.

## Recipes

- Water balloon burst: sphere flow with Normal velocity.
- Hose jet: small cylinder Inflow with Initial velocity along one axis and a few Sampling Substeps.
- Thrown liquid: animate the flow object and use Source.

## Gotchas

- Initial X/Y/Z are world-space, so rotating the emitter does not rotate them; use Normal or a driver for emitter-relative direction.
- Fluid faster than the CFL Number allows is handled by subdividing time steps; keep Adaptive Time Steps on for fast jets (see fluid-domain-resolution).

## Verify

The jet or burst travels in the expected direction; reversing the sign of Initial X/Y/Z reverses it.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/flow and physics/fluid/type/domain/settings; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Initial Velocity checkbox, Source factor meaning, Normal behaviour with closed meshes, Initial X/Y/Z in world space, CFL and adaptive time step behaviour.

Method: documentation only; no commands were run.
