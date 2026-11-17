---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-debug-helpers-and-lil-gui
name: threejs-debug-helpers-and-lil-gui
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, axeshelper, lil-gui, camerahelper, debug-ui, light-helpers]
level: practitioner
status: docs-checked
description: "Debug three.js scenes with AxesHelper, GridHelper, light/camera/box helpers and a lil-gui panel bound to live uniforms and material settings."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/helpers/AxesHelper.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/helpers/VertexNormalsHelper.js", "https://github.com/georgealways/lil-gui/blob/main/src/GUI.js", "https://github.com/georgealways/lil-gui/blob/main/src/utils/getColorFormat.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js debug helpers and lil-gui

## 1. Helpers worth adding first
```js
scene.add(new THREE.AxesHelper(2));                    // X red, Y green, Z blue
scene.add(new THREE.GridHelper(20, 20));
scene.add(new THREE.DirectionalLightHelper(sun, 1));
scene.add(new THREE.CameraHelper(sun.shadow.camera));  // shadow frustum
scene.add(new THREE.SpotLightHelper(spot));
scene.add(new THREE.BoxHelper(mesh, 0xffff00));        // call .update() after moves
import { VertexNormalsHelper } from 'three/addons/helpers/VertexNormalsHelper.js';
scene.add(new VertexNormalsHelper(mesh, 0.1));
```
Helpers for lights must be `update()`d when the light or its target moves; put them on a
dedicated layer or a `debug` group so they can be toggled in one line.

## 2. lil-gui (the dat.gui successor)
```js
import GUI from 'lil-gui';               // also three/addons/libs/lil-gui.module.min.js
const gui = new GUI();
gui.add(mat, 'roughness', 0, 1, 0.01);
gui.add(mat, 'wireframe');
gui.addColor({ c: mat.color.getHex() }, 'c').onChange(v => mat.color.set(v));
gui.add(uniforms.uAmp, 'value', 0, 2).name('amplitude');
gui.add(renderer, 'toneMappingExposure', 0, 3);
const f = gui.addFolder('Shadows'); f.add(sun.shadow, 'bias', -0.01, 0.01, 0.0001); f.close();
gui.onFinishChange(() => mat.needsUpdate = true);  // for settings that change shader defines
```
Show only in dev: `if (location.hash === '#debug')`, or `gui.hide()`.

## 3. Changes that need extra work
- Toggling `flatShading`, `vertexColors`, `transparent`, fog, or swapping maps on/off changes
  the shader program: set `material.needsUpdate = true`.
- Changing a light's `castShadow` at runtime may require the same on receiving materials.
- `gui.addColor(mat, 'color')` works on a `THREE.Color` because lil-gui accepts `{ r, g, b }` objects, but it edits
  the linear working-space channels directly; the hex round-trip shown above converts via `Color.set`.

## Gotchas
- Helpers render with the scene, so they cast into post-processing and picking; exclude them
  from raycasts (`raycaster.layers`) and from exports.
- `CameraHelper` on the main camera is invisible from that camera; view it from a second camera.
- Remove the GUI (`gui.destroy()`) when unmounting in SPAs.

## Verify
- [ ] Axes match expectations (Y up, -Z forward for cameras).
- [ ] Every GUI control visibly changes the scene without console errors.

## Checked

Checked 2026-10-25 against three.js r186 and lil-gui 0.21.0 (main branch source).
Confirmed: AxesHelper colours (X red, Y green, Z blue); `VertexNormalsHelper(object, size, color)` signature;
`update()` exists on BoxHelper, DirectionalLightHelper, SpotLightHelper and CameraHelper; `three/addons/libs/lil-gui.module.min.js`
and `stats.module.js` ship in `examples/jsm/libs`; lil-gui `addColor` accepts hex numbers, CSS strings, arrays and
`{ r, g, b }` objects; `onFinishChange`, `hide`, `close` and `destroy` exist; a camera looks down negative z.

Method: documentation only; no commands were run.
