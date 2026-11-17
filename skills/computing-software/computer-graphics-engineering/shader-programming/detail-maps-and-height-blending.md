---
id: computing-software.computer-graphics-engineering.shader-programming.detail-maps-and-height-blending
name: detail-maps-and-height-blending
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, detail-maps, height-blend, texture-blending, normal-blending, rnm, vertex-painting, terrain-shading]
level: practitioner
status: draft
description: "Layer detail maps and blend materials by height: detail albedo/normal at high tiling, reoriented normal blending, height-based layer blending and vertex-colour masks."
sources: ["https://blog.selfshadow.com/publications/blending-in-detail/", "https://www.gamedeveloper.com/programming/advanced-terrain-texture-splatting", "https://docs.unity3d.com/Manual/StandardShaderMaterialParameterDetail.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detail maps and texture blending

## 1. Detail maps
A detail map adds high-frequency variation at a much higher tiling than the base, so surfaces hold
up close without huge textures.
```glsl
vec3 base   = texture(albedo, uv).rgb;
vec3 detail = texture(detailAlbedo, uv * detailTiling).rgb;
vec3 col    = base * detail * 2.0;                 // "overlay x2": detail authored around 0.5 grey
col = mix(base, col, detailMask);                  // fade by mask and by distance
```
Fade detail out with distance or rely on mips averaging to 0.5 grey (author it that way).

## 2. Blending normal maps
Do not average normals. Use Reoriented Normal Mapping (Barre-Brisebois & Hill):
```glsl
vec3 blendRNM(vec3 n1, vec3 n2) {      // inputs in [0,1] texture space
    vec3 t = n1 * vec3( 2,  2, 2) + vec3(-1, -1,  0);
    vec3 u = n2 * vec3(-2, -2, 2) + vec3( 1,  1, -1);
    return normalize(t * dot(t, u) - u * t.z);
}
```
Whiteout (`normalize(vec3(n1.xy + n2.xy, n1.z * n2.z))`) is cheaper and close enough for detail.

## 3. Height-based layer blending
Linear blending of two materials makes muddy transitions. Use per-layer height maps so the
"higher" material wins, with a soft band:
```glsl
float h1 = texture(height1, uv).r + (1.0 - w);      // w = painted weight of layer 2
float h2 = texture(height2, uv).r + w;
float depth = 0.2;                                  // transition softness
float ma = max(h1, h2) - depth;
float b1 = max(h1 - ma, 0.0), b2 = max(h2 - ma, 0.0);
vec3 col = (c1 * b1 + c2 * b2) / (b1 + b2);
```
Masks come from vertex colours (cheap, painted in DCC), a splat map (terrain) or world-space
rules (slope, height).

## Gotchas
- Detail normal tangent frames must match the base UV set; if detail uses a different UV channel,
  you need its tangents too.
- Height blend weights must be normalised for more than two layers.
- Sampling 4+ layers x 3 maps each is texture-fetch heavy; pack (albedo+height, normal+roughness+AO)
  and use texture arrays.

## Verify
- [ ] Close-up shows detail; at distance no tiling repetition or shimmer.
- [ ] Layer transitions follow height (stones poke through sand), not a smooth crossfade.
