---
id: computing-software.computer-graphics-engineering.directx.ray-tracing-denoising-nrd
name: ray-tracing-denoising-nrd
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, rt-denoising, nrd, reblur, relax, sigma]
level: sme
status: draft
description: "Denoise 1-spp ray-traced shadows, reflections and GI with NVIDIA NRD (ReBLUR/ReLAX/SIGMA): inputs, packing, hit distance and history validation."
sources: ["https://github.com/NVIDIA-RTX/NRD", "https://developer.nvidia.com/rtx/ray-tracing/rt-denoisers", "https://research.nvidia.com/publication/2017-07_spatiotemporal-variance-guided-filtering-real-time-reconstruction-path-traced"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Denoising ray-traced effects with NRD

**Goal:** turn noisy 0.5-1 spp RT signals into stable images using spatio-temporal denoisers.

## 1. Pick the denoiser per signal
| Signal | NRD denoiser |
|---|---|
| Diffuse/specular GI, reflections | REBLUR (fast, hit-distance based) or RELAX (better with RTXDI many-light input) |
| Shadows (sun, local lights) | SIGMA |
| AO / specular occlusion | REBLUR occlusion variants |

## 2. Required guides (G-buffer)
- Linear view depth, motion vectors (consistent with jitter), packed normal plus roughness
  (`NRD_FrontEnd_PackNormalAndRoughness`), optional material ID.
- Radiance and **normalised hit distance** (`REBLUR_FrontEnd_PackRadianceAndNormHitDist`), not raw
  distance: hit distance drives the specular blur radius.
- Current and previous camera matrices and `frameIndex`; set
  `CommonSettings::accumulationMode = RESTART` on camera cuts.

## 3. Integration (NRD integration layer over NRI)
1. Create an instance with the denoisers you need; allocate the pool textures it requests.
2. Per frame: fill `CommonSettings` and per-denoiser settings, then call `Denoise`.
3. Output stays packed; unpack (`REBLUR_BackEnd_UnpackRadianceAndNormHitDist`) before
   compositing. Demodulate albedo before denoising and re-apply it after.

## 4. Tuning
- Raise `maxAccumulatedFrameNum` for stability, lower it for response to lighting changes.
- Turn on NRD validation (`enableValidation`) to view history length and disocclusions.
- Feed checkerboard or half-res traces with the matching `checkerboardMode`.

## Gotchas
- Motion vectors off by half a pixel or missing on skinned meshes produce ghosting trails.
- Denoising pre-modulated radiance blurs texture detail.
- Mirror-like specular (roughness below about 0.05) may look better with a separate mirror path.

## Verify
- [ ] Validation view shows full history on static views and resets on disocclusion.
- [ ] Moving-camera captures free of smearing on thin geometry.
