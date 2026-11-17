---
id: creative-arts.animation.blender.vegetation-scattering
name: vegetation-scattering
category: creative-arts
field: animation
product: blender
tags: [blender, vegetation-scattering, vegetation, plant-scattering, gn-scatter, environment-modeling, instancing]
level: practitioner
status: docs-checked
description: "Scatter vegetation in Blender geometry nodes: Poisson spacing, density masks, picking collection instances, normal alignment, random scale and seeds."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/point/distribute_points_on_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/instances/instance_on_points.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vegetation-scattering

Goal: natural-looking grass, bushes and trees on terrain that render quickly.

## Geometry nodes setup (on the terrain)

```
Group Input ─► Distribute Points on Faces (Poisson Disk; Distance Min, Density Max, Density driven by a mask)
           ─► Instance on Points (Instance = Collection Info, Pick Instances on,
                                  Rotation from the Rotation output or Align Rotation to Vector, Scale = random)
           ─► Join Geometry (with original terrain) ─► Group Output
```
- **Distribute Points on Faces** needs a mesh with faces. In *Poisson Disk* mode, *Distance Min* is the minimum spacing between points and *Density Max* is points per square metre, multiplied by the *Density* input to give the final density. Density Max is capped by Distance Min: once the spacing cannot fit more points, none are added. At the default Distance Min of zero, Poisson Disk behaves like *Random*, which is the fastest method.
- **Masks**: point, corner and polygon attributes of the terrain, including vertex weights and UV maps, are transferred to the generated points, so a weight-painted vertex group can be read on the points for hand-placed areas. Multiply further masks (slope from the normal, altitude from Position Z, noise for patchiness) into the density.
- **Pick Instances** chooses one item per point from the instance list of the *Instance* input; the manual says it is intended for use with Collection Info. *Instance Index* defaults to the point ID (or the index if no ID exists), and out-of-range or negative values wrap around, so random indexes work and duplicating a common plant in the collection raises its odds.
- **Rotation**: Distribute Points on Faces outputs *Normal* and an Euler *Rotation* built from it (smooth and custom normals are used by default). Its Z rotation is arbitrary because a normal cannot fix all three axes, so add your own random Z spin. An Euler can also be built from any direction with Align Rotation to Vector. Mixing the normal with world Z keeps trees upright while grass follows slopes.
- The node generates a stable `id` attribute per point, so points stay consistent when the mesh deforms or the density changes, and it feeds Random Value and Instance on Points.

## Layers

Use separate modifiers or node groups for trees, bushes, grass and rocks with different spacing, and a different seed per layer (the *Seed* input), or every layer picks the same points.

## Performance

Instances are a fast way to add the same geometry many times without duplicating the underlying data, so keep plants as instances rather than converting them to real geometry. The `duplicates_make_real` operator is available when you need real objects from instances.

## Gotchas

- Instance on Points works on any geometry with a Point domain; it cannot instance Metaball objects.

## Verify

Viewport shows plants only where masks allow, and no regular pattern is visible from the camera.

## Checked

2026-11-09. Confirmed against the Blender manual Distribute Points on Faces and Instance on Points pages (raw RST, both read in full): Random and Poisson Disk methods, Distance Min, Density Max (per m2, capped), Density, Seed, Normal / Rotation outputs and the arbitrary Z, attribute transfer, stable id, Pick Instances with Collection Info, Instance Index default and wrapping, Align Rotation to Vector, duplicates_make_real, Metaball limitation. Removed: specific numbers (0.3, 5, 0.7-1.3), slope formula, Is Viewport / Viewport Density, camera culling, Geometry Proximity exclusion, Scatter Objects and legacy hair alternatives, and memory claims about Realize Instances (not on the pages). Also removed the apply-scale gotcha (not on the pages).
Method: documentation only; no commands were run.
