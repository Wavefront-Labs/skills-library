---
id: computing-software.computer-graphics-engineering.shader-programming.water-surface-shader-gerstner
name: water-surface-shader-gerstner
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, water-shader, gerstner-waves, fresnel, depth-fade, refraction]
level: advanced
status: draft
description: "Shade water surfaces: Gerstner wave displacement with normals, Fresnel reflection, depth-based colour and foam, refraction distortion, and screen-space edge cases."
sources: ["https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-1-effective-water-simulation-physical-models", "https://catlikecoding.com/unity/tutorials/flow/waves/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Water surface shading with Gerstner waves

## 1. Gerstner displacement (vertex)
```glsl
vec3 gerstner(vec2 xz, vec2 dir, float steep, float wavelength, float t, inout vec3 T, inout vec3 B) {
  float k = 6.28318 / wavelength, c = sqrt(9.8 / k), a = steep / k;
  vec2 d = normalize(dir); float f = k * (dot(d, xz) - c * t);
  T += vec3(-d.x*d.x*steep*sin(f), d.x*steep*cos(f), -d.x*d.y*steep*sin(f));
  B += vec3(-d.x*d.y*steep*sin(f), d.y*steep*cos(f), -d.y*d.y*steep*sin(f));
  return vec3(d.x * a * cos(f), a * sin(f), d.y * a * cos(f));
}
// sum 3-8 waves; T starts (1,0,0), B starts (0,0,1); normal = normalize(cross(B, T))
```
Sum of steepness across waves must stay below 1 or crests loop over themselves.

## 2. Fragment
```glsl
float fres = 0.02 + 0.98 * pow(1.0 - max(dot(N, V), 0.0), 5.0);     // Schlick, water F0 0.02
vec3 refl = sampleEnvOrSSR(reflect(-V, N));
float sceneDepth = linearDepth(texture(uDepth, screenUV).r);
float waterDepth = sceneDepth - fragViewDepth;                      // thickness along view
vec3 absorb = exp(-waterDepth * vec3(0.45, 0.09, 0.06));            // red absorbed fastest
vec2 distort = N.xz * 0.03 * clamp(waterDepth, 0.0, 1.0);
vec3 refr = texture(uSceneColor, screenUV + distort).rgb * absorb + deepColor * (1.0 - absorb);
float foam = 1.0 - smoothstep(0.0, 0.6, waterDepth);               // shoreline foam
color = mix(refr, refl, fres) + foam * foamTex;
```
Needs the opaque scene colour and depth copied before the water pass.

## 3. Detail
Add two scrolling normal maps (different scales/directions) on top of Gerstner normals for
small ripples; FFT ocean (Tessendorf) when you need realistic open sea.

## Gotchas
- Refraction distortion samples objects in front of the water; reject samples whose depth is
  nearer than the water and fall back to undistorted UV.
- Fresnel needs the geometric normal blended in at distance, or the horizon sparkles.
- Displacement in vertex shader requires dense or tessellated mesh near the camera (clipmap grid).

## Verify
- [ ] Shoreline foam follows geometry; no refraction leaks of objects above water.
