---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-shadow-camera-and-map-tuning
name: threejs-shadow-camera-and-map-tuning
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-shadows, shadow-camera, shadow-bias, pcfsoftshadowmap, vsmshadowmap, normalbias, camerahelper, directional-light-shadow, shadow-acne, castshadow, receiveshadow, shadow-autoupdate]
level: practitioner
status: docs-checked
description: "Get crisp, stable shadows in three.js: enable casting/receiving, fit the directional light's orthographic shadow camera, map size, bias vs normalBias, and shadow map types."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLShadowMap.js", "https://github.com/mrdoob/three.js/blob/r186/src/lights/LightShadow.js", "https://github.com/mrdoob/three.js/blob/r186/src/lights/DirectionalLightShadow.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/shadows.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# three.js shadow camera and shadow map tuning

**Goal:** shadows that are sharp where the player looks, free of acne and gaps, and cheap.

## 1. Turn them on (four switches)
```js
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;   // default; also BasicShadowMap, VSMShadowMap
light.castShadow = true;
mesh.castShadow = true; ground.receiveShadow = true;
```
Missing any one = no shadow, no error.

## 2. Fit the shadow camera (the key step)
A DirectionalLight shadow uses an **orthographic camera** around `light.position` looking at
`light.target`. Default frustum is ±5 units — too small for most scenes (shadows cut off)
or, if enlarged lazily, too big (blurry).
```js
const cam = light.shadow.camera;
cam.left = -20; cam.right = 20; cam.top = 20; cam.bottom = -20;
cam.near = 0.5; cam.far = 80;
cam.updateProjectionMatrix();
light.shadow.mapSize.set(2048, 2048);
scene.add(new THREE.CameraHelper(cam));      // visualise while tuning
scene.add(light.target);                      // target must be in the scene to follow moves
```
Make the box as tight as possible around what needs shadows. For a moving player, move the
light and its target with the player (snap to texel increments to avoid shimmering:
`worldUnitsPerTexel = (right-left)/mapSize.x`).
SpotLight shadow: perspective camera from `angle`; PointLight: cube map (6 renders —
expensive, avoid many).

## 3. Bias
- `light.shadow.bias` (default 0): the three.js docs say tiny adjustments on the order of 0.0001 may reduce artifacts.
- `light.shadow.normalBias` (default 0): offsets the shadow-map lookup along the surface normal; it reduces acne on
  surfaces lit at shallow angles, at the cost that shadows may appear distorted.

## 4. Types and softness
- `PCFShadowMap` (the default): `shadow.radius` above 1 blurs the edge; high values cause banding unless `mapSize` is large.
  `PCFSoftShadowMap` was removed: r186 logs a warning and uses `PCFShadowMap`.
- `BasicShadowMap`: `shadow.radius` has no effect.
- `VSMShadowMap`: blurred with `shadow.radius` and `shadow.blurSamples` (default 8); receiving meshes are also rendered
  into the shadow pass, and VSM is not supported for point lights.

## 5. Cost control
Each shadow-casting light renders the scene again (6x for point lights). Disable
`castShadow` on tiny/distant objects; static scenes: `renderer.shadowMap.autoUpdate = false`
and set `renderer.shadowMap.needsUpdate = true` when something moves.

## Gotchas
- Opacity is ignored in the shadow pass: transparent objects cast solid shadows unless they use `alphaTest` with a `map`
  or `alphaMap` (or a `customDepthMaterial`).
- A `mapSize` above `renderer.capabilities.maxTextureSize` is reduced by the renderer, so you do not get the resolution you asked for.
- Moving `light.position` without the target changes direction, not just placement.

## Verify
- [ ] CameraHelper box tightly encloses shadow casters/receivers in view.
- [ ] No acne on slopes, no detached shadows at contact points.
- [ ] Frame time measured with and without shadows; within budget.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: `renderer.shadowMap.type` defaults to `PCFShadowMap` and `PCFSoftShadowMap` has been removed (warning and fallback);
DirectionalLightShadow uses an orthographic camera of +/-5 with near 0.5 and far 500; `bias` and `normalBias` default 0 with the
documented guidance; `radius` default 1 and no effect for `BasicShadowMap`; `blurSamples` default 8; `mapSize` default 512 and it
is clamped to `maxTextureSize`; VSM unsupported for point lights; the shadow depth material honours `alphaTest` with `map` or
`alphaMap` but not opacity; the DirectionalLight target must be in the scene to move; `shadowMap.autoUpdate` and `needsUpdate`.

Method: documentation only; no commands were run.
