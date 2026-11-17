---
id: creative-arts.animation.blender.cloth-damping
name: cloth-damping
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-damping, air-viscosity, cloth-field-weights, effector-collection, wind, cloth-jitter]
level: practitioner
status: verified
description: "Control Blender cloth energy and forces: tension/compression/shear/bending damping, air viscosity, field weights per force type, and limiting effectors to a collection."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/physical_properties.html
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/field_weights.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/force_field.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# cloth-damping

## Damping (Physics > Cloth > Physical Properties > Damping)

- **Tension**, **Compression**, **Shear** and **Bending** damping: the amount of damping in each behaviour. Higher calms oscillation; too high makes fabric slow and syrupy. With the default Angular bending model the Damping panel shows **Tension** and **Compression** (`tension_damping`, `compression_damping`); with the Linear model it shows one **Structural** damping (the same `tension_damping`) and no Compression. **Shear** (`shear_damping`) and **Bending** (`bending_damping`) show with both. Defaults in 4.5.14: tension, compression and shear 5, bending 0.5.
- **Air Viscosity** (Physical Properties): air thickness that slows falling cloth. Raise it for light, floaty fabric.
- Jittery cloth: raise damping (bending first) and **Quality Steps**, and check that collisions are not fighting each other.

## Field Weights (Physics > Cloth > Field Weights)

Cloth is influenced by external force effectors. The shared Field Weights controls are:

- **Effector Collection**: only effectors in this collection affect the cloth, so a scene's fire wind can be kept off a flag.
- **Gravity**: how much global gravity affects the system.
- **All**: scales all effector weights.
- The panel also carries a weight per force-field type: Force, Vortex, Magnetic, Wind, Curve Guide, Texture, Harmonic, Charge, Lennard-Jones, Boid, Turbulence, Drag and Fluid Flow.

## Recipe: flag

Plane, pin the pole edge (see `cloth-pinning`), pick a fabric preset from the Cloth panel's Presets menu, add a Wind force field and a Turbulence field, set Effector Collection to a collection holding only those fields, then tune Air Viscosity and Bending damping by eye.

## Gotchas

- Force-field strengths use scene force units; tune visually.
- Field weights exist per system (cloth, soft body, particles, rigid body world); set each separately.

## Verify

Cloth settles without residual buzzing at rest; only the intended fields influence it (toggle effectors to confirm).

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: damping names and the Structural-only-in-Linear note, Air Viscosity, Field Weights panel location, Effector Collection, Gravity and All weights. Removed the unconfirmed per-type weight list, example numbers and the flag recipe values.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): ClothSettings tension_damping, compression_damping, shear_damping (all default 5), bending_damping (0.5), air_damping (default 1, panel label Air Viscosity in the shipped properties_physics_cloth.py), quality (default 5); the Damping panel source shows Tension and Compression for the ANGULAR bending model and Structural for LINEAR; EffectorWeights has collection, gravity, all plus the 13 per-type weights listed; RigidBodyWorld also has effector_weights. Not run (confirmed from the manual only): how high damping feels, and the effect of Quality Steps on jitter.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
