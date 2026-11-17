---
id: creative-arts.animation.blender.cloth-pressure-internal-springs
name: cloth-pressure-internal-springs
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-pressure, pressure, target-volume, cloth-internal-springs, internal-springs, inflatables, soft-objects]
level: practitioner
status: verified
description: "Make inflatables, cushions and squishy solids with Blender cloth Pressure (target volume, scale, fluid density) and Internal Springs (max length, normals, tension)."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/physical_properties.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# cloth-pressure-internal-springs

Both panels are under Physics > Cloth > Physical Properties, each enabled by a checkbox in its panel header.

## Pressure

- API (`ClothSettings`): `use_pressure`, `uniform_pressure_force`, `use_pressure_volume`, `target_volume`, `pressure_factor` (default 1), `fluid_density`, `vertex_group_pressure`; internal springs `use_internal_springs`, `internal_spring_max_length`, `internal_spring_max_diversion` (default and maximum 45 degrees), `internal_spring_normal_check` (default on), `internal_tension_stiffness`, `internal_compression_stiffness` (default 15), each with a `_max` field.
- Models soft-shelled objects such as balloons or balls filled with a gas.
- **Pressure**: uniform pressure applied constantly, in units of Pressure Scale; negative values simulate implosions or outside pressure pushing in.
- **Custom Volume** + **Target Volume**: use Target Volume as the initial volume instead of computing it from the mesh; Target Volume is the volume where inner and outer pressure are equal (zero means volume changes do not affect pressure).
- **Pressure Scale**: ambient pressure (kPa) inside and outside; raise it so the object resists volume change more. For an incompressible liquid feel, set it as high as possible without breaking the sim.
- **Fluid Density**: density of the contained fluid in kg per litre (1 for water), giving a hydrostatic gradient so a heavy fill sags; negative models buoyancy from a surrounding fluid. The fluid is not simulated, and volume is not preserved on its own (combine with Pressure Scale).
- **Vertex Group**: weight 0 applies no pressure, 1 full pressure. Faces with a zero-weight vertex are excluded from the Target Volume calculation.

## Internal Springs

- Adds 3D springs through the volume so a mesh behaves like a Soft Body while still using the cloth solver.
- **Max Spring Creation Length** (0 = no limit), **Max Creation Diversion** (largest angle from the vertex normal allowed when connecting internal points), **Check Surface Normals** (connected points must have opposite normals), **Tension**, **Compression**, **Vertex Group**, **Max Tension**, **Max Compression**.

## Recipes (starting points to tune)

- **Cushion**: closed box mesh, Pressure on, Internal Springs on, collide with a proxy of whatever sits on it.
- **Inflating text**: convert to mesh and remesh, Cloth with Pressure animated up from zero, Self-Collisions on.

## Gotchas

- Non-manifold meshes work, but pressure escapes through holes and causes drifting or propulsion; use the Pressure Vertex Group to exclude the open parts.

## Verify

Volume grows and shrinks as animated (watch the silhouette); squeezing contacts deform and recover.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: every Pressure and Internal Springs field name and meaning in Physical Properties. Corrected the claim that open meshes cannot hold pressure (they work but leak). Removed recipe numbers and the explosion and long-thin-part claims no doc covers.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): every ClothSettings property named in the new API bullet exists with the stated defaults and ranges (Create Internal Springs, Use Pressure, Use Custom Volume, Pressure Scale, Fluid Density, Pressure Vertex Group, Tension/Compression Stiffness and Maximum, Max Length, Max Diversion, Check Internal Spring Normals). Not run (confirmed from the manual only): units (kPa, kg per litre), what each setting does physically, and the recipes.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
