---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-scene-setup-and-performance
name: threejs-scene-setup-and-performance
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [threejs, three-js, webgl, webgl2, webgpu, javascript, scene-graph, perspectivecamera, webglrenderer, meshstandardmaterial, pbr, gltf, gltfloader, draco, ktx2, basis, instancedmesh, draw-calls, dispose, memory-leaks, colour-management, srgb, tone-mapping, devicepixelratio, r3f, react-three-fiber, spector-js]
level: practitioner
status: docs-checked
description: "Build a Three.js scene that looks right and runs at 60 fps: renderer and colour setup, resize/pixel ratio, glTF with Draco/KTX2, instancing, disposal, and profiling draw calls."
sources: ["https://threejs.org/docs/", "https://discoverthreejs.com/tips-and-tricks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Three.js scene setup and performance

**Goal:** a browser 3D scene with correct colour, crisp but affordable resolution,
compressed assets and a draw-call budget that holds 60 fps on mid-range laptops and phones.
Three.js API details drift between releases (`r1xx`); check the migration guide for
your version.

## 1. Baseline setup
```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const canvas = document.querySelector('#c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));   // 3x phones: 2.25x the pixels of 2x for little visible gain
renderer.outputColorSpace = THREE.SRGBColorSpace;               // documented default
renderer.toneMapping = THREE.ACESFilmicToneMapping;             // or AgXToneMapping / NeutralToneMapping
renderer.shadowMap.enabled = true;

const scene  = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 200);    // keep near/far ratio modest: z-fighting
function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== Math.floor(w * renderer.getPixelRatio())) {
    renderer.setSize(w, h, false);                              // false: CSS controls display size
    camera.aspect = w / h; camera.updateProjectionMatrix();
  }
}
renderer.setAnimationLoop((t) => { resize(); renderer.render(scene, camera); });
```
- Lighting for PBR (`MeshStandardMaterial`/`MeshPhysicalMaterial`): an **environment map**
  (`HDRLoader` (RGBE .hdr) + `PMREMGenerator`, or `RoomEnvironment`) does most of the work; add one
  directional light for shadows. Without an environment, metals look black.
- Colour: colour/albedo textures must be tagged `texture.colorSpace = THREE.SRGBColorSpace`;
  normal/roughness/metalness maps stay linear (`Texture.colorSpace` defaults to `NoColorSpace`). Washed-out or too-dark scenes are almost always colour-space mistakes.

## 2. Assets: glTF, compressed
```js
const draco = new DRACOLoader().setDecoderPath('/draco/');
const ktx2  = new KTX2Loader().setTranscoderPath('/basis/').detectSupport(renderer);
const loader = new GLTFLoader().setDRACOLoader(draco).setKTX2Loader(ktx2);
const gltf = await loader.loadAsync('/models/scene.glb');
scene.add(gltf.scene);
```
- Pipeline: export `.glb` from Blender, then compress geometry (Draco) and textures (KTX2) with an offline glTF optimiser, and resize textures.
- **Why KTX2:** a 2048² PNG is small on disk but about **16 MB in GPU memory** uncompressed
  (2048 x 2048 x 4 bytes, roughly 1.33x with mipmaps); KTX2/Basis textures stay compressed on the GPU.

## 3. Performance budget
Check `renderer.info.render.calls` and `.triangles` each frame in dev.
- Set draw-call and triangle budgets by measuring on your target devices. Every mesh x material is a
  draw call; each shadow-casting light adds passes.
- Many copies of one object → `THREE.InstancedMesh` (one draw call for thousands; per-instance
  matrix and colour). Different static meshes sharing a material →
  `BufferGeometryUtils.mergeGeometries`, or `BatchedMesh` in recent versions.
- Shadows: limit casters, keep the shadow map modest, fit the shadow camera tightly to
  the scene; consider baked lightmaps/AO for static scenes.
- Post-processing passes each cost a full-screen pass — budget them on mobile.
- Render on demand (only when something changes) for configurators and viewers: saves
  battery and heat.
- Avoid allocating `new Vector3()` etc. inside the loop; reuse temporaries.

## 4. Memory: dispose explicitly
GPU resources aren't garbage collected. When removing objects:
```js
obj.traverse((o) => {
  if (o.geometry) o.geometry.dispose();
  if (o.material) [].concat(o.material).forEach((m) => {
    for (const k in m) if (m[k] && m[k].isTexture) m[k].dispose();
    m.dispose();
  });
});
```
Watch `renderer.info.memory.geometries/textures` — they should return to baseline after
navigating away from a scene (critical in SPAs).

## Gotchas
- Blended transparency has sorting artefacts; `alphaTest` or `alphaHash` (Material docs) avoid them for foliage.
- Large world coordinates jitter due to float precision; keep the action near the origin.
- Profile with the browser's DevTools Performance panel and `renderer.info`.

## Verify
- [ ] Albedo textures in sRGB; scene looks the same as in Blender's viewport with the same HDRI.
- [ ] Pixel ratio capped at 2; canvas resizes without stretching.
- [ ] Draw calls and triangles within your measured budget on a real mid-range phone.
- [ ] Assets compressed (Draco/Meshopt + KTX2); total download size known.
- [ ] `renderer.info.memory` returns to baseline after unloading.

## Checked
2026-11-01. Confirmed against the three.js docs source (`docs/pages`): `WebGLRenderer` `outputColorSpace` (default `SRGBColorSpace`), `toneMapping` values, `setPixelRatio`, `setAnimationLoop`, `info` (`render.calls`, `memory.geometries`/`textures`); `GLTFLoader` `setDRACOLoader`/`setKTX2Loader`/`loadAsync`; `DRACOLoader.setDecoderPath`; `KTX2Loader` `setTranscoderPath`/`detectSupport`; `BufferGeometryUtils.mergeGeometries`; `BatchedMesh`, `HDRLoader`, `RoomEnvironment`, `PMREMGenerator`; `dispose()` on Texture, BufferGeometry, Material; `Texture.colorSpace`; `Material.alphaHash`/`alphaTest`. The 16 MB figure is arithmetic. Removed unconfirmed: draw-call and triangle targets, compression ratio, texture size caps, shadow map sizes, float-jitter distances, glTF loader colour-space claim, gltf-transform command line, WebGPU and Spector.js remarks, transparency-sorting detail.
Method: documentation only; no commands were run.
