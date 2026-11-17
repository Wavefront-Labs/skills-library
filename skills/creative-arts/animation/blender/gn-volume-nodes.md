---
id: creative-arts.animation.blender.gn-volume-nodes
name: gn-volume-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-volume-nodes, volume-cube, points-to-volume, mesh-to-volume, volume-to-mesh, sdf, clouds]
level: practitioner
status: verified
description: "Make procedural clouds, blob merges and fog volumes with Geometry Nodes volume nodes: Volume Cube density fields, Points/Mesh to Volume, Volume to Mesh, and rendering."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/volume/index.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/volume/primitives/volume_cube.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/point/points_to_volume.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-volume-nodes

Goal: volumetric data made in nodes — no simulation — that renders in Cycles/EEVEE and can be meshed.

## Nodes

- **Volume Cube**: evaluates a **Density** field (which can only depend on Position) on a grid between **Min** and **Max** at **Resolution X/Y/Z** (grid points; N points give N-1 voxels). Density = Noise Texture (Position) → Map Range gives a cloud. **Background** is the value outside the bounds; voxels equal to it are pruned.
- **Points to Volume**: a fog volume sphere of **Radius** around each point; *Resolution Mode* Amount or Size; the grid is named `density`.
- **Mesh to Volume**: fills a mesh into a `density` grid (*Interior Band Width*, *Resolution Mode* Amount or Size).
- **Volume to Mesh**: mesh on the surface at a **Threshold** (iso value; larger voxels are inside), with **Adaptivity** to reduce faces and *Resolution Mode* Grid, Voxel Amount or Voxel Size.
- The Volume > Operations section also holds grid and SDF nodes (Grid to Mesh, SDF Grid Boolean and others; there is no Field to Grid node in 4.5.14) for working on grids directly.

## Recipes

- **Stylized cloud**: Points (few, hand-placed or distributed in a mesh) → Points to Volume (random radius) → Set Material (Principled Volume), then optionally Volume to Mesh → Subdivision for a toon solid cloud.
- **Smooth blob merge**: Distribute Points → Points to Volume → Volume to Mesh (tune Threshold) → Set Shade Smooth.
- **Fog bank**: Volume Cube with Density = Gradient Z × Noise, material Principled Volume.

## Rendering

- Assign a material with Set Material and a volume shader (Principled Volume). Points to Volume and Mesh to Volume name their grid `density`, the grid a volume shader reads for density.

## Gotchas

- Resolution scales cubically: the default of 32 means about 33 thousand density evaluations, 100 about a million and 1000 about a billion. Start low.
- Small changes to Voxel Size in Points to Volume or Mesh to Volume can change processing time a lot.
- Baked volumes are saved as OpenVDB; the rest of the bake format is not an interchange format.

## Verify

Spreadsheet shows the volume grid; Rendered viewport displays density; Volume to Mesh face count is reasonable.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Volume Cube, Points to Volume, Mesh to Volume, Volume to Mesh and Baking pages: inputs, resolution modes, grid name density, evaluation-count note, Threshold meaning. Removed unconfirmed claims: version gates, example numeric values, Object volume render settings behaviour, Bounding Box advice and Bake node VDB export.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Volume Cube has Density, Background, Min, Max, Resolution X, Y, Z (default 32 each) and a Volume output; a Density of Position Z < 0 at resolution 8 and Volume to Mesh gave 258 vertices and 256 faces. Points to Volume and Mesh to Volume Resolution Mode Amount or Size, Mesh to Volume Interior Band Width, Volume to Mesh Resolution Mode Grid, Voxel Amount, Voxel Size with Threshold and Adaptivity. Wrong in the old text: Field to Grid is not present in 4.5.14. Not run (confirmed from the manual only): the density grid name, pruning of background voxels, cost figures (32 cubed is about 33 thousand), OpenVDB baking, the recipes.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
