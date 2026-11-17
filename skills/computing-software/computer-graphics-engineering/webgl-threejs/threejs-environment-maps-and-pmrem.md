---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-environment-maps-and-pmrem
name: threejs-environment-maps-and-pmrem
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-materials, pmrem, environment-map, pmremgenerator, ibl, cube-camera]
level: practitioner
status: docs-checked
description: "Prefilter environment maps with PMREMGenerator for three.js PBR materials: HDR/EXR loading, RoomEnvironment, CubeCamera for dynamic reflections, and costs."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/extras/PMREMGenerator.js", "https://github.com/mrdoob/three.js/blob/r186/src/cameras/CubeCamera.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/MeshStandardMaterial.js", "https://github.com/mrdoob/three.js/blob/r186/src/scenes/Scene.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/loaders/RGBELoader.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment maps and PMREM

## 1. What PMREM does
MeshStandard/Physical need a prefiltered radiance environment map (mip chain blurred per
roughness). `PMREMGenerator` builds it as a cube-UV atlas. The material docs say environment maps are internally pre-processed
with PMREMGenerator, so an equirectangular texture (with `EquirectangularReflectionMapping`) assigned to
`scene.environment` works without manual steps; doing it yourself gives control and reuse. `scene.environment`
does not overwrite a texture already set on a material's `envMap`.

## 2. Explicit generation
```js
const pmrem = new THREE.PMREMGenerator(renderer);
pmrem.compileEquirectangularShader();          // warm up before loading
const hdr = await new HDRLoader().loadAsync('venice.hdr');    // RGBELoader is a deprecated alias (r180); or EXRLoader
const env = pmrem.fromEquirectangular(hdr).texture;
hdr.dispose();
scene.environment = env;
material.envMap = env;                          // per-material override
material.envMapIntensity = 1.0;
```
Procedural studio light: `pmrem.fromScene(new RoomEnvironment(), 0.04).texture`.

## 3. Dynamic reflections
```js
const rt = new THREE.WebGLCubeRenderTarget(256, { type: THREE.HalfFloatType });
const cubeCam = new THREE.CubeCamera(0.1, 100, rt);
scene.add(cubeCam);
// occasionally: hide the reflective object, update, show
obj.visible = false; cubeCam.update(renderer, scene); obj.visible = true;
obj.material.envMap = pmrem.fromCubemap(rt.texture).texture;   // prefilter for rough materials
```
Six scene renders per update: do it on change or once every N frames, not every frame.

## 4. Sizes
The PMREM cube face size is one quarter of the equirect width, rounded down to a power of two (minimum 256).
`scene.backgroundBlurriness` (0 to 1) blurs an environment-map background.

## Gotchas
- Without an environment, metallic materials render nearly black.
- `fromEquirectangular` and `fromCubemap` take an optional `renderTarget` to reuse; dispose render targets you no longer
  need, and call `pmrem.dispose()` when finished with the generator.
- Background and environment can differ: a blurred photo background with a separate lighting HDR.

## Verify
- [ ] Roughness sweep (0 to 1 spheres) shows smooth blur progression, no banding.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: `fromEquirectangular`, `fromCubemap`, `fromScene(scene, sigma, near, far, options)` and `compileEquirectangularShader`
signatures and the face-size rule; `CubeCamera.update(renderer, scene)`; `envMapIntensity` and the PMREM pre-processing note
(MeshStandardMaterial.js); `scene.environment` semantics and `backgroundBlurriness` range (Scene.js); `RGBELoader` is a deprecated
alias of `HDRLoader` since r180.

Method: documentation only; no commands were run.
