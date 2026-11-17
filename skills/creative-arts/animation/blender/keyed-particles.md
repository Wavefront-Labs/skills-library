---
id: creative-arts.animation.blender.keyed-particles
name: keyed-particles
category: creative-arts
field: animation
product: blender
tags: [blender, particles, keyed-particles, keyed-physics, keyed-targets]
level: practitioner
status: docs-checked
description: "Use Blender Keyed particle physics to move particles between target particle systems: Key Targets list, Loops, Use Timing with Time and Duration."
sources:
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/physics/keyed.html
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/render.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# keyed-particles

## Concept

The path of Keyed particles is determined between particles of two or more particle systems. The particles have no dynamics: they are interpolated from one system to the next each frame. The feature can chain systems into long strands or moving particles.

## Setup (Particle System > Physics, Type Keyed)

1. You need at least two particle systems in the Keys list.
2. Under **Relations > Key Targets**, add entries; for each key set **Object** (target object; if empty, the current particle system is used) and **System** (index of the particle system on the target object).
3. **Loops**: number of times the entire Keys list is repeated (disabled while Use Timing is on).
4. **Use Timing**: set per-key **Time** (frame at which the particles are at the position of that system; the Start frame of the keyed system adds an offset) and **Duration** (frames the particles stay on that system before moving to the next).

By default Use Timing is off: particles pass through all keys over their lifetime, split equally between the keys, which can give different speeds between targets; a shorter lifetime means faster movement.

## Uses

- Particles flying from a scattered cloud to the positions of a second system.
- Chains of systems for long strands (render with Render As Path).

## Gotchas

- Equal lifetime split between keys can produce uneven speeds when targets are at different distances; use Use Timing for control.
- Check particle counts and emission settings of the target systems when pairing looks wrong.

## Verify

Scrub the timeline: particles reach each target system's positions at the expected times.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Keyed physics, Particle Render panel). Confirmed: keyed concept and at-least-two-keys rule, Key Targets fields, Loops and Use Timing interaction, Time/Duration meaning, default equal split, Path render type compatibility. Removed as unconfirmed: matching-Number requirement, snap/vanish behaviour for mismatched counts, "straight-line interpolation" and the Curve Guide/Geometry Nodes alternative.
Method: documentation only; no commands were run.
