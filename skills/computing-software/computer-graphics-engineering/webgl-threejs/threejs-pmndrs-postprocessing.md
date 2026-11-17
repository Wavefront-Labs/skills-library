---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-pmndrs-postprocessing
name: threejs-pmndrs-postprocessing
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-postprocessing, pmndrs-postprocessing, effectpass, selective-bloom, smaa]
level: practitioner
status: draft
description: "Use the pmndrs postprocessing library with three.js: EffectComposer, merged EffectPass, bloom, SMAA, tone mapping, and why it beats chained three.js passes."
sources: ["https://github.com/pmndrs/postprocessing", "https://pmndrs.github.io/postprocessing/public/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pmndrs postprocessing

## 1. Setup
```js
import { EffectComposer, RenderPass, EffectPass, BloomEffect, SMAAEffect,
         ToneMappingEffect, ToneMappingMode, VignetteEffect } from 'postprocessing';
const renderer = new THREE.WebGLRenderer({ powerPreference: 'high-performance',
  antialias: false, stencil: false, depth: false });
const composer = new EffectComposer(renderer, { frameBufferType: THREE.HalfFloatType });
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new EffectPass(camera,
  new BloomEffect({ luminanceThreshold: 0.9, intensity: 1.2, mipmapBlur: true }),
  new ToneMappingEffect({ mode: ToneMappingMode.AGX }),
  new VignetteEffect()));
composer.addPass(new EffectPass(camera, new SMAAEffect()));   // AA after tone mapping
renderer.setAnimationLoop(() => composer.render());
```
On resize: `composer.setSize(w, h)`.

## 2. Why it is faster
`EffectPass` merges compatible effects into one fullscreen shader: one read and write of the
frame instead of one per pass, as with the three.js addon composer.

## 3. Rules
- Turn off renderer MSAA (`antialias: false`); use SMAA/FXAA effects or
  `multisampling: 4` on the composer for MSAA on the scene render.
- Set `renderer.toneMapping = NoToneMapping` and tone map in the effect chain, or highlights
  clip before bloom.
- Effects that need convolution (SMAA, some blurs) cannot merge with others; give them their own pass.
- Selective bloom: `SelectiveBloomEffect` with a selection set, or emissive above threshold.

## Gotchas
- Mixing addon passes (`three/addons/postprocessing`) with pmndrs composer does not work.
- HalfFloat buffers are needed for HDR bloom; 8-bit clamps highlights.
- React: `@react-three/postprocessing` wraps this library.

## Verify
- [ ] Spector.js capture shows one fullscreen draw per EffectPass.
