---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-cascaded-shadow-maps
name: threejs-cascaded-shadow-maps
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-shadows, three-csm, cascaded-shadow-maps, directional-shadows]
level: advanced
status: docs-checked
description: "Add cascaded shadow maps to a three.js scene with the CSM addon: cascade count, split mode, light margin, material setup and fade between cascades."
sources: ["https://github.com/mrdoob/three.js/blob/dev/examples/jsm/csm/CSM.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cascaded shadow maps in three.js

**Goal:** sharp sun shadows near the camera and coverage to the horizon, which a single
directional shadow map cannot do.

## 1. Setup
```js
import { CSM } from 'three/addons/csm/CSM.js';
renderer.shadowMap.enabled = true;
const csm = new CSM({
  maxFar: 250, cascades: 4, mode: 'practical',        // 'uniform' | 'logarithmic' | 'practical' | 'custom'
  shadowMapSize: 2048, lightDirection: new THREE.Vector3(-1, -1, -1).normalize(),
  camera, parent: scene, lightIntensity: 3, lightMargin: 200,
});
csm.fade = true;                                         // blend across cascade borders
scene.traverse(o => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; csm.setupMaterial(o.material); } });
renderer.setAnimationLoop(() => { camera.updateMatrixWorld(); csm.update(); renderer.render(scene, camera); });
```
On resize or camera projection change call `csm.updateFrustums()`.

## 2. Tuning
- `maxFar` well below camera far. Defaults in CSM.js: `maxFar` 100000, `cascades` 3, `shadowMapSize` 2048, `lightIntensity` 3, `lightMargin` 200, `mode` `'practical'`, `fade` false.
- Split modes: `'practical'`, `'uniform'`, `'logarithmic'`, `'custom'` (with `customSplitsCallback`).
- `lightMargin`: extends the light camera backwards so off-screen casters (mountains, tall
  buildings) still cast into view.
- Bias is set per cascade light; normalBias helps acne.

## 3. WebGPU / TSL
The CSM.js header says to use `CSMShadowNode` instead of this class with `WebGPURenderer`; find its import path and usage in the release you pin.

## Gotchas
- Forgetting `setupMaterial` on materials created later (loaded glTF) means they ignore cascades.
- Shimmering when the camera moves: raise map size or reduce `maxFar`.

## Verify
- [ ] No visible gaps between cascades.

## Checked

2026-10-28. Confirmed in CSM.js: option names and defaults (`cascades`, `maxFar`, `mode`, `shadowMapSize`, `lightIntensity`, `lightMargin`, `customSplitsCallback`), `fade` default false, `setupMaterial`, `updateFrustums`, and the note pointing to `CSMShadowNode` for WebGPU.
Removed (not in the fetched pages): 100-300 m typical range, the `three/addons/csm/CSMShadowNode.js` path, `shadow.shadowNode`, the bias snippet, texel-snapping and pass-count claims, `CSMHelper`.

Method: documentation only; no commands were run.
