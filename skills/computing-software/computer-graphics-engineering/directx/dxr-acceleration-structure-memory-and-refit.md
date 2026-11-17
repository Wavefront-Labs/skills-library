---
id: computing-software.computer-graphics-engineering.directx.dxr-acceleration-structure-memory-and-refit
name: dxr-acceleration-structure-memory-and-refit
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, as-refit, scratch-buffer, blas-build-flags]
level: sme
status: docs-checked
description: "Budget DXR acceleration structure memory: prebuild sizes, scratch reuse, build flags (FAST_TRACE vs FAST_BUILD, ALLOW_UPDATE), refit vs rebuild policy and batching."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Acceleration structure memory and refit policy

## Sizes
```cpp
D3D12_BUILD_RAYTRACING_ACCELERATION_STRUCTURE_INPUTS in = {};
in.Type = D3D12_RAYTRACING_ACCELERATION_STRUCTURE_TYPE_BOTTOM_LEVEL;
in.Flags = D3D12_RAYTRACING_ACCELERATION_STRUCTURE_BUILD_FLAG_PREFER_FAST_TRACE |
           D3D12_RAYTRACING_ACCELERATION_STRUCTURE_BUILD_FLAG_ALLOW_COMPACTION;
in.NumDescs = 1; in.DescsLayout = D3D12_ELEMENTS_LAYOUT_ARRAY; in.pGeometryDescs = &geom;
D3D12_RAYTRACING_ACCELERATION_STRUCTURE_PREBUILD_INFO pre;
device5->GetRaytracingAccelerationStructurePrebuildInfo(&in, &pre);
// pre.ResultDataMaxSizeInBytes, pre.ScratchDataSizeInBytes, pre.UpdateScratchDataSizeInBytes
```
AS buffers: `D3D12_RESOURCE_STATE_RAYTRACING_ACCELERATION_STRUCTURE` for their whole life, created with the
allow-unordered-access resource flag, 256-byte aligned addresses
(`D3D12_RAYTRACING_ACCELERATION_STRUCTURE_BYTE_ALIGNMENT`). Many BLASes can share one buffer.

## Build flags by object type
| Object | Flags | Per frame |
|---|---|---|
| Static meshes | `PREFER_FAST_TRACE | ALLOW_COMPACTION` | build once, compact |
| Skinned characters | `PREFER_FAST_BUILD | ALLOW_UPDATE` (or FAST_TRACE if few) | update (refit) per frame, rebuild when quality drops |
| Destruction / large deformation | `PREFER_FAST_BUILD` | rebuild |
| TLAS | `PREFER_FAST_TRACE` (+`ALLOW_UPDATE` if mostly static transforms) | rebuild per frame usually cheap |

## Refit vs rebuild
An update (`PERFORM_UPDATE`) keeps topology and re-fits to new vertex positions. Builds with `ALLOW_UPDATE` can
use more memory and build time and give lower trace performance, but updates should be faster than a full build.
The spec documents these costs; choosing a rebuild interval or a deformation threshold is an engine
tuning decision to measure.

## Compaction
After building with `ALLOW_COMPACTION`, read the compacted size (postbuild info,
`COMPACTED_SIZE`) once the build has completed on the GPU, allocate, `CopyRaytracingAccelerationStructure(..., COMPACT)`,
then free the original.

## Scratch memory
Scratch is only needed during the build. Builds that share scratch memory must be serialised with UAV
barriers; give concurrent builds separate scratch regions.

## Gotchas
- `UpdateScratchDataSizeInBytes` is the scratch requirement for every update; it is 0 when `ALLOW_UPDATE` was not set.
- UAV barrier on the BLAS buffer between BLAS builds and the TLAS build that references them.
- Track acceleration structure memory in your VRAM budget.

## Verify
- [ ] Trace cost stays stable over time for updated characters (check in a GPU profiler); AS memory is reported in the budget overlay.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: prebuild info fields (ResultDataMaxSizeInBytes, ScratchDataSizeInBytes, UpdateScratchDataSizeInBytes and its zero-when-no-ALLOW_UPDATE rule), 256-byte alignment, permanent AS resource state and UAV barrier synchronisation, ALLOW_UPDATE cost wording, COMPACTED_SIZE postbuild info and the compaction copy mode. Removed: 30-50% compaction saving, 8-30 frame rebuild interval, >1 GB figure and 'default heap' (not stated in the spec text checked).
Method: documentation only; no commands were run.
