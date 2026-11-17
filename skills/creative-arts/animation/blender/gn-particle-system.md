---
id: creative-arts.animation.blender.gn-particle-system
name: gn-particle-system
category: creative-arts
field: animation
product: blender
tags: [blender, gn-particle-system, gn-particles, simulation-nodes, geometry-nodes, particles]
level: advanced
status: docs-checked
description: "Build a particle system in geometry node simulation zones: emission per frame, IDs, velocity and gravity integration, age and lifetime deletion, and instancing for render."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/point/distribute_points_on_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attributes_reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gn-particle-system

Goal: a controllable particle emitter (sparks, debris, dust) without the legacy particle system.

## Layout inside the Simulation Zone

```
Simulation Input.Geometry (existing points) ──────────────────────┐
Emitter mesh ─► Distribute Points on Faces (Seed = Scene Time.Frame, Density) ─► Store: velocity, age=0, lifetime ─► Join Geometry
                                                                                                                      │
   update: velocity += gravity × Δt ; position += velocity × Δt ; age += Δt  ◄─────────────────────────────────────────┘
   Delete Geometry where age > lifetime ─► Simulation Output.Geometry
```

## Node details

1. **Emit**: Distribute Points on Faces on the emitter (*Random* or *Poisson Disk* method; *Density* is points per square metre; its *Normal* output gives the emit direction). Drive *Seed* from the frame so each frame spawns new points, and scale density by Δt for frame-rate independence. Store `velocity` (Normal × speed + Random Value vector jitter), `age` 0 and a random `lifetime`.
2. **Join** new points with the state points.
3. **Integrate**: Set Position with *Offset* = velocity × Delta Time. Store velocity = velocity + (0,0,-9.81) × Δt (+ drag: velocity × (1 - k Δt)).
4. **Age**: Store `age` = age + Δt; Delete Geometry (*Domain* Point, *Mode* All) where `age > lifetime`.
5. **Output** the points; outside the zone, Instance on Points (scale by age curve) → Realize Instances if needed, Set Material.

## IDs and stability

Distribute Points on Faces writes a stable built-in `id` attribute, and Random Value uses `id` by default (index if there is none), so keep the attribute for stable per-particle randomness.

## Gotchas

- Delta Time is the time in seconds between frames; driving rates with it keeps playback consistent when the frame rate changes.
- Point counts grow without deletion: always kill by age or bounds.
- A built-in Point-domain vector attribute named `velocity` is used to create motion blur when rendering animations.
- Anonymous attributes are not carried through the zone unless stored in the simulation state; store needed values under names.

## Verify

Play from frame 1: steady emission, parabolic arcs, particles disappear after their lifetime; the Spreadsheet point count stabilises instead of growing forever.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Simulation Zone, Distribute Points on Faces, Set Position, Delete Geometry, Instance on Points and Attributes Reference pages: Delta Time, Seed, Density units, stable id, velocity attribute for motion blur, anonymous attribute rule. Removed the unconfirmed claim about ids staying unique across joins.

Method: documentation only; no commands were run.
