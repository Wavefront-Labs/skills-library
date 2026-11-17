---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-lights-and-environment-lighting
name: threejs-lights-and-environment-lighting
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, three-lights, hemispherelight, directionallight, environment-lighting, physically-correct-lights, rgbeloader]
level: practitioner
status: docs-checked
description: "Choose and configure three.js lights (Ambient, Hemisphere, Directional, Point, Spot, RectArea) and environment lighting with physical units and sane costs."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/lights/RectAreaLight.js", "https://github.com/mrdoob/three.js/blob/r186/src/lights/SpotLight.js", "https://github.com/mrdoob/three.js/blob/r186/src/lights/PointLight.js", "https://github.com/mrdoob/three.js/blob/r186/src/lights/DirectionalLight.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLPrograms.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/loaders/RGBELoader.js"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# three.js lights and environment lighting

## 1. Light types
| Light | Use | Cost |
|---|---|---|
| `HemisphereLight(sky, ground, i)` | Cheap outdoor fill, sky/ground tint | Very low |
| `AmbientLight` | Flat fill; looks fake, prefer hemisphere or env map | Very low |
| `DirectionalLight` | Sun; shadows via orthographic shadow camera | Medium (+shadow) |
| `PointLight(c, intensity, distance, decay=2)` | Bulbs | Shadow = 6 cube faces, expensive |
| `SpotLight` | Torches, stage | One shadow map |
| `RectAreaLight` | Soft panels; PBR materials only, no shadows | Medium (LTC) |
`RectAreaLight` needs `RectAreaLightUniformsLib.init()` with WebGLRenderer (WebGPURenderer uses `RectAreaLightTexturesLib`) before use.

## 2. Units
PointLight and SpotLight intensity is measured in candela; `distance` defaults to 0 (no limit) and `decay` to 2
(inverse square). The other light classes document no unit for `intensity`.

## 3. Environment lighting (usually the biggest win)
```js
import { HDRLoader } from 'three/addons/loaders/HDRLoader.js';   // RGBELoader is a deprecated alias (r180)
new HDRLoader().load('studio.hdr', (tex) => {
  tex.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = tex;          // IBL for all PBR materials
  scene.background = tex;           // optional
});
// or procedural: scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
```
`scene.environmentIntensity` (default 1) scales the scene environment globally.

## 4. Budget
The number of lights of each type is part of the shader program key (WebGLPrograms), so changing the light counts
recompiles the affected materials.

## Gotchas
- Adding or removing lights at runtime changes the program key and recompiles (stutter). An object with
  `visible = false` is skipped by the renderer, which also changes the light count; set `intensity = 0` instead.
- MeshBasicMaterial ignores lights; RectAreaLight supports PBR materials only.
- `DirectionalLight` direction comes from position to `light.target`; add the target to the scene
  if you move it.

## Verify
- [ ] `renderer.info.programs.length` stable while toggling lights.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: PointLight `(color, intensity, distance = 0, decay = 2)` with intensity in candela; SpotLight
`(color, intensity, distance, angle, penumbra, decay)` with candela; RectAreaLight has no shadow support, supports only PBR
materials, and needs `RectAreaLightUniformsLib.init()` for WebGLRenderer (`RectAreaLightTexturesLib` for WebGPURenderer);
DirectionalLight points from its position to `target` and the target must be in the scene to move; HemisphereLight and
AmbientLight cannot cast shadows; light counts are in the program key (WebGLPrograms.js); invisible objects are skipped
by `projectObject`; `RGBELoader` is a deprecated alias of `HDRLoader` since r180; `scene.environmentIntensity` defaults to 1.
The relative cost labels in the table are rule-of-thumb descriptions, not documented figures.

Method: documentation only; no commands were run.
