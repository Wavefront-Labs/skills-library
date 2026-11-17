---
id: computing-software.computer-graphics-engineering.rendering-techniques.mip-streaming-and-mip-bias
name: mip-streaming-and-mip-bias
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, mip-streaming, mip-bias, texture-streaming, sampler-feedback, min-lod, memory-budget]
level: advanced
status: docs-checked
description: "Stream texture mips on demand with D3D12 sampler feedback: tiled textures, MinMip maps, feedback maps and mip regions; mip chain memory arithmetic and mip bias cautions."
sources: ["https://microsoft.github.io/DirectX-Specs/d3d/SamplerFeedback.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mip streaming and mip bias

## 1. Mip streaming with D3D12 sampler feedback
Streaming loads texture data on demand instead of keeping the most detailed mips of every texture in
memory. The D3D12 Sampler Feedback spec describes this workflow ("SFS"):
1. Use a tiled (reserved) texture resource for anything that is streamed. The spec recommends
   `D3D12_TILED_RESOURCES_TIER_2`: tier 2 covers control of tile residency and clamping to resident
   mips when sampling.
2. Create two small companion textures per tiled texture:
   - **MinMip map**: per-region mip clamp values; what is actually loaded. Each texel covers one *mip
     region* of the paired texture and holds the most detailed mip that is fully resident there. This is
     recommended application practice, not a runtime feature. The shader samples it and uses the value as
     a per-pixel mip clamp on the tiled texture.
   - **Feedback map**: per-region desired mip level; what needs to be loaded. Its format is opaque
     (`DXGI_FORMAT_SAMPLER_FEEDBACK_MIN_MIP_OPAQUE` or `..._MIP_REGION_USED_OPAQUE`) and is decoded to read.
3. Shaders write feedback with HLSL `FeedbackTexture2D<SAMPLER_FEEDBACK_MIN_MIP>` (or
   `SAMPLER_FEEDBACK_MIP_REGION_USED`) and `WriteSamplerFeedback(texture, sampler, uv)`.
4. Stream individual tiles rather than whole mips, driven by the feedback map. When tiles become
   resident or non-resident the app must update the MinMip map; loading a mip 0 tile touches one MinMip
   texel in the typical one-texel-per-mip-0-tile layout, a mip 1 tile four, a mip 2 tile sixteen.
5. The MinMip map may be filtered to fade one mip into another smoothly (spec remark), which helps hide
   pops when new mips arrive.

Details worth knowing:
- Mip region dimensions are powers of two, at least 4, and at most half the paired texture's most
  detailed dimension; a typical streaming region is a 64 KB tile.
- A MinMip feedback map records, per region, the most detailed mip requested ("ideal") with no clamping.
- Feedback is not supported on multisampled resources. Support is queried through `CheckFeatureSupport`
  and is not part of any feature level; `TIER_0_9` limits address modes (WRAP, CLAMP) and view
  parameters, `TIER_1_0` removes those limits.
- Zero-weight reads in filtering may or may not write feedback, depending on hardware. Anisotropic
  filtering on a texture with a single mip can give conservative false positives.
- Without sampler feedback, tiled resources still allow progressive mip loading, and the status from a
  sample can be passed to `CheckAccessFullyMapped` to detect non-resident tiles.

Other APIs and engines (Vulkan min-LOD extensions, Unity and Unreal streaming settings) are not covered
here: read the engine's current texture streaming page for its budget and heuristics.

## 2. Memory accounting (arithmetic)
A full mip chain is about 4/3 the size of mip 0, and dropping the top mip removes three quarters of
the texels. Work out bytes from the texture's actual format and dimensions, budget per platform and log
the resident set.

## 3. Mip bias
Check the vendor documentation of the upscaler you integrate for the bias it asks for, apply it to
material samplers only (not post-processing, UI or lookup tables), and re-check when dynamic resolution
changes the render scale. This skill does not give bias formulas because none were confirmed.

## Gotchas
- Feedback maps cannot themselves be tiled resources.

## Checked
2026-11-08. Confirmed against the Microsoft DirectX-Specs Sampler Feedback page: tiled resources and tier 2 recommendation, MinMip map and feedback map roles and formats, HLSL types and `WriteSamplerFeedback`, MinMip update counts, mip region constraints, feature tiers and restrictions, single-sample restriction, zero-weight and anisotropic caveats. Removed: Unity and Unreal streaming claims (pages were a stub index and blocked), Vulkan extension names, `MinLODClamp` usage details, the BC7 size example, DLSS bias guidance and the `log2` bias formula (none stated in the fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Texture memory stays under budget in worst-case views; no blurry textures after settle time.
- [ ] Mip visualisation mode shows expected mips; upscaler path shows bias applied.
