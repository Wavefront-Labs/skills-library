---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-texture-wrapping-filtering-anisotropy
name: threejs-texture-wrapping-filtering-anisotropy
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-materials, texture-wrapping, flipy, anisotropy, mipmaps, minfilter]
level: practitioner
status: docs-checked
description: "Configure three.js textures correctly: wrapS/wrapT, mag/min filters and mipmaps, anisotropic filtering, flipY for glTF vs images, and colorSpace per map."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/textures/Texture.js", "https://github.com/mrdoob/three.js/blob/r186/src/loaders/ImageBitmapLoader.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLCapabilities.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/loaders/GLTFLoader.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/textures.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js texture wrapping, filtering and anisotropy

## 1. Settings checklist per texture
```js
const t = await new THREE.TextureLoader().loadAsync('/tex/brick_albedo.jpg');
t.colorSpace = THREE.SRGBColorSpace;            // colour/emissive maps only; data maps stay NoColorSpace
t.wrapS = t.wrapT = THREE.RepeatWrapping;       // ClampToEdgeWrapping (default), MirroredRepeatWrapping
t.repeat.set(4, 4);
t.anisotropy = renderer.capabilities.getMaxAnisotropy();   // default 1; higher is less blurry than a plain mipmap, at more cost; 0 if the extension is missing
t.magFilter = THREE.LinearFilter;               // NearestFilter for pixel art
t.minFilter = THREE.LinearMipmapLinearFilter;   // trilinear, default
t.generateMipmaps = true;
```
Changing wrap/filter after first upload needs `t.needsUpdate = true`.

## 2. flipY
- `TextureLoader` images: `flipY = true` (default) matches three's UV convention.
- glTF textures: `flipY = false` (glTF UV origin is top-left). Swapping a glTF map with a
  TextureLoader texture without setting `flipY = false` shows it upside down.
- `ImageBitmapLoader`: flip at decode with `setOptions({ imageOrientation: 'flipY' })`; the texture's
  flipY is ignored for ImageBitmaps.

## 3. Pixel art
`magFilter = minFilter = NearestFilter; generateMipmaps = false;` and keep `renderer.setPixelRatio` integer.

## 4. Non-power-of-two
three.js r186 requires WebGL 2 (`capabilities.isWebGL2` is kept only for backwards compatibility), where non-power-of-two
textures can use mipmaps and repeat wrapping.

## Gotchas
- Sharing an image with a different `repeat` per material requires `t.clone()`: the clone shares the source image but has its own transform, and `copy()` already sets `needsUpdate`.
- Moire on distant tiling: ensure mipmaps exist (`minFilter` with Mipmap) and anisotropy set.
- Normal maps tagged sRGB light incorrectly; roughness/metalness/AO must be linear.

## Verify
- [ ] Floor texture sharp at grazing angles (anisotropy) and no shimmer far away (mipmaps).
- [ ] Replaced glTF textures appear the right way up.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: Texture constructor defaults (`ClampToEdgeWrapping`, `magFilter` LinearFilter, `minFilter`
LinearMipmapLinearFilter, `anisotropy` 1, `generateMipmaps` true, `flipY` true, `repeat` (1, 1)); the anisotropy description and that
`getMaxAnisotropy()` returns 0 without `EXT_texture_filter_anisotropic`; GLTFLoader sets `flipY = false` on glTF textures;
ImageBitmapLoader ignores `flipY` and takes `imageOrientation` through `setOptions`; the colour-management manual says
`normalMap` and `roughnessMap` use `NoColorSpace`; `Texture.copy()` sets `needsUpdate = true`.

Method: documentation only; no commands were run.
