---
id: computing-software.computer-graphics-engineering.rendering-techniques.multiple-scattering-energy-compensation
name: multiple-scattering-energy-compensation
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, physically-based-shading, multiscattering, energy-compensation, kulla-conty, rough-metals]
level: advanced
status: docs-checked
description: "Add multiple-scattering energy compensation to microfacet specular so rough metals do not darken, using the Filament scaled-lobe approach and its DFG lookup table."
sources: ["https://google.github.io/filament/Filament.md.html#materialsystem/improvingthebrdfs/energylossinspecularreflectance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple-scattering energy compensation

**Problem:** the Cook-Torrance BRDF models one bounce of light per microfacet event, so it loses energy
at high roughness (a ray reflected onto another microfacet is discarded by masking/shadowing). Rough
metals look too dark.

## 1. Filament approach (cheap, real-time)
Heitz (2016) gives a multiscattering BRDF but only a stochastic evaluation, which is not suitable for
real-time. Kulla and Conty add an energy-compensation term as an extra lobe; Lagarde and Golubev
simplify it to a scaled copy of the GGX lobe:
```
f_r = f_ss + F0 * (1/r - 1) * f_ss        r = integral of D * V * <NoL> over the hemisphere
```
`r` is the same integral as the IBL DFG terms without the Fresnel term, so it can be stored in the DFG
lookup table. With that table the direct-light code is:
```glsl
vec3 energyCompensation = 1.0 + f0 * (1.0 / dfg.y - 1.0);
Fr *= energyCompensation;   // scale the specular lobe
```
## 2. The multiscatter DFG table
Assuming f90 = 1, Filament rebuilds the split sum with a "multiscatter" pair:
- `DFG1_ms` = sum of `Fc(VoH) * V * (VoH/NoH) * NoL` (Fresnel-weighted), times 4/N;
- `DFG2_ms` = the same sum without Fresnel, times 4/N, and this is `r`.
- IBL specular colour is then `mix(dfg.xxx, dfg.yyy, f0)`, i.e. `(1 - f0) * dfg.x + f0 * dfg.y`.

The analytic DFG approximations by Karis (2014) and Narkowicz (2014) are NOT compatible with this
compensation term: use the precomputed LUT. The table values are in [0, 1] but 8-bit textures lack the
precision; Filament suggests RG16F where available.

## Gotchas
- Compensation must use the same D and V model the LUT was built with.
- It matters for metals (it scales by F0); dielectrics have low F0 and gain little.

## Verify
- [ ] White furnace test (uniform white lighting): a fully reflective metal sphere (F0 = 1) should be
  indistinguishable from the background at every roughness. Without compensation it darkens as
  roughness rises.

## Checked
2026-11-09. Read the Filament materials guide sections on energy loss in specular reflectance
(Kulla/Conty and Lagarde/Golubev lobe, `energyCompensation` listing, white furnace) and
pre-integration for multiscattering (DFG multiscatter terms, analytic-approximation incompatibility,
RG16F note), via a text extraction of the page. Corrected: the compensation uses `1.0 / dfg.y`
(Filament listing), not `1/(dfg.x + dfg.y)`, and the LUT split is `(1 - f0) * dfg.x + f0 * dfg.y`.
Removed: the "~60 percent loss" figure, the Fdez-Aguera section and Kulla-Conty production-table
formulas (JCGT and Imageworks sources could not be read as text here).
Method: documentation only; no commands were run.
