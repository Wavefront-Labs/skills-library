---
id: computing-software.computer-graphics-engineering.rendering-techniques.toon-cel-shading
name: toon-cel-shading
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, non-photorealistic-rendering, toon-shading, cel-shading, ramp-texture, anime-shading, rim-light, shadow-threshold, face-normals, toon-ramp]
level: practitioner
status: draft
description: "Build stylised toon/cel shading: quantised or ramp-texture diffuse, stepped specular and rim light, shadow integration, artist-controlled normals for faces."
sources: ["https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf", "https://roystan.net/articles/toon-shader/", "Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 15.1", "https://docs.unity3d.com/Packages/com.unity.toonshader@0.9/manual/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toon / cel shading

**Goal:** a hand-drawn, anime or comic look with flat colour bands that artists control,
stable under animation and lighting changes (RTR4 §15.1; Guilty Gear Xrd GDC 2015).

## 1. Core: quantise the light response
```glsl
float NdotL = dot(N, L);
float lit = smoothstep(threshold - softness, threshold + softness, NdotL);   // hard but AA'd edge
vec3 diffuse = mix(shadowColor, baseColor, lit * shadowAtten);
```
Or a **ramp texture**: `texture(ramp, vec2(NdotL * 0.5 + 0.5, rampRow)).rgb` — artists paint
bands, colour shifts in shadow (warm light, cool/purple shadows), per-material rows.
Use `smoothstep` with a small width (or `fwidth`-based) rather than `step` so band edges
don't alias.

## 2. Specular and rim
```glsl
float spec = smoothstep(0.5 - e, 0.5 + e, pow(max(dot(N, H), 0.0), glossiness));  // crisp highlight
float rim  = smoothstep(rimMin, rimMax, 1.0 - dot(N, V)) * lit;                  // backlight edge
color = diffuse + spec * specColor + rim * rimColor;
```

## 3. Shadows from other objects
Real-time shadow maps produce soft/blurry edges that clash with the style: threshold the
shadow term (`step(0.5, shadow)` with slight smoothing) and combine with the NdotL band, or
use only self-shading for characters and blob shadows on the ground.

## 4. Artist control of normals (faces)
Realistic normals give ugly patchy shadows on faces. Techniques:
- **Normal transfer/editing**: copy normals from a sphere/ellipsoid proxy onto the face mesh
  (Blender "Data Transfer" modifier, custom split normals) for smooth, round shading.
- **Face shadow maps**: SDF-style threshold texture authored per face, sampled using the light
  angle around the head's up axis (common in modern anime games).
- Vertex colour channels for per-vertex shadow bias ("always lit" areas, AO-like threshold
  offsets, as in Guilty Gear Xrd).

## 5. Lighting setup
Toon shading reads best with **one dominant key light** + flat ambient; many lights and IBL
fight the look. Clamp light intensity; convert scene HDR lighting to a normalised key
direction per character if needed.

## Gotchas
- Tone mapping (ACES) desaturates and shifts the flat colours — use neutral/linear tone
  mapping or exclude stylised materials.
- Band edges crawl on low-poly meshes: add geometry in shoulders/faces or smooth normals.
- MSAA helps band edges; TAA can smear stylised lines.

## Verify
- [ ] Turntable with rotating light: bands move smoothly, no patchy face shadows.
- [ ] Art-director-approved ramp per material.
- [ ] Combined with outlines, consistent across characters and environments.
