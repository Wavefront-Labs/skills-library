---
id: computing-software.computer-graphics-engineering.rendering-techniques.area-lights-with-ltc
name: area-lights-with-ltc
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, area-lights, ltc, linearly-transformed-cosines, rect-lights]
level: sme
status: draft
description: "Shade rectangular and polygonal area lights in real time with Linearly Transformed Cosines: LUT setup, polygon integration, horizon clipping and textured lights."
sources: ["https://eheitzresearch.wordpress.com/415-2/", "https://blog.selfshadow.com/publications/s2016-advances/", "https://github.com/selfshadow/ltc_code"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Area lights with LTCs

**Idea:** a GGX lobe is approximated by a clamped cosine distribution transformed by a 3x3 matrix
M. Integrating the cosine over a polygon has a closed form, so transform the light polygon by
M^-1 and integrate.

## 1. Data
Two 64x64 LUTs indexed by (roughness, sqrt(1 - NoV)): `ltc_1` (4 entries of M^-1) and `ltc_2`
(GGX norm, Fresnel scale/bias, sphere form factor). Use the precomputed tables from the paper's
code release (float16 textures).

## 2. Shading
```glsl
vec4 t1 = texture(ltc1, uv);
mat3 Minv = mat3(vec3(t1.x, 0, t1.y), vec3(0, 1, 0), vec3(t1.z, 0, t1.w));
// build orthonormal frame around N with T1 in the N-V plane
vec3 T1 = normalize(V - N * dot(V, N)), T2 = cross(N, T1);
Minv = Minv * transpose(mat3(T1, T2, N));
vec3 spec = LTC_Evaluate(N, V, P, Minv, lightCorners, twoSided);
vec3 diff = LTC_Evaluate(N, V, P, mat3(1), lightCorners, twoSided);  // identity = Lambert
vec2 t2 = texture(ltc2, uv).xy;
spec *= specColor * t2.x + (1.0 - specColor) * t2.y;
color = lightColor * (spec + albedo * diff);
```
`LTC_Evaluate` transforms corners, clips the polygon to the horizon, and sums edge integrals
(`acos`-based, use the fitted `IntegrateEdgeVec` approximation for precision).

## 3. Cheaper horizon clipping
The 2017 follow-up replaces polygon clipping with a sphere approximation using the
form-factor vector and the `ltc_2` sphere LUT: fewer branches, fine for most lights.

## 4. Textured lights
Prefilter the light's texture into mips; fetch at the point where the transformed cosine
projects onto the light plane with LOD from the projected area.

## Gotchas
- No shadows: combine with shadow maps from the light centre or ray-traced soft shadows.
- three.js RectAreaLight uses LTC (needs `RectAreaLightUniformsLib.init()`).
- Precision: use the edge-integral approximation from the paper; naive `acos` breaks at grazing.

## Verify
- [ ] Compare against a Monte Carlo reference of a GGX surface lit by a quad; highlight shape
  stretches correctly with roughness.
