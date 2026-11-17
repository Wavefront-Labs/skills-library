---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-shadowmaterial-shadow-catchers
name: threejs-shadowmaterial-shadow-catchers
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-shadows, shadowmaterial, shadow-catcher, ar-shadows, product-viewer]
level: practitioner
status: docs-checked
description: "Show only shadows on an invisible ground in three.js with ShadowMaterial: product viewers over HTML backgrounds, AR shadow catchers, opacity and colour tuning."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/materials/ShadowMaterial.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/Material.js", "https://github.com/mrdoob/three.js/blob/r186/examples/webxr_ar_lighting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js ShadowMaterial and shadow catchers

## 1. Basic catcher
```js
const ground = new THREE.Mesh(
  new THREE.PlaneGeometry(20, 20).rotateX(-Math.PI / 2),
  new THREE.ShadowMaterial({ opacity: 0.35, color: 0x000000 }));
ground.receiveShadow = true;
scene.add(ground);
```
The plane is invisible except where shadows fall; it is a transparent material, so it composes
over `scene.background = null` with `alpha: true` renderer (HTML behind) or over AR camera passthrough.

## 2. Tuning
- `opacity` controls darkness (the class documentation example uses 0.2).
- Soft look: `shadow.radius` above 1 with the default `PCFShadowMap`, or `VSMShadowMap`; `PCFSoftShadowMap` no longer exists in r186.
- Coloured shadows: `color` tints the shadowed area.
- Per its documentation, a ShadowMaterial can receive shadows but is otherwise completely transparent.

## 3. AR use
Place the catcher at the hit-test floor pose under the model; keep the shadow camera tight
around the model. Combine with `XREstimatedLight` for a matching light direction.

## Gotchas
- Shadow catcher z-fights with a visible floor at the same height: offset or remove one.
- Being transparent, it sorts with other transparent objects; set `renderOrder` lower than glass in the scene.
- Tone mapping and post-processing can lift the shadow towards grey; check final output, and set `toneMapped: false` if needed.

## Verify
- [ ] Over a white HTML background, only a soft grey shadow is visible under the model.
- [ ] No visible plane edge when the shadow camera is fitted.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), ShadowMaterial.js, Material.js and the `webxr_ar_lighting` example.
Confirmed: `ShadowMaterial` default `color` 0x000000, `transparent = true`, `fog` default true, documented as receiving
shadows but otherwise fully transparent; `Material.toneMapped` exists; `XREstimatedLight` is used in the AR lighting example with
the `light-estimation` feature; `PCFSoftShadowMap` was removed in r186.

Method: documentation only; no commands were run.
