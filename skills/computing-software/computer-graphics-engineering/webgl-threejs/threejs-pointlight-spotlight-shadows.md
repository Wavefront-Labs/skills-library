---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-pointlight-spotlight-shadows
name: threejs-pointlight-spotlight-shadows
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-shadows, spotlight-shadow, pointlight-shadow, cube-shadow-map, light-map-size]
level: practitioner
status: docs-checked
description: "Tune three.js SpotLight and PointLight shadows: perspective shadow frustum, cube-map cost, near/far, focus, bias, and limiting shadow-casting lights."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/lights/SpotLightShadow.js", "https://github.com/mrdoob/three.js/blob/r186/src/lights/PointLightShadow.js", "https://github.com/mrdoob/three.js/blob/r186/src/lights/SpotLight.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLTextures.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLShadowMap.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js PointLight and SpotLight shadows

## 1. SpotLight
```js
const spot = new THREE.SpotLight(0xffffff, 50, 30, Math.PI / 6, 0.3, 2); // intensity(cd), distance, angle, penumbra, decay
spot.castShadow = true;
spot.shadow.mapSize.set(1024, 1024);
spot.shadow.camera.near = 0.5;        // far follows light.distance (30) automatically while distance is non-zero
spot.shadow.focus = 1;                // fraction of the cone angle the shadow camera covers
spot.shadow.bias = -0.0001; spot.shadow.normalBias = 0.02;
scene.add(spot, spot.target);
```
The shadow camera is a perspective camera with fov derived from `angle`; narrower cones give
sharper shadows for the same map size. `spot.map` modulates the light colour like a cookie texture and is disabled when `castShadow` is false.

## 2. PointLight
```js
point.castShadow = true;
point.shadow.mapSize.set(512, 512);   // per cube face
point.shadow.camera.near = 0.1; point.shadow.camera.far = 15;
```
Renders the shadow casters **six times** per frame (cube map faces). Use point shadows sparingly and bake or fake
(contact shadows, AO) the rest.

## 3. Precision
Perspective depth concentrates precision near `near`: push `near` out as far as possible, pull
`far` to the light's range. Acne on distant receivers can come from a `near` that is too small or a bias that is too low.

## 4. Cost control
- Only real hero lights cast; set `castShadow = false` on small props.
- Static scene: `renderer.shadowMap.autoUpdate = false` plus `needsUpdate = true` when lights or casters move.
- Point and spot light intensity is in candela; shadows only occlude the light.

## Gotchas
- Each shadow-casting light adds texture units to lit materials; three.js warns when a shader needs more texture units than the GPU supports (`renderer.capabilities.maxTextures`).
- Adding or removing lights at runtime changes the light counts in the shader program key, so lit materials recompile.

## Verify
- [ ] CameraHelper(spot.shadow.camera) shows a tight frustum.
- [ ] Frame time with point shadows measured on the target device.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: SpotLight constructor order and candela units; the spot shadow camera fov is `2 * angle * focus` and its `far` is
set from `light.distance` when non-zero; PointLightShadow uses a 90 degree perspective camera with six faces; `SpotLight.map`
is disabled when `castShadow` is false; `shadowMap.autoUpdate` and `needsUpdate`; the texture-unit warning
(`capabilities.maxTextures`); VSM is not supported for point lights.

Method: documentation only; no commands were run.
