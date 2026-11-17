---
id: computing-software.computer-graphics-engineering.shader-programming.fresnel-rim-lighting
name: fresnel-rim-lighting
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, rim-lighting, fresnel-effect, schlick-fresnel, stylised-shading, shader-graph]
level: intro
status: draft
description: "Add Fresnel-based rim lighting in shaders: Schlick approximation, view-normal falloff, controlling width and power, and combining with lighting without double counting."
sources: ["https://en.wikipedia.org/wiki/Schlick%27s_approximation", "https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/Fresnel-Effect-Node.html", "https://learnopengl.com/PBR/Theory"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fresnel rim lighting

## 1. The term
```glsl
float NdotV = clamp(dot(normalize(N), normalize(V)), 0.0, 1.0);
float rim = pow(1.0 - NdotV, rimPower);           // rimPower 2-5 typical
// Schlick form (physically motivated reflectance)
vec3 F = F0 + (1.0 - F0) * pow(1.0 - NdotV, 5.0);
```
V points from the surface to the camera. Unity Shader Graph's Fresnel Effect node is exactly
`pow(1 - saturate(dot(N, V)), power)`.

## 2. Stylised rim
```glsl
float rimMask = smoothstep(rimStart, rimStart + rimWidth, 1.0 - NdotV);
rimMask *= saturate(dot(N, L) * 0.5 + 0.5);       // only on the lit side (optional)
vec3 color = lit + rimColor * rimMask * rimIntensity;
```
Use `smoothstep` instead of `pow` for a hard, cel-shaded band.

## 3. Uses
- Character readability against dark backgrounds, selection highlights, shields (combine with
  depth intersection glow), x-ray silhouettes (render with depth test off).
- Physically, rim brightening on rough dielectrics comes from Fresnel in the specular BRDF: if you
  already use a PBR BRDF with IBL, an extra rim adds energy; keep it an artistic layer and scale it
  by exposure.

## Gotchas
- Use the **interpolated, normalised** normal; flat low-poly meshes give faceted rims.
- With normal maps, rim follows bumps; use the vertex normal for a cleaner silhouette rim.
- Orthographic cameras: V is constant (the camera forward), so compute V from the camera direction,
  not position.
- Back faces (two-sided materials) need N flipped with `gl_FrontFacing` or NdotV goes negative.

## Verify
- [ ] Rim width stable as the object moves across the screen (perspective V correct).
- [ ] No rim on faces pointing directly at the camera.
