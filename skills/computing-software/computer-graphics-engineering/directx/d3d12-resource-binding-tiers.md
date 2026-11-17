---
id: computing-software.computer-graphics-engineering.directx.d3d12-resource-binding-tiers
name: d3d12-resource-binding-tiers
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-binding, resource-binding-tier, d3d12-feature-tiers, bindless-limits]
level: advanced
status: docs-checked
description: "Understand D3D12 resource binding tiers 1-3: descriptor heap and table size limits, fully-populated table requirements, UAV counts, and designing for Tier 2+."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/hardware-support", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_resource_binding_tier", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/root-signature-limits", "https://microsoft.github.io/DirectX-Specs/d3d/HLSL_SM_6_6_DynamicResources.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource binding tiers

```cpp
D3D12_FEATURE_DATA_D3D12_OPTIONS o = {};
device->CheckFeatureSupport(D3D12_FEATURE_D3D12_OPTIONS, &o, sizeof(o));
switch (o.ResourceBindingTier) { case D3D12_RESOURCE_BINDING_TIER_1: ...; }
```

| Limit | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Feature levels | 11.0+ | 11.0+ | 11.1+ |
| Descriptors in a CBV/SRV/UAV heap used for rendering | 1,000,000 | 1,000,000 | 1,000,000+ |
| CBVs in all descriptor tables per shader stage | 14 | 14 | full heap |
| SRVs in all descriptor tables per shader stage | 128 | full heap | full heap |
| UAVs in all descriptor tables across all stages | 64 (FL 11.1+) or 8 (FL 11.0) | 64 | full heap |
| Samplers in all descriptor tables per shader stage | 16 | 2048 | 2048 |
| Unpopulated table entries | all entries covered by tables must be populated, in all heaps | CBV and UAV heap entries must be populated; SRV entries need not be | no such restriction |

Invariable limit: a shader-visible sampler heap holds at most 2048 samplers.

## Practical meaning
- SM 6.6 dynamic resources (`ResourceDescriptorHeap[]`, `SamplerDescriptorHeap[]`) require **both**
  `D3D12_RESOURCE_BINDING_TIER_3` and shader model 6.6.
- Bindless SRV-only designs fit Tier 2 (an unbounded SRV range in a descriptor table), with CBVs as root
  descriptors or a few-entry table and UAVs within 64.
- Feature level 12_2 requires Resource Binding Tier 3.

## Related caps to query together
- `ResourceHeapTier` (Tier 1: buffers, RT/DS textures and other textures live in separate heaps; Tier 2: any mix).
  Affects placed-resource and aliasing strategy.
- `TiledResourcesTier`, and the shader model via `D3D12_FEATURE_SHADER_MODEL`.

## Gotchas
- Where "must be populated" applies, even descriptors the shader never reads (for example behind a branch) have to
  hold valid descriptors: fill unused entries with null descriptors.
- The root signature size limit is 64 DWORDs (table = 1, root constant = 1, root descriptor = 2) and does not depend on
  the tier.

## Verify
- [ ] The startup log prints binding and heap tiers and shader model; the engine refuses to start with a clear message
  below its minimum tier.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Hardware tiers" and "Root signature limits"
(MicrosoftDocs/win32, last commit 2026-10-08), DirectX-Specs HLSL SM 6.6 dynamic resources and feature level 12_2
specs (2026-10-22), `ResourceHeapTier` docs. Confirmed: every figure in the table, populated-entry rules per tier,
2048 sampler heap limit, 64 DWORD costs, Tier 3 plus SM 6.6 requirement. Removed unconfirmed claims: GPU-generation to
tier mapping ("every DX12 GPU since 2016 is Tier 2 or 3"), and the OPTIONS19 sampler-heap remark.
Method: documentation only; no commands were run.
