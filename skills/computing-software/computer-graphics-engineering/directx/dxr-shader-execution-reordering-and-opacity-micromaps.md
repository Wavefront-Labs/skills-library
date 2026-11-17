---
id: computing-software.computer-graphics-engineering.directx.dxr-shader-execution-reordering-and-opacity-micromaps
name: dxr-shader-execution-reordering-and-opacity-micromaps
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, shader-execution-reordering, opacity-micromaps, hitobject, dxr-1-2]
level: sme
status: docs-checked
description: "Use DXR 1.2 features: shader execution reordering with HitObject and MaybeReorderThread for coherence, and opacity micromaps to skip alpha-test any-hit work."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_ShaderModel6_9.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader execution reordering (SER) and opacity micromaps (OMM)

Both features target divergent shading after incoherent rays, and alpha-test any-hit invocations.
In D3D12 both are part of the DXR Tier 1.2 / Shader Model 6.9 work: SER is a required part of SM 6.9 for devices with
raytracing support, and OMM arrives with `D3D12_RAYTRACING_TIER_1_2`.

## SER: split trace from shade
```hlsl
// raygen
// SER types and intrinsics live in namespace dx in the spec (dx::HitObject, dx::MaybeReorderThread)
dx::HitObject hit = dx::HitObject::TraceRay(Scene, RAY_FLAG_NONE, 0xFF, 0, 1, 0, ray, payload);  // traversal only
uint coherenceHint = hit.IsHit() ? Materials[hit.GetInstanceID()].shaderId : MISS_ID;
dx::MaybeReorderThread(hit, coherenceHint, 4);    // hint plus number of low bits to use (overload with a HitObject)
dx::HitObject::Invoke(hit, payload);              // runs closest-hit/miss
```
- Similar hint values should indicate similar upcoming work; more significant bits matter more, and the
  implementation may ignore low bits. The resulting order may be approximate.
- The minimal allowed implementation of `MaybeReorderThread` is a no-op, and devices that cannot reorder ignore the call.
- Gains depend on workload and hardware; measure.

## OMM: hardware alpha testing
An opacity micromap subdivides each triangle into micro-triangles (subdivision level 0 to 12, so up to 4^12 micro-triangles)
tagged opaque or transparent (2-state format), or additionally unknown-opaque and unknown-transparent (4-state format).
Known states are classified as hit or miss without invoking any-hit; unknown states fall back to any-hit.
Workflow:
1. Bake OMMs offline from alpha textures with your own tool or a vendor SDK, per mesh + UVs.
2. Build an OMM array (`D3D12_RAYTRACING_OPACITY_MICROMAP_ARRAY`) and reference it from BLAS
   geometry descs (OMM index buffer per triangle, special indices for fully opaque/transparent).
3. Keep the any-hit shader for unknown regions.

## Requirements
- `D3D12_RAYTRACING_TIER_1_2` is required for OMM; check `RaytracingTier` through `CheckFeatureSupport`.
- HLSL pipelines enable OMM with `RAYTRACING_PIPELINE_FLAG_ALLOW_OPACITY_MICROMAPS` (Shader Model 6.9).
- Shader Model 6.9 for the `HitObject` APIs; a device that supports SM 6.9 with raytracing must support SER.

## Gotchas
- SER changes thread order: do not assume lane positions or wave membership persist across `MaybeReorderThread`.
- OMMs depend on UVs and alpha textures; rebake when assets change.

## Verify
- [ ] A GPU profiler shows improved shading-phase utilisation with SER; any-hit invocation count drops with OMM, image unchanged.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: HitObject::TraceRay, HitObject::Invoke, MaybeReorderThread overloads (HitObject; hint plus bit count; HitObject plus hint), namespace dx, SER required in SM 6.9 for raytracing devices and as part of Tier 1.2, MaybeReorderThread may be a no-op, OMM subdivision level range 0-12, 2-bit states including unknown-transparent/unknown-opaque, RAYTRACING_PIPELINE_FLAG_ALLOW_OPACITY_MICROMAPS and Tier 1.2. Removed: NVIDIA vendor extension names and speedup figures (2x, 2-10x), which no page checked states. Vulkan extension names are no longer mentioned.
Method: documentation only; no commands were run.
