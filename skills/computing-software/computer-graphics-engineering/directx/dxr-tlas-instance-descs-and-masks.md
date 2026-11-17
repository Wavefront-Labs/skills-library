---
id: computing-software.computer-graphics-engineering.directx.dxr-tlas-instance-descs-and-masks
name: dxr-tlas-instance-descs-and-masks
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, tlas-instance, instance-mask, instance-contribution-to-hit-group]
level: advanced
status: docs-checked
description: "Fill DXR TLAS instance descs: 3x4 transforms, InstanceID vs index, 8-bit masks for ray filtering, hit-group contribution offsets and instance flags."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLAS instance descs and masks

```cpp
D3D12_RAYTRACING_INSTANCE_DESC d = {};
memcpy(d.Transform, &objectToWorld3x4, sizeof(float) * 12);  // row-major 3x4: [R|t] rows
d.InstanceID = materialOrObjectIndex;          // 24 bits, user value -> InstanceID() in shaders
d.InstanceMask = 0x01;                          // 8 bits, ANDed with ray's mask
d.InstanceContributionToHitGroupIndex = sbtOffset;   // 24 bits
d.Flags = D3D12_RAYTRACING_INSTANCE_FLAG_TRIANGLE_CULL_DISABLE;
d.AccelerationStructure = blas->GetGPUVirtualAddress();
```
Upload the array into a GPU buffer (upload heap or copied to default), then build the TLAS with
`InstanceDescs = buffer GPUVA`, `NumDescs`.

## Transform
3 rows x 4 columns, row-major, object-to-world. GLM (column-major 4x4): transpose the upper 3x4.
A wrong transpose puts all instances at the origin or skews them: debug by visualising instance
bounding boxes.

## InstanceID vs InstanceIndex
- `InstanceIndex()` in HLSL = position in the instance array (automatic).
- `InstanceID()` = your 24-bit value: index into a per-object/material table so multiple
  instances can share data or be reordered freely.

## Masks: ray filtering without shader cost
Assign bits by category: 0x01 opaque world, 0x02 foliage, 0x04 characters, 0x08 "no shadow casting"
debris, 0x10 first-person weapon. Rays pass a mask:
```hlsl
TraceRay(scene, RAY_FLAG_ACCEPT_FIRST_HIT_AND_END_SEARCH, 0x01 | 0x04 /*shadow casters*/, ...);
```
An instance is skipped if `(instanceMask & rayMask) == 0`; both masks are 8 bits.

## Hit group index
Hit group record index = `RayContributionToHitGroupIndex + MultiplierForGeometryContributionToHitGroupIndex *
GeometryContributionToHitGroupIndex + InstanceContributionToHitGroupIndex`, where the geometry term is the
system-generated index of the geometry in the BLAS (0, 1, 2, ...). `TraceRay` supplies the ray contribution and the
multiplier; the instance desc supplies the instance contribution. Setting the multiplier to 0 is possible on Tier 1.1
when shaders call `GeometryIndex()`.

## Instance flags
`TRIANGLE_CULL_DISABLE` (disables front/back culling for the instance), `TRIANGLE_FRONT_COUNTERCLOCKWISE` (reverses
front/back facing), `FORCE_OPAQUE` and `FORCE_NON_OPAQUE` (mutually exclusive; act as if the geometry opaque flag
were set or cleared for every geometry in the BLAS, and can be overridden by `RAY_FLAG_FORCE_NON_OPAQUE` and
`RAY_FLAG_FORCE_OPAQUE` respectively).

## Gotchas
- InstanceID and InstanceContributionToHitGroupIndex are 24-bit fields.
- Rebuild/refit TLAS every frame for dynamic scenes; keep instance buffers per frame in flight.
- To hide an instance, use mask 0 (an instance is skipped when `InstanceMask & rayMask` is 0); the spec does not promise zero cost for degenerate transforms.

## Verify
- [ ] Debug view coloured by InstanceID shows expected objects; shadow rays ignore mask-excluded instances.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: D3D12_RAYTRACING_INSTANCE_DESC fields (3x4 row-major Transform, 24-bit InstanceID and InstanceContributionToHitGroupIndex, 8-bit InstanceMask), the hit group index formula including the system-generated geometry index, instance flags and their override relationship with ray flags, instance desc alignment of 16 bytes, mask AND rule. Corrected: the formula's geometry term (it is the system-generated geometry contribution, not an app value) and the FORCE_OPAQUE description. Removed: the 'essentially free' claim and zero-scale cost claim.
Method: documentation only; no commands were run.
