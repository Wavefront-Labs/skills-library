---
id: computing-software.computer-graphics-engineering.rendering-techniques.underwater-fog-and-caustics
name: underwater-fog-and-caustics
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetrics, underwater-rendering, caustics, water-absorption, waterline, light-shafts, water-rendering]
level: practitioner
status: draft
description: "Render underwater scenes: wavelength-dependent absorption fog, waterline split rendering, animated caustics projected from the surface, god rays and refraction at the surface."
sources: ["https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-2-rendering-water-caustics", "https://www.alanzucconi.com/2019/09/13/believable-caustics-reflections/", "https://www.gdcvault.com/play/1025406/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Underwater fog and caustics

## 1. Absorption fog
Water absorbs red fastest, then green, leaving blue: use per-channel extinction.
```glsl
vec3 sigmaA = vec3(0.45, 0.09, 0.06);         // per metre, clear ocean-ish; murky water is larger
vec3 sigmaS = vec3(0.01, 0.02, 0.03) * turbidity;
vec3 T = exp(-(sigmaA + sigmaS) * viewDistance);
vec3 inscatter = waterColor * (1.0 - T);       // or integrate sun light with depth attenuation
color = sceneColor * T + inscatter;
```
- Light reaching depth d below the surface is attenuated by `exp(-sigma_t * d)` too: the deeper
  objects are lit bluer and darker; apply to direct light by the object's depth below the surface.

## 2. Waterline
When the camera straddles the surface, split the screen: compute per pixel whether the view ray
starts underwater (camera below a height function evaluated along the near plane), apply
underwater fog below the line and a distortion/meniscus band at the line. Simple approach: render a
fullscreen pass with a mask from the water surface rendered from the near plane.

## 3. Caustics
- **Projected texture**: an animated caustics texture (tiling, two layers scrolling different
  directions, `min()` of the two for sharp crossings) projected from above in world XZ onto
  underwater surfaces, scaled by `saturate(N.y)` and depth fade. Chromatic split: sample R/G/B with
  slight UV offsets.
- **Computed**: refract light rays through the water surface normal map and accumulate on a plane
  (GPU Gems 1 ch2), or compute caustics intensity from the surface's area change (Jacobian of the
  refracted grid) in a light-space map.
- Only within the light-lit region (shadowed by the sun shadow map).

## 4. Light shafts underwater
Volumetric froxels or a radial blur from the sun's screen position, with noise to animate them.
Stronger and bluer than in air.

## 5. Surface from below
Total internal reflection beyond ~48.6 degrees (critical angle for IOR 1.33): reflect the
underwater scene instead of showing the sky (Snell's window).

## Gotchas
- Applying above-water fog and underwater fog both to the same pixel double-fogs; one path per pixel.
- Caustics on surfaces facing down look wrong; mask by normal.

## Verify
- [ ] Distant underwater objects fade to blue-green, reds disappear first.
- [ ] Caustics move consistently with surface waves and only appear in lit areas.
