---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-tsl-node-materials
name: threejs-tsl-node-materials
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webgpurenderer, tsl, three-shading-language, nodematerial, meshstandardnodematerial, colornode, positionnode, uniform-nodes, wgsl, glsl, tsl-fn, tsl-uniforms]
level: advanced
status: docs-checked
description: "Write three.js materials in TSL (Three Shading Language) for WebGPURenderer: node materials, colorNode/positionNode hooks, uniforms, Fn functions."
sources: ["https://github.com/mrdoob/three.js/blob/r186/docs/pages/TSL.html.md", "https://github.com/mrdoob/three.js/blob/r186/src/materials/nodes/NodeMaterial.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/nodes/MeshStandardNodeMaterial.js", "https://github.com/mrdoob/three.js/blob/r186/src/nodes/tsl/TSLCore.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/common/Renderer.js"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# three.js TSL node materials

**Goal:** custom shading that runs on WebGPU and falls back to WebGL2 from one JavaScript
source, while keeping PBR lighting, shadows and fog of the built-in materials.

## 1. Setup
```js
import * as THREE from 'three/webgpu';
import { Fn, uniform, texture, uv, time, positionLocal, normalLocal, normalView, positionViewDirection, sin, mix, color, vec3 } from 'three/tsl';
const renderer = new THREE.WebGPURenderer({ antialias: true });
await renderer.init();                          // async: picks WebGPU or WebGL2 backend
```

## 2. Hook into a node material
```js
const mat = new THREE.MeshStandardNodeMaterial();
const uTint = uniform(new THREE.Color(0x44aaff));
const uAmp  = uniform(0.2);
mat.colorNode = mix(texture(albedoTex, uv()).rgb, uTint, 0.3);       // base colour
mat.positionNode = positionLocal.add(normalLocal.mul(sin(time.add(positionLocal.y.mul(4))).mul(uAmp)));
mat.roughnessNode = texture(ormTex).g;
mat.emissiveNode = color(0xff5500).mul(sin(time).mul(0.5).add(0.5));
uAmp.value = 0.4;                               // update from JS, no recompile
```
Other slots: `normalNode`, `metalnessNode`, `opacityNode`, `alphaTestNode`, `outputNode`
(post-lighting), `fragmentNode` (replace everything), `vertexNode`.

## 3. Functions
```js
const fresnel = Fn(([power]) => {
  const nDotV = normalView.dot(positionViewDirection).saturate();
  return nDotV.oneMinus().pow(power);
});
mat.emissiveNode = color(0x00ffff).mul(fresnel(3.0));
```
Use `.toVar()` for mutable variables, `If()`/`Loop()` for control flow — native JS `if`
runs at graph-build time, not on the GPU.

## 4. Debugging generated code
`await renderer.debug.getShaderAsync(scene, camera, mesh)` returns the generated shader code; the graph compiles to
WGSL (WebGPU backend) or GLSL (WebGL 2 backend).

## Gotchas
- Import from `three/webgpu` and `three/tsl` (the manual recommends an import map pointing `three` at `three.webgpu.js`)
  so only one copy of the library loads.
- `ShaderMaterial`/`onBeforeCompile` don't work with WebGPURenderer; port to TSL.
- API is evolving across releases (renamed nodes); pin the three version and check the TSL wiki
  for the release you use.
- In r186 `renderer.render()` before `init()` has completed throws; use `renderer.setAnimationLoop`, which waits for init.

## Verify
- [ ] Same scene renders identically with `forceWebGL: true` and with WebGPU.
- [ ] Uniform changes animate without shader recompiles (no hitch).
- [ ] Shadows/fog still apply to the custom node material.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), TSL documentation page and source of the files in `sources`.
Confirmed: the node slots `colorNode`, `normalNode`, `opacityNode`, `alphaTestNode`, `positionNode`, `outputNode`, `fragmentNode`,
`vertexNode` (NodeMaterial) and `emissiveNode`, `metalnessNode`, `roughnessNode` (MeshStandardNodeMaterial); TSL exports
`Fn`, `uniform`, `texture`, `uv`, `time`, `positionLocal`, `normalLocal`, `normalView`, `positionViewDirection`, `sin`, `mix`,
`color`, `vec3`, `oneMinus`, `saturate`, `pow`, `dot`, `If`, `Loop`; `.toVar()` exists; `renderer.debug.getShaderAsync`;
`ShaderMaterial` and `onBeforeCompile` are unsupported with WebGPURenderer (manual); `render()` before `init()` throws.

Method: documentation only; no commands were run.
