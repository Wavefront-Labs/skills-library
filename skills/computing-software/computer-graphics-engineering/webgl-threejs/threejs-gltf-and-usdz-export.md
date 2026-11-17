---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-gltf-and-usdz-export
name: threejs-gltf-and-usdz-export
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-loading, gltfexporter, usdzexporter, ar-quick-look, scene-export]
level: practitioner
status: docs-checked
description: "Export three.js scenes with GLTFExporter (glb, animations, binary) and USDZExporter for iOS AR Quick Look, and fix what does not survive export."
sources: ["https://github.com/mrdoob/three.js/blob/r186/examples/jsm/exporters/GLTFExporter.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/exporters/USDZExporter.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GLTFExporter and USDZExporter

## 1. glb download
```js
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';
const glb = await new GLTFExporter().parseAsync(scene, {
  binary: true, onlyVisible: true, animations: clips, maxTextureSize: 2048, includeCustomExtensions: false });
const url = URL.createObjectURL(new Blob([glb], { type: 'model/gltf-binary' }));
Object.assign(document.createElement('a'), { href: url, download: 'scene.glb' }).click();
URL.revokeObjectURL(url);
```
`binary: false` returns a JSON object whose buffer is embedded as a base64 data URI (larger).

## 2. What exports
Meshes, InstancedMesh (via EXT_mesh_gpu_instancing), skinned meshes, morph targets, cameras,
punctual lights (KHR_lights_punctual), MeshStandard/Physical (with KHR_materials_* where
supported), texture transforms, userData into `extras`.

## 3. What does not
ShaderMaterial (the exporter warns and skips the material), `onBeforeCompile` effects, fog and post-processing.
Materials other than MeshStandardMaterial and MeshBasicMaterial log a warning. Bake shader looks into textures first.

## 4. USDZ for iOS AR Quick Look
```js
import { USDZExporter } from 'three/addons/exporters/USDZExporter.js';
const usdz = await new USDZExporter().parseAsync(scene, { quickLookCompatible: true, maxTextureSize: 2048 });
const blob = new Blob([usdz]);                    // then serve it or link to it
```
Options in r186: `quickLookCompatible` (default false), `maxTextureSize` (default 1024), `animations`, `animationFrameRate`
(default 60) and `includeAnchoringProperties`. Use MeshStandardMaterial (the exporter warns otherwise); textures are
written as PNG or JPEG.

## Gotchas
- Texture images are re-encoded through a canvas (PNG or JPEG) and `flipY` is applied when writing them, so the original compressed texture format is not preserved.

## Verify
- [ ] Exported glb loads in a glTF validator and viewer without errors.
- [ ] USDZ opens in your target AR viewer with correct scale.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), GLTFExporter.js and USDZExporter.js source.
Confirmed: GLTFExporter option defaults (`binary` false, `onlyVisible` true, `maxTextureSize` Infinity, `animations`,
`includeCustomExtensions` false) and `parseAsync`; supported extensions include `KHR_lights_punctual`, `KHR_materials_*`,
`KHR_texture_transform` and `EXT_mesh_gpu_instancing`; ShaderMaterial is skipped with a warning; userData goes to `extras`;
the non-binary buffer is a base64 data URI; USDZExporter options (`quickLookCompatible`, `maxTextureSize` 1024, `animations`,
`animationFrameRate` 60), and it exports animations.

Method: documentation only; no commands were run.
