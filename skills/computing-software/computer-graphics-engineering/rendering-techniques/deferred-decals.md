---
id: computing-software.computer-graphics-engineering.rendering-techniques.deferred-decals
name: deferred-decals
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, deferred-decals, decals, projected-decals, g-buffer, clustered-decals, dbuffer]
level: sme
status: draft
description: "Render projected decals: box-projected deferred decals into the G-buffer, DBuffer and clustered forward decals, normal blending, and stretching fixes."
sources: ["https://www.slideshare.net/blindrenderer/screen-space-decals-in-warhammer-40000-space-marine-14699854", "https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-materials-in-unreal-engine", "https://www.activision.com/cdn/research/2017_Sig_Improved_Culling_final.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deferred decals

## 1. Box-projected deferred decal
After the G-buffer pass, before lighting, draw a unit cube per decal transformed by its decal-to-world matrix.
```glsl
float d = texelFetch(depthTex, ivec2(gl_FragCoord.xy), 0).r;
vec3 posWS = reconstructWorld(gl_FragCoord.xy, d);
vec3 posDS = (invDecalModel * vec4(posWS, 1)).xyz;        // decal space, cube is [-0.5,0.5]^3
if (any(greaterThan(abs(posDS), vec3(0.5)))) discard;
vec2 uv = posDS.xz + 0.5;                                  // project along local Y
vec4 c = texture(decalAlbedo, uv);
outAlbedo = vec4(c.rgb, c.a);                              // blend: src alpha into albedo RT
```
- Draw back faces with depth test GREATER (or front faces with LESS, switching when the camera is inside the box).
- Use the stencil to exclude characters/dynamic objects that should not receive decals.

## 2. Normals
- Normal-mapped decals need a tangent frame on the receiving surface: build it from the decal's own axes, or
  from screen-space derivatives of `posWS`.
- Blend normals in world space then renormalise; plain alpha-blending octahedral-encoded normals is wrong,
  so either use a blendable normal format or read-modify-write in a compute pass.

## 3. Alternatives
- **DBuffer decals** (UE): render decals into separate decal buffers after a depth prepass, consumed by the
  base pass; works with forward shading and baked lighting.
- **Clustered decals** (forward+): put decal boxes into the light cluster grid; each pixel loops its decal list
  in the main shader, sampling from an atlas or bindless textures. No extra G-buffer traffic, correct blending
  of any attribute.

## Gotchas
- Stretching on surfaces parallel to the projection axis: fade by `dot(surfaceNormal, decalAxis)` (normal from
  G-buffer).
- Per-RT blend: albedo blended but metallic untouched needs separate blend states or write masks per target.
- Mip selection breaks at box edges and depth discontinuities (UV derivatives jump): compute LOD from
  distance or use `textureGrad` with analytic derivatives.

## Verify
- [ ] Decal wraps across a corner of two walls without stretching; dynamic objects excluded via stencil; no
  shimmering mip seams at box boundaries.
