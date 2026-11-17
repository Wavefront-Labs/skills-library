---
id: computing-software.computer-graphics-engineering.rendering-techniques.rendering-openvdb-nanovdb-volumes
name: rendering-openvdb-nanovdb-volumes
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetrics, nanovdb, openvdb, sparse-volumes, volume-rendering, delta-tracking, vfx]
level: advanced
status: docs-checked
description: "Render OpenVDB/NanoVDB sparse volumes on the GPU: converting grids, NanoVDB accessors in shaders, delta-tracking/ray-marching with DDA through the tree, and lighting."
sources: ["https://github.com/AcademySoftwareFoundation/openvdb/blob/master/doc/nanovdb/FAQ.md", "https://github.com/AcademySoftwareFoundation/openvdb/blob/master/nanovdb/nanovdb/PNanoVDB.h", "https://github.com/AcademySoftwareFoundation/openvdb/blob/master/nanovdb/nanovdb/cmd/convert/nanovdb_convert.cc", "https://github.com/AcademySoftwareFoundation/openvdb/blob/master/nanovdb/nanovdb/tools/CreateNanoGrid.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rendering OpenVDB / NanoVDB volumes

## 1. Formats
- **OpenVDB**: sparse hierarchical grid (root, two internal levels, leaf nodes), used for smoke/fire/clouds in VFX; files are `.vdb`.
- **NanoVDB**: a slimmed-down version of the same tree configuration without std containers, with extra node metadata (min/max values and bounding boxes of active values) that accelerates ray tracing. It does not require CUDA: `PNanoVDB.h` gives C-style access from HLSL and GLSL.

## 2. Converting
```bash
nanovdb_convert [options] input.vdb output.nvdb       # options include -z (ZIP), -b (BLOSC), --fp16 (quantise floats)
```
Or in C++: `nanovdb::tools::createNanoGrid(srcGrid)` (CreateNanoGrid.h).
Upload the `.nvdb` buffer as a structured buffer of `uint` (the HLSL `pnanovdb_buf_t` is a `StructuredBuffer<uint>` or `RWStructuredBuffer<uint>`).

## 3. Sampling in shaders
`PNanoVDB.h` provides C-style accessors for HLSL/GLSL:
```hlsl
#define PNANOVDB_HLSL
#include "PNanoVDB.h"
pnanovdb_buf_t buf = /* StructuredBuffer<uint> */;
pnanovdb_grid_handle_t grid = { pnanovdb_address_null() };
pnanovdb_tree_handle_t tree = pnanovdb_grid_get_tree(buf, grid);
pnanovdb_root_handle_t root = pnanovdb_tree_get_root(buf, tree);
pnanovdb_readaccessor_t acc; pnanovdb_readaccessor_init(acc, root);
pnanovdb_coord_t ijk = pnanovdb_hdda_pos_to_ijk(indexSpacePos);
pnanovdb_address_t a = pnanovdb_readaccessor_get_value_address(PNANOVDB_GRID_TYPE_FLOAT, buf, acc, ijk);
float density = pnanovdb_read_float(buf, a);
```
A read accessor is an inout cache of visited nodes, intended for coherent lookups such as those along a ray. Do
trilinear interpolation yourself (8 lookups).

## 4. Traversal
- Transform the ray into index space with the grid's map (`pnanovdb_grid_world_to_indexf` / `pnanovdb_grid_world_to_index_dirf`).
- Use **HDDA** (hierarchical DDA, `pnanovdb_hdda_init`/`_update`/`_step`) to skip empty space: step through internal
  nodes/tiles that are inactive, only march inside active leaves.
- Rendering: ray marching with Beer-Lambert accumulation, or unbiased **delta tracking / ratio
  tracking** with a majorant per node (the node maximum value, available when the grid was built with statistics) for path tracing.

## 5. Lighting
Shadow rays toward lights through the volume (ratio tracking for transmittance), phase function HG,
multiple scattering via path tracing or approximations; fire uses an emission grid (temperature ->
blackbody colour).

## Gotchas
- Grids in world units with transforms: apply the grid's affine map, not just a scale.
- Huge volumes exceed GPU memory: crop, reduce resolution or stream frames of animated sequences.
- Density scale in VDBs from sims is arbitrary; expose a density multiplier.

## Verify
- [ ] Render matches Houdini/Blender preview of the same VDB at equal density and lighting.
- [ ] Empty-space skipping reduces step count (heatmap).

## Checked

2026-10-26: OpenVDB repository, read 2026-10-26: nanovdb/nanovdb/PNanoVDB.h, tools/CreateNanoGrid.h, cmd/convert/nanovdb_convert.cc and doc/nanovdb/FAQ.md. Confirmed: the PNANOVDB_HLSL/GLSL defines, StructuredBuffer<uint> buffer type, pnanovdb_address_null, grid_get_tree, tree_get_root, readaccessor_init, readaccessor_get_value_address, read_float, hdda_pos_to_ijk, hdda_init/update/step, world_to_indexf and world_to_index_dirf, nanovdb::tools::createNanoGrid, nanovdb_convert usage and options, and the FAQ statements that NanoVDB uses the same tree configuration, needs no CUDA and stores min/max and bounding boxes per node. Removed the 32/16/8 node sizes (not stated in the files read), the DCC export list, the read-only/pointer-free wording, the older openToNanoVDB name and the stencil helper mention.

Method: documentation only; no commands were run.
