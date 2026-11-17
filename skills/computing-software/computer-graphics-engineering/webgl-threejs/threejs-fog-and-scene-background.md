---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-fog-and-scene-background
name: threejs-fog-and-scene-background
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, three-fog, scene-background, fogexp2, background-blurriness, depth-cueing]
level: practitioner
status: docs-checked
description: "Set three.js scene backgrounds (colour, texture, equirect, blurred env) and Fog/FogExp2 so distant objects fade into the background without seams."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/scenes/Scene.js", "https://github.com/mrdoob/three.js/blob/r186/src/scenes/Fog.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/shaders/ShaderChunk/fog_vertex.glsl.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLBackground.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/fog.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js fog and scene background

## 1. Background options
```js
scene.background = new THREE.Color(0x87ceeb);            // flat colour (cheapest)
scene.background = cubeTexture;                           // CubeTextureLoader skybox
hdr.mapping = THREE.EquirectangularReflectionMapping;
scene.background = hdr;  scene.environment = hdr;         // same HDRI lights and shows
scene.backgroundBlurriness = 0.4;                         // 0..1, environment-map backgrounds only
scene.backgroundIntensity = 0.8;
scene.backgroundRotation.y = Math.PI / 2;                 // Euler; environmentRotation also exists
```
Transparent canvas over HTML: `new WebGLRenderer({ alpha: true })`, leave `scene.background = null`,
`renderer.setClearColor(0x000000, 0)`.

## 2. Fog
```js
scene.fog = new THREE.Fog(0xcce0ff, 10, 80);      // linear: near, far in view-space units
scene.fog = new THREE.FogExp2(0xcce0ff, 0.025);   // exponential-squared density
scene.background = new THREE.Color(0xcce0ff);     // MUST match fog colour or edges show
```
- Fog is applied per material in the fragment shader; `material.fog = false` opts out (sky
  domes, UI, emissive markers).
- Fog uses view depth, not radial distance, so objects at the screen edge fade slightly later.
- ShaderMaterial gets fog only with `fog: true` plus the `fog_pars_*`/`fog_fragment` chunks and
  `UniformsLib.fog` merged in.

## 3. Fog plus a skybox
A textured background ignores fog, so geometry fades to a flat colour against a detailed sky.
Fix: fade the horizon of the sky to the fog colour, use a gradient sky shader whose bottom
matches, or keep fog `far` beyond the visible content.

## Gotchas
- Fog `near` and `far` are distances from the camera: geometry closer than `near` is unfogged and geometry beyond `far`
  is the solid fog colour (`Fog` defaults are near 1, far 1000).
- `new THREE.Color(hex)` treats the hex as sRGB and converts to the linear working space while `ColorManagement` is enabled (the default).
- WebGPURenderer: use `scene.fogNode`/`fog()` TSL nodes or the classic Fog objects (supported).

## Verify
- [ ] Distant meshes blend into the background with no visible silhouette line.
- [ ] Sky/UI materials marked `fog: false` where they should not fade.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0) and the manual fog page.
Confirmed: `Fog(color, near = 1, far = 1000)`; fog depth is view-space `-mvPosition.z`; background materials are created with
`fog: false`; `backgroundBlurriness` range 0 to 1 and `backgroundIntensity`, `backgroundRotation`, `environmentRotation`
exist on Scene; the manual says fog and background colour should match; ShaderMaterial fog needs `fog: true` plus
`UniformsLib.fog`; WebGPURenderer reads `scene.fogNode` or `scene.fog` (NodeManager.js).

Method: documentation only; no commands were run.
