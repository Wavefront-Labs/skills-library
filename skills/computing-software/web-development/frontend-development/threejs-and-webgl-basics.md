---
id: computing-software.web-development.frontend-development.threejs-and-webgl-basics
name: threejs-and-webgl-basics
category: computing-software
field: web-development
product: frontend-development
tags: [threejs, webgl, gltf, webglrenderer, 3d-graphics, react-three-fiber]
level: practitioner
status: draft
description: "Setting up a Three.js scene correctly: renderer, camera, resize and pixel ratio, glTF/Draco loading, animation loop, disposal, context loss and draw-call performance."
sources:
  - https://threejs.org/manual/#en/fundamentals
  - https://threejs.org/docs/#examples/en/loaders/GLTFLoader
  - https://threejs.org/manual/#en/how-to-dispose-of-objects
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three.js and WebGL basics

## 1. Skeleton
```js
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js";

const canvas = document.querySelector("#scene");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));          // cap: 3x DPR = 9x fragments
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(0, 1.5, 4);
scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 2));
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;

const draco = new DRACOLoader().setDecoderPath("/draco/");
const gltf = await new GLTFLoader().setDRACOLoader(draco).loadAsync("/models/chair.glb");
scene.add(gltf.scene);

function resize() {
  const { clientWidth: w, clientHeight: h } = canvas;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(canvas);
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
```
Size the canvas with CSS and pass `false` to `setSize` so Three.js does not overwrite the CSS size.

## 2. Assets
- Use glTF/GLB; compress geometry with Draco or meshopt (`gltf-transform optimize in.glb out.glb --compress draco --texture-compress webp`).
- Textures: power-of-two not required in WebGL2 but keep sizes sane (2048 max for mobile); KTX2/Basis for GPU-compressed textures.
- Colour: r152+ defaults to sRGB output; set `texture.colorSpace = THREE.SRGBColorSpace` on colour maps you load manually.

## 3. Performance
- Draw calls dominate: merge static geometry, use `InstancedMesh` for repeated objects; check `renderer.info.render.calls`.
- Render on demand for static viewers (render only on `controls` change) instead of a constant loop.
- Stop the loop when the canvas is off-screen (IntersectionObserver) or the tab hidden.

## 4. Cleanup and failure
```js
geometry.dispose(); material.dispose(); texture.dispose(); renderer.dispose();
canvas.addEventListener("webglcontextlost", e => { e.preventDefault(); showFallback(); });
```
GPU memory is not garbage-collected; SPAs that mount/unmount scenes leak without dispose. React: `@react-three/fiber` handles disposal and the loop declaratively.

## Gotchas
- Nothing visible: camera inside the model, near/far planes wrong, or no light with `MeshStandardMaterial`.
- `three/addons/...` paths need a bundler or import map mapping `three/addons/` to `examples/jsm/`.
- WebGPU: `three/webgpu` `WebGPURenderer` falls back to WebGL2; test both.

## Verify
- [ ] `renderer.info.memory` counts return to baseline after unmounting the scene.
- [ ] 60 fps on a mid-range phone with DPR capped.
