---
id: computing-software.computer-graphics-engineering.shader-programming.wetness-snow-weather-layering
name: wetness-snow-weather-layering
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, wetness-shader, snow-shader, weather-effects, puddles, rain-ripples, material-layering]
level: practitioner
status: draft
description: "Layer dynamic weather on materials: wetness darkening and smoother specular, puddles by height, rain ripples, and snow accumulation driven by world-up normal and masks."
sources: ["https://seblagarde.wordpress.com/2013/04/14/water-drop-3b-physically-based-wet-surfaces/", "https://seblagarde.wordpress.com/2013/01/03/water-drop-2b-dynamic-rain-and-its-effects/", "https://www.gdcvault.com/play/1020210/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Snow, wetness and weather layering

## 1. Wetness (Lagarde, "Water drop" series)
Wet porous surfaces get darker and smoother:
```glsl
float porosity = saturate((roughness - 0.5) / 0.4);          // rough = more porous
float factor = mix(1.0, 0.2, (1.0 - metallic) * porosity);  // darkening
albedo   *= mix(1.0, factor, wetness);
roughness = mix(roughness, 0.1, wetness);                    // glossier film
// F0 stays ~0.02-0.04 for water on dielectrics
```
Metals barely darken; the water film mostly affects roughness.

## 2. Puddles
- Puddle mask from the height map: `puddle = saturate((waterLevel - height) / blend)`.
- In puddles: roughness -> 0.05, albedo darkened, normal flattened toward the geometry normal.
- Ripples: an animated ripple normal map (or procedural rings from a cell hash) blended in by
  rain intensity, only on up-facing surfaces (`N.y > 0.7`).

## 3. Snow accumulation
```glsl
float up = dot(worldNormal, vec3(0,1,0));                      // use the normal-mapped normal
float snow = smoothstep(snowThreshold, snowThreshold + 0.2, up + noise(worldPos.xz * 0.3) * 0.2);
snow *= snowAmount * occlusionMask;                            // occluded areas stay clear
albedo    = mix(albedo, snowAlbedo, snow);
roughness = mix(roughness, 0.6, snow);
N         = normalize(mix(N, snowNormal, snow));
```
- Occlusion mask: render a top-down depth map of the scene; snow only where the surface is the
  highest at that XZ (no snow under roofs).
- Height-blend snow with the base height map so it settles in cracks first.
- Thick snow: displace vertices (tessellation or pre-subdivided) by the snow mask.

## 4. Driving it
Global uniforms (`rainIntensity`, `wetness`, `snowAmount`) animated by the weather system; wetness
lags rain (dries slowly). Per-object masks for sheltered areas.

## Gotchas
- Applying darkening to emissive/unlit materials looks wrong; exclude them.
- Snow on vertical surfaces with normal maps can speckle; blend with the geometric normal.
- Keep all weather paths in one shader permutation driven by uniforms, or every material doubles
  its variants.

## Verify
- [ ] Dry -> wet transition darkens rough materials more than smooth ones.
- [ ] No snow under overhangs; accumulation follows slope.
