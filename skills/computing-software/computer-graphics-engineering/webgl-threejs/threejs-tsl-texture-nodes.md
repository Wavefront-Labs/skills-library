---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-tsl-texture-nodes
name: threejs-tsl-texture-nodes
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webgpu-tsl, texture-node, tsl, triplanar, storage-texture, cube-texture-node]
level: advanced
status: docs-checked
description: "Sample textures in three.js TSL: texture() with custom UVs and levels, triplanar mapping, cube and 3D textures, storage textures from compute, and swapping maps at runtime."
sources: ["https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Texture nodes in TSL

## 1. Sampling
```js
import { texture, uv, vec2, time, triplanarTexture, cubeTexture, texture3D, reflectVector } from 'three/tsl';
const t = texture(albedoTex);                         // samples at uv() by default
mat.colorNode = texture(albedoTex, uv().mul(4));      // tiling
mat.colorNode = texture(albedoTex, uv().add(vec2(time.mul(0.1), 0)));  // scrolling
const lod = texture(tex, uv(), 3);                    // texture(texture, uv = uv(), level = null)
const sz  = textureSize(texture(tex), 0);             // dimensions
```
Swizzle and math like any node: `texture(orm).g` for roughness.

## 2. Mapping helpers
- `triplanarTexture(texture(rock), null, null, float(0.5))` for terrain without UVs.
- `cubeTexture(envMap, reflectVector)` for reflections; `texture3D(volume, uvw)` for LUTs/volumes.
- `viewportSharedTexture(uvNode = screenUV)` accesses what has already been rendered (refraction, distortion); `viewportDepthTexture` and `viewportMipTexture` are listed too.

## 3. Storage textures
```js
const st = /* a storage texture: copy the class and constructor from your release's examples */;
const writeTex = Fn(() => {
  const x = instanceIndex.mod(512), y = instanceIndex.div(512);
  textureStore(st, uvec2(x, y), vec4(x.toFloat().div(512), y.toFloat().div(512), 0, 1));
})().compute(512 * 512);
renderer.compute(writeTex);
mat.colorNode = texture(st);
```

## Gotchas
- The TSL wiki lists `textureSize`, `textureLoad` (no interpolation) and `textureStore` (storage textures); check it for your release.

## Verify
- [ ] Compute-written storage texture displays correctly.

## Checked

2026-10-28. Confirmed in the three.js TSL wiki: `texture(texture, uv = uv(), level = null)`, `textureLoad`, `textureStore`, `textureSize`, `cubeTexture(texture, uvw = reflectVector, level)`, `texture3D`, `triplanarTexture(textureX, textureY, textureZ, scale, position, normal)`, `viewportSharedTexture`, `viewportDepthTexture`, `viewportMipTexture`, `compute`.
Removed (not in the fetched pages): `.level()` and `.grad()` methods, runtime `.value` texture swap, `StorageTexture` class name, `computeAsync`, `isWebGPUBackend`, colour-space and control-flow gotchas, dead example links.

Method: documentation only; no commands were run.
