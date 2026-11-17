---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-ssao-gtao-passes
name: threejs-ssao-gtao-passes
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-postprocessing, gtaopass, ssaopass, n8ao, ambient-occlusion]
level: advanced
status: draft
description: "Add screen-space ambient occlusion to three.js with GTAOPass, SSAOPass or N8AO: parameters, normal/depth inputs, denoising, cost on mobile, and halo artefacts."
sources: ["https://threejs.org/docs/#examples/en/postprocessing/GTAOPass", "https://threejs.org/examples/#webgl_postprocessing_gtao", "https://threejs.org/examples/#webgl_postprocessing_ssao", "https://github.com/N8python/n8ao"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSAO and GTAO passes in three.js

## 1. GTAOPass (preferred built-in, r162+)
```js
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
composer.addPass(new RenderPass(scene, camera));
const ao = new GTAOPass(scene, camera, w, h);
ao.updateGtaoMaterial({ radius: 0.5, distanceExponent: 1, thickness: 1, scale: 1, samples: 16 });
ao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 4, rings: 2, samples: 16 }); // denoise
ao.blendIntensity = 1;
composer.addPass(ao);
composer.addPass(new OutputPass());
```
`ao.output = GTAOPass.OUTPUT.AO` (or `.Denoise`) shows the raw AO for tuning.
GTAO renders its own normal/depth pass unless you pass existing `gBuffer` textures.

## 2. SSAOPass (older)
`new SSAOPass(scene, camera, w, h)`; `kernelRadius`, `minDistance`, `maxDistance` in view-space
units relative to camera near/far. Cheaper, noisier, more haloing.

## 3. N8AO (community, high quality)
`new N8AOPass(scene, camera, w, h)` or the pmndrs `N8AOPostPass`; `aoRadius` in world units,
`halfRes = true` for mobile, `quality` presets. Generally best quality per ms.

## 4. Tuning rules
- Radius in **world units** of your scene scale (a 1 m person: 0.3-1.0).
- Half-resolution AO plus depth-aware upsample for mobile; full-res only on desktop.
- AO should darken ambient/indirect light only; post AO darkens direct light too, so keep
  intensity moderate and prefer baked AO for static assets.

## Gotchas
- Thin dark halos around silhouettes: radius too big or depth discontinuity threshold too low.
- Wrong results with logarithmic depth buffer or custom vertex displacement (normal pass mismatch).
- Transparent objects are not in the normal/depth pass: they get no AO and may show AO from behind.

## Verify
- [ ] AO-only view shows contact darkening in corners, no banding or wide halos.
- [ ] Cost measured: AO pass under ~2 ms on target hardware.
