---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-effectcomposer-render-targets-and-passes
name: threejs-effectcomposer-render-targets-and-passes
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, effectcomposer, three-postprocessing, renderpass, shaderpass, outputpass, webglrendertarget, halffloattype, msaa-samples, custom-pass]
level: practitioner
status: docs-checked
description: "Set up three.js post-processing correctly: EffectComposer with RenderPass, ShaderPass and OutputPass, HDR half-float targets, MSAA samples."
sources: ["https://github.com/mrdoob/three.js/blob/dev/examples/jsm/postprocessing/EffectComposer.js", "https://github.com/mrdoob/three.js/blob/dev/examples/jsm/postprocessing/RenderPass.js", "https://github.com/mrdoob/three.js/blob/dev/examples/jsm/postprocessing/OutputPass.js", "https://github.com/mrdoob/three.js/blob/dev/src/core/RenderTarget.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js EffectComposer, render targets and passes

**Goal:** a post-processing chain with correct colour (tone mapping and sRGB applied once,
at the end), antialiasing, and custom effects.

## 1. Minimal correct chain
```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(myEffectPass);
composer.addPass(new OutputPass());          // tone mapping, LAST
renderer.setAnimationLoop(() => composer.render());
```
- EffectComposer's own default target is `HalfFloatType` (see its constructor).
- `samples` on the render target sets its MSAA sample count (default 0).
- `OutputPass` applies the renderer's tone mapping (OutputPass.js), so keep it last and tone map only once.

## 2. Custom ShaderPass
```js
const Vignette = {
  uniforms: { tDiffuse: { value: null }, strength: { value: 0.4 } },  // tDiffuse = previous pass
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float strength; varying vec2 vUv;
    void main(){ vec4 c = texture2D(tDiffuse, vUv);
      float d = distance(vUv, vec2(0.5)); c.rgb *= 1.0 - strength * d * d * 2.0; gl_FragColor = c; }`
};
const vignette = new ShaderPass(Vignette);
composer.addPass(vignette);                         // place before OutputPass (works in linear HDR)
```

## 3. Resize and pixel ratio
```js
function onResize() {
  renderer.setSize(w, h); composer.setSize(w, h);
  composer.setPixelRatio(renderer.getPixelRatio());
}
```
Every pass costs per pixel, so cap the pixel ratio.

## 4. Render targets directly
For render-to-texture outside the composer (mirrors, minimaps, portals):
```js
renderer.setRenderTarget(rtMini); renderer.render(scene, topCam); renderer.setRenderTarget(null);
screenMat.map = rtMini.texture;
```
Don't sample a target while rendering into it (feedback loop → black/undefined).

## Verify
- [ ] Colours with composer match `renderer.render` without effects (OutputPass present once).
- [ ] No banding in dark gradients (HalfFloat targets).
- [ ] GPU time per pass measured on target devices.

## Checked

2026-10-28. Confirmed: `EffectComposer(renderer, renderTarget)` with default `HalfFloatType` target, `setSize` / `setPixelRatio` (EffectComposer.js); `OutputPass` applies `toneMapping` (OutputPass.js); render-target `samples` option (RenderTarget.js).
Removed (not in the fetched pages): r153 version gate, bloom/banding claim about UnsignedByte, double tone-mapping claim, `Math.min(devicePixelRatio, 2)`, 4K/mobile pass-count claim, "toneMapping ignored in render targets", pmndrs speed claim, Spector.js, dead manual and docs links. ShaderPass vignette code is an illustrative sketch.

Method: documentation only; no commands were run.
