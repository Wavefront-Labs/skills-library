---
id: creative-arts.animation.blender.fluid-flow-objects
name: fluid-flow-objects
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, mantaflow, fluid-flow-objects, inflow, outflow, flow-behavior]
level: practitioner
status: docs-checked
description: "Configure Mantaflow flow objects: geometry, inflow and outflow behaviour, use flow toggle animation, surface emission and planar sources."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/flow.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fluid-flow-objects

## Flow Behavior

- **Geometry**: all regions of the object inside the domain bounding box become fluid; surface normals must point outwards. The real mesh geometry is used, and you can place several flow objects in a domain.
- **Inflow**: the object continuously emits fluid (tap, base of a fire).
- **Outflow**: any fluid entering the object's bounding box is removed (drain); it follows the object if animated.
- **Use Flow** (Inflow and Outflow only) enables or disables the flow and can be keyframed to start and stop a tap.

## Source

- **Flow Source**: Mesh, or Particle System (Fire or Smoke flows only; the particle system must be an Emitter type).
- Mesh options: **Is Planar** (single-dimension or non-manifold meshes), **Surface Emission** (maximum distance in voxels from the surface in which fluid is emitted; results vary with domain resolution), **Volume Emission** (Fire or Smoke only; unpredictable with non-manifold meshes).
- **Sampling Substeps**: reduces gaps in emission from fast-moving sources; substeps happen at each simulation step, not per frame.
- **Vertex Group**: controls where smoke is emitted.

## Recipe: tap

Small cylinder inside the domain, Flow Type Liquid, Flow Behavior Inflow, Initial Velocity on with a downward Initial Z, Use Flow keyframed on then off to stop the stream.

## Gotchas

- Flow objects should be inside the domain's bounding box to work.
- A Geometry flow with flipped normals does not simulate properly.
- Fast-moving inflow without Sampling Substeps leaves gaps in the emitted fluid.

## Verify

The domain shows a continuous stream that starts and stops on the keyed Use Flow frames; the Outflow region stays empty.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/flow; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Flow Behavior (Geometry, Inflow, Outflow) semantics, Use Flow availability, Flow Source options and the particle-system restriction, Is Planar, Surface Emission, Volume Emission, Sampling Substeps, Vertex Group, bounding-box requirement.

Method: documentation only; no commands were run.
