---
id: computing-software.computer-graphics-engineering.shader-programming.parallax-occlusion-mapping
name: parallax-occlusion-mapping
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shaders, material-effects, parallax-occlusion-mapping, pom, height-map, tangent-space, parallax-mapping, self-shadowing, relief-mapping]
level: advanced
status: draft
description: "Add depth to flat surfaces with parallax occlusion mapping: tangent-space view rays, adaptive layer counts, linear+binary refinement, self-shadowing, and silhouette/LOD limits."
sources: ["https://learnopengl.com/Advanced-Lighting/Parallax-Mapping", "https://developer.amd.com/wordpress/media/2012/10/Tatarchuk-ParallaxOcclusionMapping-Sketch-print.pdf", "https://advances.realtimerendering.com/s2006/Tatarchuk-POM.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parallax occlusion mapping

**Goal:** bricks, cobblestones and tiles that show convincing depth and self-occlusion at
grazing angles, without adding geometry.

## 1. View ray in tangent space
Vertex shader passes TBN; fragment computes tangent-space view direction:
```glsl
vec3 V = normalize(transpose(TBN) * (camPos - worldPos));   // tangent space, z = out of surface
```

## 2. Ray march the height field
```glsl
vec2 parallaxUV(vec2 uv, vec3 V) {
    float nLayers = mix(32.0, 8.0, abs(V.z));               // more layers at grazing angles
    float layerDepth = 1.0 / nLayers, cur = 0.0;
    vec2 dUV = (V.xy / V.z) * heightScale / nLayers;        // heightScale ~ 0.02-0.08
    vec2 dx = dFdx(uv), dy = dFdy(uv);                      // derivatives taken BEFORE the loop
    float h = 1.0 - textureGrad(depthMap, uv, dx, dy).r;    // depth = 1 - height
    while (cur < h) {
        uv -= dUV; cur += layerDepth;
        h = 1.0 - textureGrad(depthMap, uv, dx, dy).r;
    }
    // linear interpolation between last two layers (removes stair-stepping)
    vec2 prevUV = uv + dUV;
    float after = h - cur, before = (1.0 - textureGrad(depthMap, prevUV, dx, dy).r) - cur + layerDepth;
    float w = after / (after - before);
    return mix(uv, prevUV, w);
}
```
- Use `textureGrad` with derivatives from the original UV: `texture()` inside a
  data-dependent loop has undefined derivatives → mip noise/sparkles.
- Use the resulting UV for **all** material textures (albedo, normal, roughness).

## 3. Self-shadowing
March from the found point toward the light in tangent space; if height above the ray,
shadowed. Soft version: accumulate `max(heightAboveRay)` with falloff.

## 4. Limits and mitigation
- Silhouettes stay flat — POM can't change the mesh outline. Use real displacement
  (tessellation/mesh LOD) for edges and close-ups.
- UV seams and tiled UVs: offsets cross tile edges fine; atlas borders bleed — pad atlases.
- Discard fragments where UV leaves [0,1] only for decals/single-tile surfaces.
- Distance LOD: fade `heightScale` to 0 beyond ~10–20 m and skip the loop (plain normal map).

## Gotchas
- Wrong TBN handedness (bitangent sign) inverts the parallax direction — depth looks
  "inside out".
- Depth vs height map convention (white = high or low) — be consistent with the bake tool.
- Cost scales with layers × texture fetches; mobile: ≤ 8–16 layers or skip.

## Verify
- [ ] Grazing-angle view: no stair-stepping or swimming; correct occlusion of bricks.
- [ ] No sparkles at distance (textureGrad used).
- [ ] GPU timing with LOD fade on vs off.
