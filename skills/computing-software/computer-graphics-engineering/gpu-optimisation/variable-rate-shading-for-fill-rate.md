---
id: computing-software.computer-graphics-engineering.gpu-optimisation.variable-rate-shading-for-fill-rate
name: variable-rate-shading-for-fill-rate
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, fragment-cost, vrs-performance, variable-rate-shading, shading-rate-image, fill-rate, d3d12, vulkan-fragment-shading-rate]
level: advanced
status: draft
description: "Cut pixel shading cost with variable rate shading: per-draw, per-primitive and image-based rates, building shading-rate images, and quality pitfalls."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/vrs", "https://docs.vulkan.org/spec/latest/chapters/primsrast.html#primsrast-fragment-shading-rate", "https://gpuopen.com/fidelityfx-variable-shading/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VRS for fill-rate

## 1. What VRS does
Runs the pixel shader once per coarse block (1x2, 2x1, 2x2, up to 4x4) and broadcasts the result to
covered pixels. Depth/coverage stay at full resolution, so edges remain sharp. Saves pixel shading
cost (not bandwidth for depth/ROP).

## 2. Ways to set the rate
| Tier/feature | D3D12 | Vulkan (`VK_KHR_fragment_shading_rate`) |
|---|---|---|
| Per draw | `RSSetShadingRate(D3D12_SHADING_RATE_2X2, combiners)` (Tier 1) | `vkCmdSetFragmentShadingRateKHR` |
| Per primitive | `SV_ShadingRate` output from VS/GS (Tier 2) | `PrimitiveShadingRateKHR` |
| Screen-space image | `RSSetShadingRateImage(tex)` with tiles of 8/16 px (Tier 2) | attachment shading rate image |
Combiners decide how the three sources merge (max, min, override, passthrough).

## 3. Generating a shading-rate image
- From last frame's luminance contrast per tile: low-contrast tiles (sky, dark areas, flat walls)
  get coarser rates. AMD FidelityFX Variable Shading computes this in compute from the previous
  frame's colour and motion vectors.
- From motion: fast-moving regions tolerate coarse shading (motion blur hides it).
- Foveation for VR: coarse in the periphery (lens-distorted areas), fine in the centre or at the
  tracked gaze.

## 4. Where it pays
Expensive pixel shaders (forward lighting, complex materials) at high resolutions. Gains 10-30%
on the affected passes typically. Little gain for cheap shaders or bandwidth-bound passes.

## 5. Deferred and compute
VRS applies to pixel shaders; deferred lighting in compute doesn't benefit. Alternatives: software
VRS in compute (shade one pixel per 2x2 in lighting compute, as in Call of Duty/Gears approaches) or
apply VRS to the G-buffer pass only.

## Gotchas
- Text, UI and high-frequency textures look blocky at coarse rates; exclude UI and use per-draw 1x1
  for detailed materials.
- Coarse shading with derivatives changes mip selection (derivatives across a coarse block).
- Check `D3D12_FEATURE_DATA_D3D12_OPTIONS6` tier and tile size; Vulkan rate image texel size limits.

## Verify
- [ ] Shading-rate debug overlay matches content (coarse in flat/dark areas).
- [ ] GPU time reduction measured on the affected pass; no visible artefacts in A/B.
