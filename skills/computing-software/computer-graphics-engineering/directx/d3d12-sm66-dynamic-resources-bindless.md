---
id: computing-software.computer-graphics-engineering.directx.d3d12-sm66-dynamic-resources-bindless
name: d3d12-sm66-dynamic-resources-bindless
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, directx-12, d3d12-resource-binding, resourcedescriptorheap, sm66-bindless, bindless, shader-model-6-6]
level: advanced
status: docs-checked
description: "Go bindless in Direct3D 12 with Shader Model 6.6 ResourceDescriptorHeap and SamplerDescriptorHeap indexing: root signature flags, NonUniformResourceIndex."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_SM_6_6_DynamicResources.md", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/hardware-support"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SM 6.6 dynamic resources (ResourceDescriptorHeap)

**Goal:** index any SRV/UAV/CBV/sampler in the bound heaps directly from HLSL, with no
descriptor tables in the root signature.

## 1. Requirements
- `D3D12_FEATURE_SHADER_MODEL` >= 6.6 and resource binding tier 3
  (`D3D12_FEATURE_D3D12_OPTIONS::ResourceBindingTier`).
- A shader model 6.6 target in DXC (for example `-T ps_6_6`).
- Root signature flags:
  `D3D12_ROOT_SIGNATURE_FLAG_CBV_SRV_UAV_HEAP_DIRECTLY_INDEXED |
   D3D12_ROOT_SIGNATURE_FLAG_SAMPLER_HEAP_DIRECTLY_INDEXED`.
- `SetDescriptorHeaps` with the shader-visible CBV/SRV/UAV and sampler heaps before draws.

## 2. Shader
```hlsl
struct DrawConstants { uint albedoIdx; uint samplerIdx; uint vbIdx; };
ConstantBuffer<DrawConstants> dc : register(b0);         // root constants
float4 PSMain(VSOut i) : SV_Target {
    Texture2D<float4> tex = ResourceDescriptorHeap[dc.albedoIdx];
    SamplerState      smp = SamplerDescriptorHeap[dc.samplerIdx];
    return tex.Sample(smp, i.uv);
}
// per-pixel varying index (e.g. from a material ID buffer):
Texture2D t = ResourceDescriptorHeap[NonUniformResourceIndex(matIdx)];
```
Index = descriptor slot in the heap. `ResourceDescriptorHeap[i]` must be assigned to a CBV/SRV/UAV variable and
`SamplerDescriptorHeap[i]` to a sampler variable; the indexing result cannot be stored or used any other way.
Buffers: `StructuredBuffer<Vertex> vb = ResourceDescriptorHeap[dc.vbIdx];` enables vertex
pulling without input layouts.

## 3. Heap management
One big shader-visible heap (the hardware-support page lists 1,000,000 descriptors for all tiers, 1,000,000+ on Tier 3), a free-list
allocator for persistent resources, and a ring region for transient per-frame descriptors. The page lists 2048 samplers for
Tier 2 and 3 tables. Never overwrite a descriptor the GPU may still read; defer frees by frames in flight.

## Gotchas
- Indexing is assumed uniform; for a non-uniform index you must use `NonUniformResourceIndex`, or the result may be undefined.
- Descriptors and data looked up through the heaps are treated as volatile (equivalent to `DESCRIPTORS_VOLATILE | DATA_VOLATILE`).
- The new root signature flags are not allowed on local root signatures.
- Keep index spaces typed in C++ so a descriptor is only read as its own type; use GPU-based validation to catch bad indices.

## Verify
- [ ] Root signature has no tables; draws use only root constants and heap indices.
- [ ] GPU-based validation clean; mixed materials within one draw render correctly on more than one GPU.

## Checked

Checked 2026-10-26 against the DirectX-Specs HLSL Dynamic Resources spec (v1.00, 2021-04-20 with a 2024-07-31 sample fix) and the Learn hardware-support page. Confirmed: ResourceDescriptorHeap/SamplerDescriptorHeap semantics, NonUniformResourceIndex rule, root signature flags CBV_SRV_UAV_HEAP_DIRECTLY_INDEXED (0x400) and SAMPLER_HEAP_DIRECTLY_INDEXED (0x800), not allowed on local root signatures, volatility rule, support requires D3D12_RESOURCE_BINDING_TIER_3 and shader model 6.6, descriptor counts. Removed: vendor-specific corruption claims, the CPUHandle arithmetic comment, and the Agility SDK/older Windows 10 remark. The statement that the root signature must also call SetDescriptorHeaps follows from the spec's SetDescriptorHeaps section but the call order was not verified here.
Method: documentation only; no commands were run.
