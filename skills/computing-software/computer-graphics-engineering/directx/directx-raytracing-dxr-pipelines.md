---
id: computing-software.computer-graphics-engineering.directx.directx-raytracing-dxr-pipelines
name: directx-raytracing-dxr-pipelines
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [directx, dxr, directx-raytracing, d3d12, blas, tlas, acceleration-structure, shader-table, hit-group, raygen, closest-hit, miss-shader, inline-raytracing, hybrid-rendering, denoising]
level: advanced
status: docs-checked
description: "Build a DXR raytracing pipeline: BLAS/TLAS acceleration structures, shader tables, hit groups, and the hybrid raster+RT patterns real engines ship (reflections, shadows, GI)."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-raytracing", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-raytracing-hlsl-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DirectX Raytracing (DXR) pipelines

**Goal:** set up a DXR pipeline that actually dispatches and hits rays correctly —
the acceleration-structure/shader-table wiring is where most first attempts break,
not the shading math. Builds on
`computer-graphics-engineering.directx.direct3d12-root-signatures-and-command-lists`.

## Acceleration structures: BLAS → TLAS
- **BLAS** (bottom-level): one per mesh/geometry, built from vertex/index buffers.
  Build with `D3D12_RAYTRACING_ACCELERATION_STRUCTURE_BUILD_FLAG_PREFER_FAST_TRACE`
  for static geometry, `..._ALLOW_UPDATE` for skinned/deforming meshes you'll refit
  rather than rebuild.
- **TLAS** (top-level): one per scene, references BLAS instances with their own
  transform + instance mask + instance ID. Rebuild/refit every frame instances move.
- **Refit vs rebuild**: an update (build flag `..._PERFORM_UPDATE`, which needs the original build to have
  used `..._ALLOW_UPDATE`; passing the same address as source and destination updates in place) is
  cheaper but only valid for the same topology (primitive count and connectivity unchanged,
  just moved) — rebuild when geometry itself changes (LOD swap, destruction).
- Acceleration structure memory lives in resources created with `D3D12_RESOURCE_FLAG_ALLOW_UNORDERED_ACCESS`
  that stay permanently in `D3D12_RESOURCE_STATE_RAYTRACING_ACCELERATION_STRUCTURE`; synchronise
  reads and writes with UAV barriers, not state transitions. A missing barrier between build and use is a
  common bug.

## Shader tables and hit groups
A DXR pipeline has no single "the shader" — it's a table of shader records indexed
by ray/geometry:
- **Raygen shader**: one entry point, launched per pixel/sample via
  `DispatchRays`. Generates primary rays and calls `TraceRay`.
- **Hit groups**: closest-hit (+ optional any-hit, intersection-for-procedural-
  geometry) bound **per geometry instance** via the shader table's stride/offset.
  Mismatched shader table layout vs TLAS instance order is the classic "random
  wrong material per object" bug.
- **Miss shader**: runs when a ray hits nothing (sky/environment lookup).
- Each shader record starts with a `D3D12_SHADER_IDENTIFIER_SIZE_IN_BYTES` (32) identifier, record
  strides must be multiples of 32 bytes (`D3D12_RAYTRACING_SHADER_RECORD_BYTE_ALIGNMENT`) and table
  start addresses 64-byte aligned; local root signature data is appended if hit groups use per-instance resources
  (material index, vertex buffer SRV) via a **local root signature** distinct from
  the pipeline's global one.

## Dispatch and recursion
- `TraceRay` recursion depth is bounded by `MaxTraceRecursionDepth` in the pipeline config (0 to 31;
  the ray generation shader is depth 0). A `TraceRay` at the maximum depth puts the device into the removed
  state. The spec advises picking the lowest limit you need.
- Ray flags (`RAY_FLAG_CULL_BACK_FACING_TRIANGLES`, `RAY_FLAG_FORCE_OPAQUE` to treat geometry as opaque
  and skip any-hit when you don't need it) reduce work.

## Hybrid rendering (what ships, not full path tracing)
Real-time DXR almost never means pure ray-traced primary visibility — it means:
- **Ray-traced shadows**: replace shadow maps with a shadow ray per light sample;
  removes peter-panning/acne entirely but costs per-light-per-pixel rays.
- **Ray-traced reflections**: raster G-buffer for primary visibility, trace
  reflection rays from there (cheaper than full RT, matches rasterised geometry
  exactly at the primary hit).
- **RT global illumination**: ReSTIR, DDGI (irradiance probes updated via RT) —
  the probe/SH approach avoids per-pixel path tracing cost.
- Low sample counts per pixel are noisy by construction and normally need a **denoiser**
  (for example NVIDIA NRD, which provides REBLUR, RELAX and SIGMA) or temporal accumulation.

## Gotchas
- DXR requires a capability check (`CheckFeatureSupport` with `D3D12_FEATURE_D3D12_OPTIONS5`, member
  `RaytracingTier`) — not all D3D12 hardware supports it; fall back to raster.
- PIX/Nsight Graphics have dedicated DXR debug views (acceleration structure
  viewer, ray inspector) — printf-style debugging doesn't work inside hit shaders.

## Verify
- [ ] UAV barrier present between AS build and first use in the same command list.
- [ ] Shader table row order matches TLAS instance order one-to-one (log and diff
      if materials look shuffled).
- [ ] Refit used only when topology is provably unchanged; rebuild otherwise.
- [ ] A denoiser or temporal accumulation stage sits between ray output and final
      composite for noisy low-sample RT effects.
- [ ] RaytracingTier checked before pipeline creation; non-DXR fallback path exists.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: acceleration structures stay in the RAYTRACING_ACCELERATION_STRUCTURE state with UAV-barrier synchronisation and the UAV resource flag, PERFORM_UPDATE and ALLOW_UPDATE semantics and in-place update, shader identifier size 32 and record/table alignments (32 and 64), recursion depth range 0-31 and device removal at the limit, D3D12_OPTIONS5 RaytracingTier. NRD provides REBLUR, RELAX and SIGMA (NVIDIA-RTX/NRD README, 2026-10). Corrected: the nonexistent PERFORM_UPDATE_IN_PLACE flag, the UNORDERED_ACCESS state claim, the field name MaxRecursionDepth (the field is MaxTraceRecursionDepth), and the shader-table alignment wording. Removed: 'most engines cap at 1-2', DLSS-RR and SVGF mentions.
Method: documentation only; no commands were run.
