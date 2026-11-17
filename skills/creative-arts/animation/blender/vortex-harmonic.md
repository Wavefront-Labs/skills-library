---
id: creative-arts.animation.blender.vortex-harmonic
name: vortex-harmonic
category: creative-arts
field: animation
product: blender
tags: [blender, force-fields, vortex-harmonic, vortex, harmonic, magnetic, charge]
level: practitioner
status: docs-checked
description: "Use Blender Vortex, Harmonic, Magnetic, Charge and Lennard-Jones force fields for swirls, springs and particle attraction effects."
sources:
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/vortex.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/harmonic.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/magnetic.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/charge.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/lennard_jones.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/force.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vortex-harmonic

## Vortex

Gives a spiraling force that twists the direction of points around the force object's local Z axis; useful for a swirling sink, a tornado, or kinks in particle hair. Strength can be positive or negative to change the spin direction. **Inflow** is the inwards component of the vortex force (shown when the shape is not Point). Pair it with a Force field of negative strength (attracts toward the origin) for a tornado or whirlpool.

## Harmonic

The field source is the zero point of a harmonic oscillator (spring, pendulum). **Rest Length** sets the spring's rest length; **Damping** of 1 stops the movement at the moment the object is reached. **Multiple Springs** makes every point be affected by multiple springs. Assigned to particles, each target particle is assigned to a field particle, so particles move to the places of other particles and form shapes.

## Magnetic

Depends on the speed of the particles; it simulates the force of magnetism on magnetized objects.

## Charge

Similar to Force but attracts or repels depending on the charge of the affected particle (negative or positive). It only affects particles that also have a Charge field, which a particle system can carry via Particle System > Force Field Settings.

## Lennard-Jones

A very short-range force: very repulsive at distances smaller than the combined sizes of effector and affected particle, attractive beyond that. It tries to keep particles at an equilibrium distance, and particles must be close to each other to be affected.

## Tornado recipe

Empty with a Vortex field using a Tube falloff and a Max Distance, a Force field at the same spot with negative strength, and a Wind field pointing upward. Particles use Newtonian physics.

## Gotchas

- Soft bodies react only to Force, Wind and Vortex fields (Harmonic is not useful for them).
- Fields affect everything by default: use Max Distance and Field Weights to limit them.

## Verify

Particles visibly rotate around the Z axis; reversing Strength reverses the spin.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/forces/force_fields/introduction and types vortex, harmonic, magnetic, charge, lennard_jones, force; branch blender-v5.2-release) and the 5.2 source (properties_physics_common.py). Confirmed: Vortex axis, direction and Inflow, Harmonic Rest Length, Damping and Multiple Springs behaviour, Magnetic, Charge (only affects particles with a Charge field) and Lennard-Jones descriptions, Force sign semantics, soft body support list; Inflow shown only when shape is not Point (properties_physics_common.py).

Method: documentation only; no commands were run.
