---
id: creative-arts.animation.blender.gn-collision-simulation
name: gn-collision-simulation
category: creative-arts
field: animation
product: blender
tags: [blender, gn-collision-simulation, gn-collisions, raycast, simulation-nodes, geometry-nodes, geometry-proximity]
level: advanced
status: docs-checked
description: "Make geometry node simulations collide with meshes: Raycast along velocity, reflect and damp on hit, Geometry Proximity push-out, collider inputs and tunnelling fixes."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/sample/raycast.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/sample/geometry_proximity.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/collider.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gn-collision-simulation

Goal: particles bounce off floors and props instead of passing through.

## Built-in Collider node

The manual lists a **Collider** node (Simulation nodes) that marks a mesh as an external collider for simulation nodes. Inputs: *Geometry*, *Deforming* (enable if the collider deforms; disable for static or only instance-transformed colliders for speed), *Boundary* (keeps colliding geometry inside instead of outside), *Edge Contacts* (currently only supported for curve geometry, i.e. hair), *Margin*, *Friction*, *Softness* and *Filter* (comma-separated tags; only simulated geometry with a matching tag collides). The XPBD Solver node consumes colliders through its *World* input and is used by the Hair Dynamics and Cloth Dynamics experimental assets; it is intended to sit inside friendlier assets. Use these when the solver in your file supports them; the hand-built version below works with a plain Simulation Zone.

## Collider input (hand-built)

Object Info node for the collider object (*Transform Space*: Original or Relative; *As Instance* option), or Collection Info for many; use Realize Instances if you need real geometry, then pass it into the simulation zone. Links from outside into the zone are re-evaluated each step at the current frame.

## Raycast collision (inside the zone, before integrating position)

```
step = velocity x Delta Time
Raycast(Target Geometry = collider, Source Position = position, Ray Direction = normalize(step), Ray Length = length(step) + radius)
if Is Hit:
    position = Hit Position + Hit Normal x radius
    velocity = reflect(velocity, Hit Normal) x bounce
    tangential friction: subtract (velocity - dot(velocity, N) N) x friction
else:
    position += step
```
Build the branch with Switch nodes (Vector type) controlled by *Is Hit*. Vector Math has *Reflect*, *Dot Product* and *Normalize* operations. Bounce and friction values are yours to tune.

## Push-out safety net

Geometry Proximity (Target Element *Faces*) gives the closest *Position*, *Distance* and *Is Valid* but no normal. For a push-out direction use the Raycast *Hit Normal*, or push along (position minus nearest position) when it is non-zero.

## Tunnelling

- A ray length covering the whole step stops fast particles skipping thin colliders.
- A Repeat Zone (*Iterations* = N) inside the Simulation Zone with Delta Time / N per iteration handles very fast motion.

## Gotchas

- The Raycast *Hit Normal* is the surface normal at the hit; flipped normals reflect the wrong way.
- Rays test only the current frame's collider shape, so very fast colliders can still penetrate.
- Dense collider meshes make every ray expensive; use a decimated proxy.

## Verify

Drop a stream onto a tilted plane: particles bounce and slide off; increase speed and confirm none pass through (check with a camera under the plane).

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Raycast, Geometry Proximity, Collider, XPBD Solver, Simulation Zone, Repeat Zone and Object Info pages: socket and output names, Proximity has no normal output, Collider options. Removed unconfirmed numeric ranges and the claim that Object Info re-evaluates per frame. Corrected the push-out step, which relied on a normal Geometry Proximity does not output.

Method: documentation only; no commands were run.
