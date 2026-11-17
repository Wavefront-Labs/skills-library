---
id: computing-software.computer-graphics-engineering.rendering-techniques.validating-pbr-against-references
name: validating-pbr-against-references
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, physically-based-shading, pbr-validation, furnace-test, white-furnace, reference-rendering, mitsuba, energy-conservation]
level: advanced
status: draft
description: "Validate a real-time PBR implementation: white furnace tests, comparing with Mitsuba/PBRT/Filament references, MERL/measured data checks, and common energy and unit errors."
sources: ["https://google.github.io/filament/Filament.md.html", "https://blog.selfshadow.com/publications/s2017-shading-course/", "https://www.mitsuba-renderer.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating PBR against references

## 1. White furnace test
Place a sphere with albedo = 1 (or F0 = 1 metal) in a uniform white environment (radiance = 1),
no other lights. A correct, energy-conserving BRDF integrated over the hemisphere returns <= 1
everywhere and, for a perfect non-absorbing material, exactly 1 (the sphere "disappears").
- Single-scattering GGX loses energy at high roughness (sphere darkens at the rim): expected unless
  you implement multiple-scattering compensation.
- Brighter than background anywhere = bug (missing 1/PI, double-counted Fresnel, Burley without
  renormalisation, IBL scale error).

Also run a **weak furnace test** (only D and G, no Fresnel) to isolate the microfacet distribution.

## 2. Reference renders
1. Build an identical scene in Mitsuba 3 or PBRT-v4 (same geometry, camera FOV, light units, HDR
   environment, BRDF parameters with `roughvalue = alpha` vs perceptual mapping noted).
2. Render your engine with exposure, tonemapping and bloom disabled; output linear EXR.
3. Compare per-pixel ratio or FLIP; plot along a scanline across the sphere.

Filament's material sample scenes and Khronos glTF Sample Assets (with the Khronos glTF
Sample Viewer as reference) are free cross-checks for glTF PBR.

## 3. Typical errors found
| Symptom | Cause |
|---|---|
| everything 3x too bright | missing 1/PI in diffuse, or light intensity in wrong units |
| dark rims at roughness 1 | single-scattering energy loss (add Kulla-Conty/Fdez-Aguera compensation) |
| rough metals too dark in IBL | prefiltered mip mapping vs roughness mismatch |
| specular too sharp | perceptual roughness used as alpha |
| colour shifts | albedo texture not decoded from sRGB; lighting in gamma space |
| IBL and analytic lights disagree | environment not in the same radiometric units as lights |

## 4. Measured data
MERL BRDF database: fit your model's parameters to measured materials and compare shapes of the
lobes; good for checking that a model can represent real materials.

## 5. Automate
Render a material grid (roughness x metallic) in CI and compare to stored references; any change
to BRDF code must update references intentionally.

## Gotchas
- Different references use different roughness remappings; document the mapping.
- Bloom/TAA/tonemapping must be off for numeric comparisons.

## Verify
- [ ] Furnace test passes (<= 1, matching expected energy loss curve).
- [ ] Mean error vs Mitsuba under X% on the material grid.
