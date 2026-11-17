---
id: creative-arts.animation.blender.smoke-vdb-export
name: smoke-vdb-export
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, smoke-vdb-export, vdb-cache, openvdb, volume-objects]
level: practitioner
status: docs-checked
description: "Export Mantaflow smoke as OpenVDB for other DCCs or reuse: cache format, compression, precision, and importing VDB sequences as Volume objects."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html
  - https://docs.blender.org/manual/en/latest/modeling/volumes/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# smoke-vdb-export

## Bake to VDB

Domain > Cache > Volumetric Data: **Format = OpenVDB** stores all simulation objects (grids and particles) in a single `.vdb` file per frame, inside the per-type directory under the Cache Directory (noise has its own directory).

- **Compression**: Zip (effective but slower than Blosc), Blosc (multi-threaded, similar size and quality to Zip) or None.
- **Precision**: Full (32-bit), Half (16-bit) or Mini (8-bit where possible, otherwise 16-bit).
- Uni Cache is the alternative format: one `.uni` file per simulation object.

## Reuse in Blender

Volume objects represent OpenVDB files in Blender, including files generated from the fluid cache. Create one from the Add menu or by dragging a `.vdb` file into the 3D Viewport; a frame sequence of OpenVDB files can be imported for animation. By default the Principled Volume shader renders volume objects and uses the grids named `density`, `color` and `temperature`; if those are missing, pick another grid name in the shader nodes.

## Other DCCs

OpenVDB is a library and file format for interoperability: files can be exchanged with other software such as Houdini. Check grid names and orientation in the target application.

## Gotchas

- Noise grids are in their own directory; for upres smoke use the noise cache as well.
- OpenVDB sparse volumes are still rendered as dense volumes in Blender, which costs performance and memory.
- Level-set grids can be read but not rendered as surfaces, and importing OpenVDB points is not supported.

## Verify

Import the VDB sequence into an empty scene: the smoke plays back and renders like the domain.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/cache and modeling/volumes/introduction; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: OpenVDB vs Uni Cache layout, Compression and Precision options, volume object creation, sequence import, default grid names, and the rendering limitations.

Method: documentation only; no commands were run.
