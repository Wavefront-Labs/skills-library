---
id: creative-arts.animation.blender.gn-scatter
name: gn-scatter
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-scatter, distribute-points, distribute-points-on-faces, instance-on-points, poisson-disk, scattering]
level: practitioner
status: docs-checked
description: "Scatter rocks, grass and props with Geometry Nodes: Distribute Points on Faces (Random vs Poisson Disk, density by weight/attribute), Instance on Points with collection pick, random rotation/scale."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/point/distribute_points_on_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/instances/instance_on_points.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gn-scatter

Goal: controllable, non-overlapping, art-directable scattering that stays light (instances).

## Core tree

`Group Input Geometry → Distribute Points on Faces → Instance on Points (Instance = Collection Info with Separate Children + Reset Children, Pick Instances on) → Join Geometry (with original) → Group Output`

## Distribute Points on Faces

- **Random** (the fastest method): **Density** is points per square metre on each face and is multiplied by the values of the density attribute (the manual calls it *Density Attribute*); drive it with a painted vertex group via Named Attribute or a noise.
- **Poisson Disk**: **Distance Min** (minimum spacing; at zero it behaves like Random), **Density Max** (points per m², multiplied by Density; capped by Distance Min).
- **Seed**: change to reshuffle.
- Outputs **Normal** and **Rotation** (an Euler rotation from the normal whose Z spin is arbitrary): plug Rotation into Instance on Points for normal-aligned instances, or use Align Rotation to Vector, and blend toward world Z for grass that stays upright on slopes.
- The node writes a stable `id`; when the mesh is deformed or density changes the values stay consistent for the remaining points.

## Instance on Points variety

- Collection Info (*Separate Children*, *Reset Children*) + **Pick Instances** on. **Instance Index** defaults to the point ID (or index); wrapped if out of range. Children are sorted alphabetically, and renaming does not re-evaluate the modifier automatically.
- **Rotation** = Random Value (Vector) combined with the normal rotation via Rotate Rotation.
- **Scale** = Random Value Float in a range such as 0.7 to 1.3.

## Art direction

- Density from a vertex group painted on the terrain (Weight Paint, then Named Attribute).
- Exclusion: Geometry Proximity to a path curve → Map Range → Density Factor (no rocks on the road).
- Slope filter: Compare Normal Z > 0.8 to keep grass off cliffs.

## Gotchas

- Instances are a fast way to repeat the same geometry without duplicating data; realised instances take more memory, so Realize Instances only when needed (export, booleans).
- Instance on Points only supports objects with geometry; use Object Info for lights, and metaballs are not supported.

## Verify

Spreadsheet Instance domain count is in budget; viewport shows no interpenetrations at the Poisson Distance Min.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Distribute Points on Faces, Instance on Points and Collection Info pages: distribution methods, Distance Min and Density Max, stable id, Pick Instances and Instance Index defaults, Separate and Reset Children. Removed unconfirmed claims: Density Factor input name and 0..1 range, scale-dependence of counts, reshuffle on topology change, Statistics overlay behaviour.

Method: documentation only; no commands were run.
