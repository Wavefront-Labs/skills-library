---
id: computing-software.computer-graphics-engineering.directx.d3d12-static-samplers
name: d3d12-static-samplers
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, directx-12, d3d12-resource-binding, static-samplers, root-signature, d3d12-static-sampler-desc]
level: practitioner
status: docs-checked
description: "Declare Direct3D 12 static samplers in root signatures (C++ or HLSL): register mapping, border colours, comparison samplers, limits and when to use heap samplers."
sources: ["https://microsoft.github.io/DirectX-Specs/d3d/ResourceBinding.html", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_static_sampler_desc", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/specifying-root-signatures-in-hlsl", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/root-signature-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static samplers in Direct3D 12

**Goal:** bake fixed sampler state into the root signature so it needs no descriptor heap slot and no per-draw
binding. Static samplers do not count towards the 64 DWORD root signature limit.

## 1. C++
```cpp
D3D12_STATIC_SAMPLER_DESC s{};
s.Filter = D3D12_FILTER_ANISOTROPIC; s.MaxAnisotropy = 16;
s.AddressU = s.AddressV = s.AddressW = D3D12_TEXTURE_ADDRESS_MODE_WRAP;
s.MaxLOD = D3D12_FLOAT32_MAX; s.ShaderRegister = 0; s.RegisterSpace = 0;   // s0
s.ShaderVisibility = D3D12_SHADER_VISIBILITY_PIXEL;
D3D12_STATIC_SAMPLER_DESC shadow = s;
shadow.Filter = D3D12_FILTER_COMPARISON_MIN_MAG_LINEAR_MIP_POINT;
shadow.ComparisonFunc = D3D12_COMPARISON_FUNC_LESS_EQUAL;
shadow.AddressU = shadow.AddressV = shadow.AddressW = D3D12_TEXTURE_ADDRESS_MODE_BORDER;
shadow.BorderColor = D3D12_STATIC_BORDER_COLOR_OPAQUE_WHITE; shadow.ShaderRegister = 1;  // s1
// pass both in D3D12_ROOT_SIGNATURE_DESC1::pStaticSamplers
```
## 2. HLSL root signature
```hlsl
#define RS "RootFlags(ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT), CBV(b0), DescriptorTable(SRV(t0, numDescriptors=8)), " \
           "StaticSampler(s0, filter=FILTER_ANISOTROPIC, maxAnisotropy=16), " \
           "StaticSampler(s1, filter=FILTER_COMPARISON_MIN_MAG_LINEAR_MIP_POINT, comparisonFunc=COMPARISON_LESS_EQUAL, " \
           "addressU=TEXTURE_ADDRESS_BORDER, addressV=TEXTURE_ADDRESS_BORDER, borderColor=STATIC_BORDER_COLOR_OPAQUE_WHITE)"
[RootSignature(RS)] float4 PSMain(...) : SV_Target { ... }
```
Shader declares `SamplerState gAniso : register(s0); SamplerComparisonState gShadow : register(s1);`.

## 3. Rules
- Border colour is chosen from the `D3D12_STATIC_BORDER_COLOR` enum: transparent black, opaque black and opaque white
  for float samplers, plus opaque black and opaque white unsigned-integer colours (shader model 6.7 or higher, with
  `D3D12_SAMPLER_FLAG_UINT_BORDER_COLOR`). Arbitrary colours need heap samplers.
- The limit is 2032 **unique** static samplers across all root signatures live on a device at once (a sampler used by
  two root signatures counts once); this is separate from the 2048 samplers in a sampler descriptor heap. Arrays of
  static samplers are not permitted.
- A sampler register must not be declared both as a static sampler and in a sampler descriptor table (compilation
  fails).
- Use heap samplers when the choice is truly dynamic, when you need dynamic sampler indexing, or when the sampler type
  is not supported as a static sampler; a static sampler cannot change without rebuilding the root signature.

## Verify
- [ ] Debug layer clean; the capture shows the static samplers under the root signature.
- [ ] Shadow comparisons return filtered 0..1 values (comparison sampler in effect).

## Checked
Date: 2026-10-26. Documentation: DirectX-Specs ResourceBinding (static samplers section, 2026-10-22), Microsoft
Learn "Root signature limits" and "Specifying root signatures in HLSL" (MicrosoftDocs/win32, 2026-10-08),
`D3D12_STATIC_SAMPLER_DESC` (MicrosoftDocs/sdk-api). Confirmed: HLSL clause names (`filter`, `maxAnisotropy`,
`comparisonFunc`, `addressU`, `borderColor`), border colour enum, the 2032 limit and its device-wide scope, no-overlap
rule, 64 DWORD exemption. Corrected: the draft said 2032 static samplers per root signature, and listed only three
border colours. Removed the unverified TAA/DLSS mip-bias remark and the static-samplers page link (not in the
repository).
Method: documentation only; no commands were run.
