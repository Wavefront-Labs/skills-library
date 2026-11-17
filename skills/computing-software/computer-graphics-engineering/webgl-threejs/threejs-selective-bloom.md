---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-selective-bloom
name: threejs-selective-bloom
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-postprocessing, unrealbloompass, selective-bloom, emissive, hdr-bloom, luminance-threshold, layers]
level: practitioner
status: draft
description: "Make only chosen objects glow in three.js: UnrealBloomPass parameters, HDR emissive with threshold 1 as the modern selective method, and the layer-based two-composer technique."
sources: ["https://threejs.org/examples/#webgl_postprocessing_unreal_bloom", "https://threejs.org/examples/#webgl_postprocessing_unreal_bloom_selective", "https://threejs.org/docs/#examples/en/postprocessing/UnrealBloomPass", "https://github.com/pmndrs/postprocessing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# three.js selective bloom

**Goal:** neon signs, lasers and UI highlights glow; the rest of the scene stays crisp.

## 1. UnrealBloomPass basics
```js
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
const bloom = new UnrealBloomPass(new THREE.Vector2(w, h), /*strength*/ 1.2, /*radius*/ 0.4, /*threshold*/ 1.0);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(bloom);
composer.addPass(new OutputPass());
```
- `threshold`: luminance above which pixels bloom; `strength`: intensity; `radius`: spread
  across the mip chain.
- Bloom runs on a mip chain at decreasing resolutions — cost mostly in the first levels.

## 2. Selective via HDR (preferred)
With a **HalfFloatType** composer target and `threshold = 1.0`, only pixels brighter than 1
bloom. Make glowing objects exceed 1:
```js
glowMat = new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0x00ffff, emissiveIntensity: 4 });
// or unlit: new THREE.MeshBasicMaterial({ color: new THREE.Color(0, 4, 4), toneMapped: false })
```
Regular lit surfaces stay below 1 (before tone mapping) and don't bloom. No extra scene
render — this is how pmndrs `postprocessing` `SelectiveBloomEffect`-free setups and R3F
`<Bloom luminanceThreshold={1} mipmapBlur />` work.
Requires tone mapping in OutputPass so >1 values compress nicely.

## 3. Selective via layers (when HDR threshold isn't possible)
The official selective example: render the scene twice.
1. Bloom composer: darken non-bloom objects (swap materials to black), render, bloom,
   `renderToScreen = false`.
2. Final composer: render scene normally, then a ShaderPass that adds the bloom texture.
Costs a second scene render and material swapping each frame — use only if bright
non-glowing surfaces (white snow under sun) must not bloom.

## 4. Mobile considerations
Lower resolution bloom (`bloom.resolution` / composer size half), fewer mips
(pmndrs `levels`), or skip bloom on low-tier devices.

## Gotchas
- 8-bit render targets clamp at 1.0: threshold-based selective bloom silently stops working.
- Bloom applied after OutputPass blooms tone-mapped LDR — wrong order, washed out.
- Transparent objects: bloom picks up their premultiplied colour; tune emissive.

## Verify
- [ ] Only intended objects glow in a scene with bright white non-glow surfaces.
- [ ] No banding in bloom halos (half-float targets).
- [ ] GPU cost of bloom pass measured at target resolution.
