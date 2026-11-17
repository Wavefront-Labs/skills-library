---
id: computing-software.computer-graphics-engineering.rendering-techniques.irradiance-probes-and-ddgi
name: irradiance-probes-and-ddgi
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, ddgi, irradiance-probes, probe-volumes, octahedral-probes, light-leaking]
level: sme
status: draft
description: "Implement probe-based diffuse GI: irradiance probe grids, DDGI with ray-traced updates, octahedral irradiance and depth maps, and leak prevention."
sources: ["https://www.jcgt.org/published/0008/02/01/", "https://github.com/NVIDIAGameWorks/RTXGI-DDGI", "https://developer.nvidia.com/rtx/ray-tracing/rtxgi"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Irradiance probes and DDGI

## 1. Probe grid
Regular 3D grid of probes covering the scene (e.g. 1-2 m spacing indoors), each storing
irradiance: SH L1/L2 (baked) or octahedral maps (DDGI: 6x6 or 8x8 irradiance texels, 14x14-16x16
depth texels, 1-texel borders for bilinear).

## 2. DDGI update (per frame)
1. Trace N rays (128-256) per probe with a random rotation per frame; shade hits with direct
   light + previous-frame probe irradiance (infinite bounces over time).
2. Blend into the octahedral irradiance map (hysteresis ~0.97) and store mean distance and
   distance squared in the depth map.
3. Relocate probes stuck inside geometry (many backface hits) and deactivate probes in
   empty space.

## 3. Sampling at a shading point
Trilinear blend of the 8 surrounding probes with weights:
- Trilinear weight,
- Backface weight `(dot(dirToProbe, N) + 1) / 2` squared,
- **Chebyshev visibility** from the depth map (variance shadow test) to stop leaks through walls,
- Normal and view bias on the sample position (`P + N*0.2*spacing + V*0.8*...`).
Then sum `irradiance * weight` / total weight; multiply by albedo/pi.

## 4. Practical
RTXGI-DDGI SDK provides shaders and a D3D12/Vulkan integration; scrolling volumes (cascades)
for open worlds. Baked SH probes work without RT hardware (update offline).

## Gotchas
- Leaks remain where walls are thinner than probe spacing; thicken or add probes.
- Low ray counts flicker; increase hysteresis, but lighting then lags.
- Only diffuse; pair with reflection probes or RT reflections for specular.

## Verify
- [ ] Probe visualisation shows sensible irradiance; no light leaking under doors at grid scale.
