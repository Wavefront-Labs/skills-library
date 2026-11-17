---
id: computing-software.computer-graphics-engineering.directx.d3d12-sampler-feedback-streaming
name: d3d12-sampler-feedback-streaming
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-advanced-features, sampler-feedback, texture-streaming, reserved-resources, minmip-map]
level: sme
status: docs-checked
description: "Use D3D12 sampler feedback (MinMip / MipRegionUsed) with reserved resources to stream only the texture tiles and mips shaders actually sample."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/SamplerFeedback.md", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/sampler-feedback"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sampler feedback streaming

**Goal:** record which mip regions shaders requested, then load only those tiles into a
reserved (tiled) texture.

## 1. Check support
```cpp
D3D12_FEATURE_DATA_D3D12_OPTIONS7 o7{};
dev->CheckFeatureSupport(D3D12_FEATURE_D3D12_OPTIONS7, &o7, sizeof(o7));
// o7.SamplerFeedbackTier >= D3D12_SAMPLER_FEEDBACK_TIER_0_9
```

## 2. Resources
- Paired texture: reserved resource (`CreateReservedResource`), tiles mapped via
  `UpdateTileMappings` from a heap pool.
- Feedback map: `CreateCommittedResource2` with format `DXGI_FORMAT_SAMPLER_FEEDBACK_MIN_MIP_OPAQUE`
  and a `SamplerFeedbackMipRegion` (a `D3D12_MIP_REGION`; the spec's sample uses 8x8x1 and notes a region is typically about one 64 KB tile or a small multiple).
- Bind with `CreateSamplerFeedbackUnorderedAccessView(paired, feedback, cpuHandle)`.

## 3. Shader
```hlsl
FeedbackTexture2D<SAMPLER_FEEDBACK_MIN_MIP> gFeedback : register(u0);
Texture2D gAlbedo : register(t0);
float4 c = gAlbedo.Sample(s, uv);
gFeedback.WriteSamplerFeedback(gAlbedo, s, uv);   // records the min mip that would be sampled
```
The spec suggests reducing the number of feedback writes by stochastic methods such as random discard, because each write costs.

## 4. Readback loop
1. `ResolveSubresourceRegion(..., D3D12_RESOLVE_MODE_DECODE_SAMPLER_FEEDBACK)` into an R8_UINT
   readback buffer.
2. CPU: for each region, compare requested mip with resident mip; queue loads and
   evictions.
3. Maintain a **residency map** (R8 min-mip texture) the shader uses as a clamp
   (the min-LOD clamp argument of `Sample`) so it never samples unmapped tiles.
4. Clear the feedback map each frame with `ClearUnorderedAccessViewUint` (the four clear values are ignored; a cleared map means no mips requested).

## Gotchas
- Tier 0.9 restricts the SRV passed to feedback-writing methods; Tier 1.0 supports all texture addressing modes and any SRV. Check `SamplerFeedbackTier`.
- Feedback writes cost per pixel; reduce them where you can.
- Without the residency clamp you get black or garbage texels from unmapped tiles.

## Verify
- [ ] Resident tile count tracks camera movement; VRAM for streamed textures stays bounded.
- [ ] No pop-in beyond one or two frames at normal camera speeds.

## Checked

Checked 2026-10-26 against the DirectX-Specs Sampler Feedback spec (repository current to 2026-10-22). Confirmed: D3D12_FEATURE_D3D12_OPTIONS7 SamplerFeedbackTier and TIER_0_9/TIER_1_0, CreateCommittedResource2 with SamplerFeedbackMipRegion, DXGI_FORMAT_SAMPLER_FEEDBACK_MIN_MIP_OPAQUE, CreateSamplerFeedbackUnorderedAccessView (ID3D12Device8), ResolveSubresourceRegion with D3D12_RESOLVE_MODE_DECODE_SAMPLER_FEEDBACK, FeedbackTexture2D<SAMPLER_FEEDBACK_MIN_MIP> and WriteSamplerFeedback, decoded map is R8_UINT, stochastic-writes advice. Corrected: the clear call ignores its values (the old 0xFF was wrong). The spec confirms the min-mip map is used to clamp to resident mip levels when sampling.
Method: documentation only; no commands were run.
