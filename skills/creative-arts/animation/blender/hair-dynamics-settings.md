---
id: creative-arts.animation.blender.hair-dynamics-settings
name: hair-dynamics-settings
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-dynamics, hair-dynamics-settings, hair-stiffness, particle-hair]
level: practitioner
status: docs-checked
description: "Simulate legacy particle hair with Blender Hair Dynamics: quality steps, pin goal strength, structure, volume (air drag, friction, density) and collision settings."
sources:
  - https://docs.blender.org/manual/en/latest/physics/particles/hair/dynamics.html
  - https://docs.blender.org/manual/en/latest/physics/particles/hair/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hair-dynamics-settings

## Enable
Particle properties > hair particle system > **Hair Dynamics** panel, checkbox in the panel header. This is the legacy hair particle system; Curves objects do not have this panel (convert with hair-convert-particles).

## Main settings
- **Quality Steps** (steps per frame; higher is better and slower).
- **Pin Goal Strength**: spring stiffness of the vertex target position.
- Motion blur needs one extra baked frame past the last rendered frame.

## Structure
**Vertex Mass**, **Stiffness** (bending; **Random** variation), **Damping** (bending motion).

## Volume
Volumetric model on a voxel grid: **Air Drag**, **Internal Friction** (friction between hairs), **Voxel Grid Cell Size**, **Density Target** (maximum density) and **Density Strength** (influence of the target).

## Collisions
**Quality**, **Distance** (how close an object may get before hair is repelled), **Impulse Clamping** (restricts movement after a collision), **Collision Collection**: only objects in that collection collide, and they must also have Collision physics enabled.

## Gotchas
- Small collision Distance can cause errors; large values look unrealistic and run slowly.
- Bake before rendering, as with other particle caches.

## Verify
Animate the head: hair lags and settles, and no strands pass through the collision mesh.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed panel names, every setting listed and the motion blur and collision collection notes on the Hair Dynamics page. Removed numeric ranges (stiffness 0.5-5, quality steps 5-10), the Particle Edit pin-weight claim, the proxy-body advice, the children-simulation claim and the Simulation Nodes suggestion, which the docs do not cover.
Method: documentation only; no commands were run.
