---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-fxaa-smaa-taa-passes
name: threejs-fxaa-smaa-taa-passes
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-postprocessing, smaapass, taarenderpass, fxaa, anti-aliasing, msaa-render-target]
level: practitioner
status: draft
description: "Restore anti-aliasing when using three.js EffectComposer: MSAA render targets, SMAAPass, FXAA ShaderPass, TAARenderPass for static scenes, and pass ordering."
sources: ["https://threejs.org/docs/#examples/en/postprocessing/SMAAPass", "https://threejs.org/examples/#webgl_postprocessing_smaa", "https://threejs.org/examples/#webgl_postprocessing_taa", "https://threejs.org/examples/#webgl_postprocessing_fxaa"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anti-aliasing passes in three.js

`new WebGLRenderer({ antialias: true })` only anti-aliases the default framebuffer. With
EffectComposer the scene renders into render targets, so edges become jagged.

## 1. MSAA render target (best for geometry edges)
```js
const rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
```
WebGL2 only; costs memory bandwidth; does nothing for shader aliasing (specular sparkle).

## 2. SMAA
```js
import { SMAAPass } from 'three/addons/postprocessing/SMAAPass.js';
composer.addPass(new SMAAPass(w * renderer.getPixelRatio(), h * renderer.getPixelRatio()));
```
Good quality morphological AA, ~1 ms. Place after tone mapping (after OutputPass), because edge
detection works on display-referred colours.

## 3. FXAA
```js
import { FXAAShader } from 'three/addons/shaders/FXAAShader.js';
const fxaa = new ShaderPass(FXAAShader);
fxaa.material.uniforms.resolution.value.set(1 / (w * dpr), 1 / (h * dpr));
composer.addPass(fxaa);   // last, after OutputPass
```
Cheapest; blurs textures and text slightly.

## 4. TAARenderPass (static camera, accumulation)
Jitters the camera and accumulates frames: superb for configurators while idle.
`taa.sampleLevel = 2..5`, `taa.accumulate = true` when the camera stops; replace RenderPass with it.
Not a motion-aware TAA: moving scenes ghost unless `accumulate = false`.

## 5. Choosing
Desktop: MSAA 4x target + optional SMAA. Mobile: FXAA or SMAA at pixel ratio 1.5-2. Product
viewer idle: TAA accumulation. High DPR (3x) phones often need none.

## Gotchas
- Resize: update SMAA size and FXAA resolution uniform with pixel ratio.
- AA before tone mapping (on HDR) causes bright-edge aliasing to persist; order matters.
- WebGPURenderer: use the TSL `fxaa()`/`smaa()`/`traa()` nodes in `PostProcessing`.

## Verify
- [ ] Zoomed screenshot of thin diagonal edges shows smooth stair-steps after the pass.
- [ ] Text/UI textures not visibly blurred.
