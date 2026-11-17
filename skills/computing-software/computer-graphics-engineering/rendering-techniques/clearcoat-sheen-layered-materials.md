---
id: computing-software.computer-graphics-engineering.rendering-techniques.clearcoat-sheen-layered-materials
name: clearcoat-sheen-layered-materials
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, physically-based-shading, clearcoat, sheen, layered-materials, gltf-extensions, anisotropy]
level: advanced
status: docs-checked
description: "Add clearcoat and sheen layers to a PBR material: Filament and glTF lobe formulas, energy conservation between layers, extension parameters and layering order."
sources: ["https://google.github.io/filament/Filament.md.html#materialsystem/clearcoatmodel", "https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_clearcoat", "https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_sheen"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clearcoat, sheen and layered materials

## 1. Clearcoat (car paint, varnish, lacquer)
Filament models the coat as a second Cook-Torrance lobe: GGX distribution, Kelemen visibility,
Schlick Fresnel, with F0 = 0.04 (an air-polyurethane interface, IOR 1.5). The coat roughness is
remapped and clamped like the base roughness (Filament clamps perceptual roughness to 0.089..1):
```glsl
float Fc  = F_Schlick(0.04, LoH) * clearCoat;     // clearCoat = strength 0..1
float Dc  = D_GGX(ccRoughness, NoH);
float Vc  = 0.25 / (LoH * LoH);                   // Kelemen: cheap, fine for a smooth coat
float Frc = Dc * Vc * Fc;
vec3 color = baseColor * ((Fd + Fr) * (1.0 - Fc) + Frc);  // base attenuated by coat Fresnel
```
- Base layer F0 must be recomputed for a coat-to-material interface instead of air-to-material
  (Filament: `f0_base = (1 - 5*sqrt(f0))^2 / (5 - sqrt(f0))^2`).
- IBL: the coat is a second specular lobe along the view direction, using the same DFG
  approximation as the main lobe. Filament's IBL energy step is `iblDiffuse *= 1 - Fc`,
  `iblSpecular *= (1 - Fc)^2`, then `iblSpecular += specularIBL(r, coatRoughness) * Fc`.
- glTF `KHR_materials_clearcoat` (ratified): `clearcoatFactor` (default 0, 0 disables the layer),
  `clearcoatRoughnessFactor` (default 0), `clearcoatTexture` (red channel),
  `clearcoatRoughnessTexture` (green channel), `clearcoatNormalTexture`. Coat BRDF alpha is
  `clearcoatRoughness^2`; layering uses `fresnel_coat` with IOR 1.5, weighting the layer by
  `clearcoat * fresnel` and the base by one minus that. Emission sits under the coat and is
  darkened by `1 - clearcoat * clearcoat_fresnel`.
- Without `clearcoatNormalTexture` no normal mapping is applied to the coat, even when the base is
  normal mapped. A coat normal map needs a defined tangent space (provide NORMAL and TANGENT).

## 2. Sheen (cloth, velvet, dust)
Retro-reflective grazing highlight. Estevez and Kulla's "Charlie" distribution (an exponentiated
sinusoid) with a simple visibility term (Filament cites Neubelt and Pettineo; glTF cites
Ashikhmin and Premoze for the same expression):
```glsl
float D_Charlie(float r, float NoH) { float inv = 1.0/r; float sin2 = 1.0 - NoH*NoH; return (2.0+inv)*pow(sin2, inv*0.5)/(2.0*PI); }
float V_Neubelt(float NoV, float NoL) { return 1.0 / (4.0 * (NoL + NoV - NoL*NoV)); }
vec3 sheen = sheenColor * D_Charlie(sheenRoughness, NoH) * V_Neubelt(NoV, NoL);
```
- In glTF the `r` passed to the distribution is `alpha_g = sheenRoughness^2`.
- glTF `KHR_materials_sheen` (ratified): `sheenColorFactor` (default [0,0,0], 0 disables the
  layer), `sheenColorTexture` (RGB), `sheenRoughnessFactor` (default 0), `sheenRoughnessTexture`
  (alpha channel). Sheen roughness is independent of the material roughness.
- Energy conservation (Conty and Kulla albedo scaling): scale the base layer by
  `1 - max3(sheenColor) * E(VdotN)`, with `E` from a lookup table indexed by `VdotN` and
  `sheenRoughness`. The full form takes the minimum over the view and light directions. The simpler
  Ashikhmin-style visibility above is not energy conserving when combined with albedo scaling.
- If clearcoat is also active, clearcoat is layered on top of sheen.

## 3. Other layers
glTF also defines `KHR_materials_anisotropy` (brushed metal) and `KHR_materials_transmission` /
`KHR_materials_volume` (glass). Real-time engines implement subsets of a full layered stack.

## Gotchas
- The glTF layering is a simple approximation: infinitely thin coat, no refraction, no scattering
  between layers, and the coat and base Fresnel terms computed independently.
- Coat normal differs from base normal; reusing the base normal loses the "smooth over bumpy" look.

## Verify
- [ ] A coat strength of 0 reproduces the uncoated material exactly.
- [ ] Sheen with `sheenColor` zero reproduces the base material exactly.

## Checked
2026-11-08. Read in full: Filament materials guide (clear coat and cloth sections, clear coat IBL),
Khronos KHR_materials_clearcoat and KHR_materials_sheen READMEs. Confirmed: F0 0.04 at IOR 1.5, GGX
+ Kelemen + Schlick coat, 0.089 roughness clamp, base F0 recomputation, IBL second lobe, extension
parameter names, defaults and texture channels, alpha = roughness^2, Charlie distribution and visibility
formulas, albedo scaling and its table lookup, clearcoat layered above sheen. Corrected: the base
direct-light formula attenuated the specular by the coat Fresnel twice; Filament uses
`(Fd + Fr) * (1 - Fc) + Frc` there (the squared term applies to IBL only). Removed
unsourced claims: OpenPBR, iridescence, per-light cost and permutation advice, sample asset names.
Method: documentation only; no commands were run.
