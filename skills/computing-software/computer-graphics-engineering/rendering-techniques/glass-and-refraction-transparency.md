---
id: computing-software.computer-graphics-engineering.rendering-techniques.glass-and-refraction-transparency
name: glass-and-refraction-transparency
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, glass-shader, refraction, fresnel, absorption, rough-glass, gltf-extensions]
level: practitioner
status: docs-checked
description: "Render glass with the glTF transmission and volume model: Fresnel reflection, thin versus volumetric, thickness, Beer-Lambert attenuation, IOR and rough-glass blur."
sources: ["https://google.github.io/filament/Filament.md.html#materialsystem/refraction", "https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_transmission", "https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_volume"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Glass, transmission and refraction

## 1. Why alpha is not enough
Core glTF alpha is "alpha as coverage": it says whether the surface exists. Glass is a surface that
exists: light enters it and is reflected, refracted, absorbed or transmitted, and even a perfectly
clear sheet stays visible through its reflection. Alpha coverage weakens reflections as the surface
fades; optical transparency does not. Model glass with transmission, not with alpha blending.

## 2. Thin glass: `KHR_materials_transmission`
- Parameters: `transmissionFactor` (default 0) and `transmissionTexture` (red channel, multiplied by
  the factor). Value 1 means 100% of the light that penetrates the surface (that is, is not
  specularly reflected) is transmitted rather than diffusely re-emitted.
- The surface is treated as infinitely thin: two back-to-back surfaces, no net refraction, no
  scattering, no dispersion. Roughness still blurs transmitted light because the microfacets of the
  front and back faces are uncorrelated and act as tiny prisms (modulated by the IOR, default 1.5).
- Tint: `baseColor` tints the transmitted light; for thin surfaces absorption is constant and
  equal to `1 - baseColor`.
- Reflection is unchanged: the dielectric is a Fresnel mix with IOR 1.5 of the specular layer over
  a base, and transmission only modifies the base layer (a specular BTDF mixed with diffuse).
- Metals absorb all refracted light, so with `metallicFactor` 1 the transmission value is irrelevant.
- Keep `alphaMode` OPAQUE unless you also want alpha coverage; transmission is not blending. The
  extension does not dictate a rendering algorithm or ordering.

## 3. Thick glass: `KHR_materials_volume`
Combine it with transmission; the volume only takes effect if light can enter the surface.
- `thicknessFactor` (default 0 = thin-walled), `thicknessTexture` (green channel, range 0..1,
  multiplied by the factor), `attenuationDistance` (default infinity), `attenuationColor`
  (default [1, 1, 1]). A non-zero thickness requires a closed (manifold) mesh, and the medium is
  homogeneous and not texturable.
- Refraction angle comes from `KHR_materials_ior`, or 1.5 when absent.
- Absorption by Beer's law: `sigma_t = -log(c) / d` for attenuation colour `c` and distance `d`,
  so the transmittance after travelling distance `x` is `T(x) = c^(x / d)`. Scattering is not
  modelled (sigma_t = sigma_a).
- Base colour changes light at the boundary (a uniform tint); absorption depends on the path
  length, so thicker parts of the object are darker or more saturated.
- Thickness is baked like ambient occlusion but with rays cast opposite the surface normal; it
  estimates the exit distance at the entry point and is lossy because the true distance depends on
  the incidence angle. Ray tracers should ignore the map and use the real distance, though they
  must still test `thicknessFactor` to decide thin versus volumetric.

## 4. Rasterizer notes
The extensions define the material, not the algorithm, and say that ordering of transparent
primitives is a hard problem they do not solve. Thickness is baked into a map because it is hard to
compute at run time in a rasterizer. Choose the refraction technique per engine and check it against
the material definitions above.

## Gotchas
- Thickness from a map is an approximation, accurate only if the baked values reflect real
  thickness; keep them close to the true thickness so rasterized and ray-traced results look alike.

## Verify
- [ ] A clear sheet with transmission 1 is still visible through reflections.
- [ ] Rough glass blurs the background in proportion to roughness.
- [ ] Thin-walled (thickness 0) and volumetric (thickness above 0) versions of a mesh differ as expected.

## Checked
2026-11-08. Read in full: Khronos KHR_materials_transmission and KHR_materials_volume READMEs;
the cited Filament page was fetched but contains no refraction section (the anchor does not exist
in that document), so nothing here rests on it. Confirmed: parameter names,
defaults and texture channels, tint rule, metals rule, blend-mode guidance, volume requirements,
IOR default 1.5, Beer's-law derivation, thickness-map caveats. Removed: the GLSL refraction/LOD
snippet, `exp(-absorption * thickness)` pseudo-code, the screen-space copy recipe, and the
dispersion and TAA remarks, none of which the sources state.
Method: documentation only; no commands were run.
