---
id: computing-software.computer-graphics-engineering.directx.d3d12-variable-rate-shading
name: d3d12-variable-rate-shading
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, d3d12-advanced, directx-12-ultimate, variable-rate-shading, vrs, shading-rate-image, rssetshadingrate, sv-shadingrate, content-adaptive-shading]
level: advanced
status: docs-checked
description: "Reduce pixel shading cost with Direct3D 12 variable rate shading: tier checks, per-draw rates, screen-space shading-rate images built from luminance or motion, and combiners."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/VariableRateShading.md", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/vrs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 variable rate shading

**Goal:** shade 1 pixel per 2x2 (or 2x1, 4x4) block where nobody will notice — dark, blurred,
fast-moving or low-contrast areas — reducing pixel shader invocations.

## 1. Check the tier
```cpp
D3D12_FEATURE_DATA_D3D12_OPTIONS6 o6{};
device->CheckFeatureSupport(D3D12_FEATURE_D3D12_OPTIONS6, &o6, sizeof o6);
// Tier 1: per-draw rate only. Tier 2: + per-primitive (SV_ShadingRate) + screen-space image.
UINT tile = o6.ShadingRateImageTileSize;          // Tier 2: 16x16 or smaller tiles (the spec cites 8x8 or 16x16)
bool rates4x4 = o6.AdditionalShadingRatesSupported;   // gates the extra rates such as 2X4, 4X2, 4X4
```

## 2. Per-draw (tier 1)
```cpp
ComPtr<ID3D12GraphicsCommandList5> cl5; cmd.As(&cl5);
cl5->RSSetShadingRate(D3D12_SHADING_RATE_2X2, nullptr);   // e.g. for distant terrain, particles
... draws ...
cl5->RSSetShadingRate(D3D12_SHADING_RATE_1X1, nullptr);
```

## 3. Screen-space shading-rate image (tier 2)
An `R8_UINT` texture of size `ceil(w/tile) x ceil(h/tile)`, each texel a `D3D12_SHADING_RATE`
value, generated each frame by a compute pass:
- luminance/contrast of last frame's output (reprojected): low local contrast → coarser;
- motion vector magnitude: fast motion → coarser;
- foveation in VR; edges of the screen behind UI/vignette.
```cpp
// SRI must be in D3D12_RESOURCE_STATE_SHADING_RATE_SOURCE
D3D12_SHADING_RATE_COMBINER comb[2] = { D3D12_SHADING_RATE_COMBINER_PASSTHROUGH,   // draw vs primitive
                                        D3D12_SHADING_RATE_COMBINER_MAX };         // result vs image
cl5->RSSetShadingRate(D3D12_SHADING_RATE_1X1, comb);
cl5->RSSetShadingRateImage(sri.Get());
```
Combiners: `PASSTHROUGH`, `OVERRIDE`, `MIN`, `MAX`, `SUM`. `SUM` is only usable when the device cap for it is set
(`SUM` combiner support is a Tier 2 cap). `MAX` picks the coarser rate.

## 4. Per-primitive
A vertex/geometry/mesh shader can write `SV_ShadingRate` per provoking vertex (valid with one viewport, or with multiple
viewports when `SupportsPerVertexShadingRateWithMultipleViewports` is true) — e.g.
coarse shading for objects in motion blur or depth-of-field regions. Pixel shaders can also read `SV_ShadingRate` on Tier 2.

## What not to VRS
- UI, text, HUD (render after resetting to 1X1 or without the image).
- Alpha-tested foliage edges and high-frequency normal-mapped surfaces at close range.
- Passes whose output feeds temporal history: coarse shading can leave visible blockiness in the history; evaluate carefully.
- Compute-based passes: shading rate applies to pixel shader invocations, not compute dispatches.

## Gotchas
- Only pixel shader invocations are reduced; gains depend on how pixel-shader-bound the pass is.
- The screen-space image must be in `D3D12_RESOURCE_STATE_SHADING_RATE_SOURCE` at draw time (validated at Draw).

## Verify
- [ ] Debug overlay colours tiles by rate; coarse areas match expectations.
- [ ] A/B GPU timing of the affected passes shows the expected saving.
- [ ] Side-by-side image comparison shows no visible artefacts on text and edges.

## Checked

Checked 2026-10-26 against the DirectX-Specs Variable Rate Shading spec (repository current to 2026-10-22). Confirmed: ShadingRateImageTileSize and AdditionalShadingRatesSupported caps, Tier 1 per-draw and Tier 2 per-primitive plus image, DXGI_FORMAT_R8_UINT image sized ceil(rt/tile), SHADING_RATE_SOURCE state checked at Draw, ID3D12GraphicsCommandList5::RSSetShadingRate with combiners PASSTHROUGH/OVERRIDE/MIN/MAX/SUM, SUM cap, provoking-vertex rule and SV_ShadingRate. Corrected: tile sizes (8, 16 or 32 became 16x16 or smaller). Removed: 10-30% saving, FidelityFX/TAA implementation claims, SV_Position and depth/coverage behaviour claims, none of which the spec states.
Method: documentation only; no commands were run.
