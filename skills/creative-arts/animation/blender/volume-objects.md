---
id: creative-arts.animation.blender.volume-objects
name: volume-objects
category: creative-arts
field: animation
product: blender
tags: [blender, volume-object, openvdb, vdb, volumes, vdb-sequence, mesh-to-volume, volume-to-mesh, volume-displace, grids, density, clouds, embergen, houdini-vdb]
level: advanced
status: docs-checked
description: "OpenVDB volume objects in Blender: VDB sequences, grids, viewport and render properties, and the Mesh to Volume, Volume to Mesh and Volume Displace modifiers."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/volumes/properties.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mesh_to_volume.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/volume_to_mesh.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/volume_displace.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# volume-objects

Goal: bring sparse OpenVDB volumes in, shade and render them, and convert between meshes and volumes.

## Importing VDB

- Object Data (Volume tab) → **OpenVDB File**: *File Path*, *Sequence*, *Frames* (how many frames of the sequence to use), *Start* (scene frame at which the sequence starts), *Offset* (frames of the sequence to skip at the beginning), *Mode* (Clip / Extend / Repeat / Ping-Pong: behaviour before the first and after the last frame).
- Sequence files need a numerical suffix: if you pick `smoke-000.vdb`, Blender expects `smoke-001.vdb`, `smoke-002.vdb` and so on.
- **Grids** panel: lists the grids in the VDB with name and data type. A grid is a set of volumetric data, typically density, but also temperature, velocity and so on. Click a grid to make the volume object display it.

## Viewport and render settings

- Viewport Display: *Wireframe* (None / Bounds / Boxes / Points; for heavy volumes, always-wireframe display keeps the viewport responsive while the final render still shows the volume), *Detail* (Coarse: one box or point per intermediate tree node; Fine: one per leaf node of 8x8 voxels), *Density* (viewport thickness only; render density comes from Volume Shading), *Interpolation* (Linear / Cubic / Closest), *Slice* (Axis Auto/X/Y/Z and Position).
- **Render** panel: *Space* (Object keeps density and detail the same regardless of object scale; World specifies step size and density in world space), and Cycles-only *Clipping* (values under it are treated as empty space), *Precision* (Full 32-bit / Half 16-bit / Variable), *Velocity Grid* (a vector grid, or a prefix of three scalar grids with x/.x/_x, y, z suffixes, used for motion blur), *Velocity Unit* (per frame or per second) and *Velocity Scale*.

## Modifiers

- **Mesh to Volume** (volume objects only): builds a new grid named `density` from a mesh and discards all previously existing grids on the volume object, so add it to an empty volume object. Options: *Object* (the mesh), *Density*, *Interior Band Width*, *Resolution Mode* (Voxel Amount: approximate voxel count along the mesh diagonal, so voxel size changes if the mesh dimensions change; Voxel Size: exact size). For final animation renders, specify the voxel size explicitly to avoid artifacts.
- **Volume Displace** (volume objects only): displaces grids by a 3D *Texture* using its RGB channels for X, Y and Z; grayscale textures stretch along one axis, so use a colour texture. Options: *Strength*, *Sample Radius* (smaller is faster but can cut off the volume outside), *Mid Level* (re-centres a texture that offsets the whole volume; keep the displaced volume near its original position for performance).
- **Volume to Mesh**: converts one *scalar* grid (such as density) of a source volume *Object* to a mesh. Options: *Grid Name*, *Resolution Mode* (Grid: follows the grid resolution; Voxel Amount; Voxel Size: fixed), *Threshold* (voxels with a larger value are inside; the iso value), *Adaptivity* (like decimating where resolution is not needed), *Smooth Shading*.
- To copy or move the generated volume or mesh separately from its source, use a collection instance.

## Gotchas

- Volume to Mesh only converts scalar grids; a vector grid such as velocity cannot be converted.
- A grid name that does not match the grid in the Grids panel is the first thing to check when a volume renders empty.
- Mesh to Volume replaces existing grids, so it is not a way to add a grid to an imported VDB.

## Verify

- The Grids panel shows the expected names and types.
- With *Sequence* set, the displayed frame changes as you scrub; *Mode* behaves as chosen beyond the end of the sequence.
- Volume to Mesh with a chosen Threshold gives a mesh whose boundary follows the visible volume.

## Checked

2026-10-28. Confirmed against the Blender manual pages Volume Properties, Mesh to Volume, Volume to Mesh and Volume Displace: sequence naming and the Frames/Start/Offset/Mode options, Grids panel, Viewport Display options, Render panel options (Space, Clipping, Precision, Velocity settings), and every modifier option listed above. Removed everything the pages do not support: file menu paths, Houdini/EmberGen/Mantaflow workflow notes, Cycles/EEVEE settings and defaults, Principled Volume shading recipes, Geometry Nodes volume nodes, export routes including pyopenvdb and USD, memory figures and performance advice, and version-specific claims. Some recipes in the earlier draft may be correct but were not verifiable from these pages.
Method: documentation only; no commands were run.
