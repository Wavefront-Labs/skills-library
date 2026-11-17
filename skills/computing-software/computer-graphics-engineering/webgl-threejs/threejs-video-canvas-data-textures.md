---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-video-canvas-data-textures
name: threejs-video-canvas-data-textures
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-materials, videotexture, datatexture, canvastexture, data3dtexture, dynamic-texture]
level: practitioner
status: docs-checked
description: "Feed three.js materials from video, 2D canvas and typed arrays: VideoTexture autoplay rules, CanvasTexture updates, DataTexture formats and partial uploads."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/textures/VideoTexture.js", "https://github.com/mrdoob/three.js/blob/r186/src/textures/DataTexture.js", "https://github.com/mrdoob/three.js/blob/r186/src/textures/DataArrayTexture.js", "https://github.com/mrdoob/three.js/blob/r186/src/textures/Texture.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLTextures.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js video, canvas and data textures

## 1. VideoTexture
```js
const video = Object.assign(document.createElement('video'), {
  src: '/media/clip.mp4', loop: true, muted: true, playsInline: true, crossOrigin: 'anonymous' });
await video.play();
const vt = new THREE.VideoTexture(video);
vt.colorSpace = THREE.SRGBColorSpace;
mat.map = vt;                              // updates automatically each frame a new video frame exists
```
- With WebGPURenderer a VideoTexture's `colorSpace` must be `SRGBColorSpace` (VideoTexture docs).
- Uses `requestVideoFrameCallback` when available to upload only on new frames.
- Webcam: `navigator.mediaDevices.getUserMedia({ video: true })`, `video.srcObject = stream`.

## 2. CanvasTexture
```js
const ctx = canvas.getContext('2d');  // draw...
const ct = new THREE.CanvasTexture(canvas);  ct.colorSpace = THREE.SRGBColorSpace;
// after redrawing:
ct.needsUpdate = true;
```
Only set needsUpdate when the canvas changed; every set re-uploads the whole canvas.

## 3. DataTexture
```js
const size = 256, data = new Float32Array(size * size * 4);
const dt = new THREE.DataTexture(data, size, size, THREE.RGBAFormat, THREE.FloatType);
dt.needsUpdate = true;
dt.magFilter = THREE.NearestFilter;      // lookup tables: no interpolation
```
- Linear filtering of `FloatType` data needs `OES_texture_float_linear`; three.js warns and falls back when it is missing.
- Integer data: `RedIntegerFormat` + `UnsignedIntType`, sampled as `usampler2D` in GLSL3.
- 3D LUTs/volumes: `Data3DTexture`; arrays of layers: `DataArrayTexture` (sampler2DArray).
- Partial update: `renderer.copyTextureToTexture` or `texture.addUpdateRange` (DataArrayTexture layers via `addLayerUpdate`).

## Gotchas
- Default `flipY` is false for DataTexture; row 0 is the bottom (v=0).
- After a texture's first use its dimensions, format and type cannot be changed (VideoTexture docs): dispose it and create a new one.
- `DataTexture` sets `unpackAlignment = 1` by default (plain `Texture` uses 4), so tightly packed odd-width data uploads correctly.

## Verify
- [ ] Video plays on iOS Safari inside the scene, muted autoplay.
- [ ] Data texture values read back as expected in the shader (render to screen as debug).

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: VideoTexture updates through `requestVideoFrameCallback` when available and has `generateMipmaps = false`; the
WebGPURenderer colour-space note; DataTexture defaults (`NearestFilter`, `generateMipmaps` false, `flipY` false,
`unpackAlignment` 1) versus Texture (`flipY` true, `unpackAlignment` 4); `OES_texture_float_linear` check and warning;
`Texture.addUpdateRange` and `DataArrayTexture.addLayerUpdate` exist; Data3DTexture and CanvasTexture exist; the
`RedIntegerFormat` and `UnsignedIntType` constants exist.

Method: documentation only; no commands were run.
