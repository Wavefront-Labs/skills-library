---
id: computing-software.computer-graphics-engineering.shader-programming.grass-and-foliage-shading
name: grass-and-foliage-shading
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, grass-shader, foliage-shading, translucency, wind-animation, alpha-test, vegetation]
level: practitioner
status: draft
description: "Shade grass and foliage convincingly: two-sided lighting and translucency, normals bent to sphere/up, colour variation, wind sway, distance fading and alpha-test anti-aliasing."
sources: ["https://www.ea.com/frostbite/news/approximating-translucency-for-a-fast-cheap-and-convincing-subsurface-scattering-look", "https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis", "https://www.ghostoftsushima.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Foliage and grass shading

## 1. Normals
Raw card normals look flat and pop as cards rotate. Fix in the asset or shader:
- **Spherical normals**: point leaf normals outward from the tree/bush centre (bake in DCC).
- **Grass**: blend the blade normal toward world up (`normalize(mix(N, up, 0.5-0.8))`) so a field
  lights like a continuous surface; Ghost of Tsushima tilts normals and rounds blades in-shader.

## 2. Translucency (cheap SSS)
Leaves glow when backlit. Frostbite's approximation:
```glsl
vec3 H = normalize(L + N * distortion);
float VdotH = pow(saturate(dot(V, -H)), power) * scale;
vec3 trans = lightColor * (VdotH + ambientTrans) * thickness;   // thickness from a baked map
col += albedo * trans;
```
Two-sided: flip N on back faces (`gl_FrontFacing`) and add the translucency term.

## 3. Variation and colour
- Per-instance hue/brightness from instance ID or world-position hash.
- Darken toward the base (AO by blade height in vertex colour or UV.y).
- Dry/green variation from a low-frequency world-space noise texture.

## 4. Wind
Vertex displacement weighted by height (`uv.y` or vertex colour): main bend plus per-blade flutter
with phase offset from position. See vertex displacement and wind animation skill. Keep previous
frame positions for motion vectors (TAA) by evaluating wind at last frame's time too.

## 5. Alpha-tested edges
- Use alpha-to-coverage with MSAA or hashed alpha with TAA.
- Preserve alpha coverage in mips (scale alpha per mip so coverage matches level 0), otherwise
  distant foliage thins out and disappears.
- Fade distant grass by scaling blades down (not alpha) before culling.

## Gotchas
- Shadow maps of alpha-tested cards need the same alpha test in the shadow pass.
- Overdraw from layered cards dominates foliage cost on mobile; minimise transparent area (tight
  meshes around leaves).
- Specular on grass looks plastic; reduce F0/raise roughness, or use per-blade specular tinted by
  albedo.

## Verify
- [ ] Field reads as continuous at distance (no card orientation patterns).
- [ ] Backlit leaves show translucency; distant foliage keeps density.
