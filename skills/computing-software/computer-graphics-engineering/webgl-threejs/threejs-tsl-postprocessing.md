---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-tsl-postprocessing
name: threejs-tsl-postprocessing
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webgpu-tsl, tsl-postprocessing, webgpurenderer, pass-node, bloom-node]
level: advanced
status: docs-checked
description: "Build post-processing for three.js WebGPURenderer with TSL nodes: RenderPipeline, pass(), MRT outputs and custom node effects."
sources: ["https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-processing with TSL nodes

EffectComposer does not work with WebGPURenderer; post effects are a node graph.

## 1. Basic chain
```js
import * as THREE from 'three/webgpu';
import { pass, mrt, output, emissive, renderOutput, gaussianBlur } from 'three/tsl';

const post = new THREE.RenderPipeline(renderer);   // the class the current TSL wiki documents
const scenePass = pass(scene, camera);
const color = scenePass.getTextureNode('output');
post.outputNode = renderOutput(gaussianBlur(color, 4));  // renderOutput applies the renderer output settings
renderer.setAnimationLoop(() => post.render());    // instead of renderer.render
```
`renderOutput(node, targetColorSpace, targetToneMapping)` applies the renderer's output settings inside the graph; see the wiki for when to place it relative to other effects.

## 2. MRT for selective effects
```js
scenePass.setMRT(mrt({ output, emissive }));
const glow = gaussianBlur(scenePass.getTextureNode('emissive'), 4);
post.outputNode = scenePass.getTextureNode('output').add(glow);
```
Only the emissive output is blurred and added back. The wiki's MRT example also captures `normalView` and `velocity`.

## 3. Custom effect
```js
import { Fn, uv, vec4, screenUV, float } from 'three/tsl';
const vignette = Fn(([c]) => c.mul(float(1).sub(screenUV.sub(0.5).length().mul(1.2)).clamp(0, 1)));
post.outputNode = vignette(color);
```

## Gotchas
- Effect imports and names move between releases; pin the version and copy from that release's examples.
- `post.render()` replaces `renderer.render`; calling both renders twice.

## Verify
- [ ] Output matches the EffectComposer version visually (tone mapping applied once).
- [ ] GPU time per effect measured.

## Checked

2026-10-28. Confirmed in the three.js TSL wiki: `RenderPipeline(renderer)` with `.outputNode` and `.render()`, `pass(scene, camera)`, `getTextureNode('output')`, `setMRT(mrt({...}))`, `renderOutput(node, targetColorSpace, targetToneMapping)`, `gaussianBlur`, `normalView`, `velocity`, `screenUV`.
Removed (not in the fetched pages): `PostProcessing` class name (wiki now says RenderPipeline), bloom/FXAA addon import paths, `outputColorTransform`, `forceWebGL`, `trackTimestamp`, the node list, `.sample` usage, dead example links.

Method: documentation only; no commands were run.
