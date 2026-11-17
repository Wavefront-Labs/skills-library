---
id: creative-arts.animation.blender.particle-instance-modifier
name: particle-instance-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, particle-instance, modifiers, particles, hair, create-along-paths]
level: practitioner
status: docs-checked
description: "Duplicate a mesh at another object's particles with Blender's Particle Instance modifier: Show states, Amount/Offset, Create Along Paths, colour layers."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/physics/particle_instance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# particle-instance-modifier

## What it does

The mesh of the modified object is duplicated at the location of the particles of a selected particle system on another object (at least one other object with a particle system is required). Results depend heavily on the target system's settings.

## Settings

- **Object** and **Particle System**: the target object and which of its systems to use.
- **Create Instances**: *Regular* (parent particles), *Children* (child particles), *Size* (scale copies by the particle size attribute; otherwise all copies keep the origin size).
- **Show**: *Unborn*, *Alive*, *Dead* particles.
- **Amount**: proportion of particles used, skipped randomly. Statistically correct only: with few particles the real count can deviate noticeably (the manual's example is 100 particles at 0.1 giving about 5 to 15 instances).
- **Offset**: relative offset in the particle range, to avoid overlap when several modifiers share one system; to fully avoid overlaps, Offset must be at least Amount.
- **Coordinate Space**: *World* (copy locations depend on both the modified and target objects) or *Local* (only the modified object).
- **Axis**: pole axis of the modified object used to apply the particle rotation.

## Create Along Paths

Instead of sitting at the particle's current position, the instance follows and deforms along the particle path or hair strand.
- **Position**: percentage of the path filled (or position on the path with Keep Shape); **Random** adds variation.
- **Rotation** around the path; **Random** adds variation.
- **Keep Shape**: no deformation, the instance is only placed on the path.
- The particle system must be baked, except Hair type or Keyed physics. Hair particles die as soon as they are created, so enable *Dead* in Show for this to work.
- The mesh needs enough loop cuts along its length to bend.

## Layers

*Index* and *Value* choose Color Attributes filled from particle index and random per-particle values, usable in a shader for variation. They must be in the face corner domain with byte color data type.

## Verify

Copies follow particles; with Create Along Paths the geometry bends along each strand.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Particle Instance page). Confirmed all options and notes above. Corrected: Layers write Color Attributes of a specific domain/type; added Offset, Keep Shape and Dead-state requirement. Removed unconfirmed performance and use-case advice.
Method: documentation only; no commands were run.
