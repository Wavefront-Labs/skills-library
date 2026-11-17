---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-cameras-and-orbitcontrols
name: threejs-cameras-and-orbitcontrols
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, orbitcontrols, orthographiccamera, perspectivecamera, camera-controls]
level: practitioner
status: docs-checked
description: "Set up three.js PerspectiveCamera and OrthographicCamera with OrbitControls: resize handling, damping, limits, zoom-to-fit, and frustum sizing."
sources: ["https://github.com/mrdoob/three.js/blob/r186/examples/jsm/controls/OrbitControls.js", "https://github.com/mrdoob/three.js/blob/r186/src/cameras/Camera.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/cameras.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js cameras and OrbitControls

## 1. Perspective + OrbitControls
```js
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 1000);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;          // requires controls.update() every frame
controls.target.set(0, 1, 0);
controls.minDistance = 2; controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI * 0.49; // stop going under the floor
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
```
Depth precision depends on the near/far range: do not set `near` smaller than the scene needs.

## 2. Orthographic
```js
const frustum = 10;                      // world units visible vertically
const cam = new THREE.OrthographicCamera(-frustum * aspect / 2, frustum * aspect / 2,
                                         frustum / 2, -frustum / 2, 0.1, 100);
```
OrbitControls zoom on an ortho camera changes `camera.zoom`, not distance; `minZoom`/`maxZoom`
limit it.

## 3. Resize
```js
function onResize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  renderer.setSize(w, h, false);
  if (camera.isPerspectiveCamera) camera.aspect = w / h;
  else { camera.left = -frustum * w / h / 2; camera.right = frustum * w / h / 2; }
  camera.updateProjectionMatrix();
}
```
Always call `updateProjectionMatrix()` after changing fov, aspect, near, far, zoom or bounds.

## 4. Zoom to fit an object
```js
const box = new THREE.Box3().setFromObject(obj), size = box.getSize(new THREE.Vector3());
const centre = box.getCenter(new THREE.Vector3());
const dist = (Math.max(size.x, size.y, size.z) / 2) / Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
camera.position.copy(centre).add(new THREE.Vector3(0, 0, dist * 1.3));
controls.target.copy(centre); controls.update();
```

## Gotchas
- Damping without `controls.update()` in the loop makes the controls feel dead.
- With render-on-demand, listen to `controls.addEventListener('change', render)`.
- Setting `camera.lookAt` is overridden by OrbitControls; move `controls.target` instead.

## Verify
- [ ] Resize the window: no stretching; ortho and perspective both keep proportions.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), OrbitControls.js and Camera.js source.
Confirmed: `enableDamping` and `autoRotate` need `update()` in the loop; `target`, `minDistance`, `maxPolarAngle`,
`minZoom`/`maxZoom` exist; on an orthographic camera `update()` and dolly change `camera.zoom`; `update()` calls
`lookAt(target)` so a manual `camera.lookAt` is overridden; the controls dispatch a `change` event; a camera looks down
its local negative z axis. The zoom-to-fit arithmetic is plain trigonometry (distance = half size / tan(half fov)).

Method: documentation only; no commands were run.
