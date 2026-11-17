---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-textures-samplers-external-images
name: webgpu-textures-samplers-external-images
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, gpu-texture, copyexternalimagetotexture, gpusampler, external-texture, texture-formats]
level: practitioner
status: docs-checked
description: "Create and fill WebGPU textures: formats and usages, copyExternalImageToTexture from images/canvas, writeTexture alignment, samplers, and importExternalTexture for video."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/GPUQueue/copyExternalImageToTexture", "https://webgpufundamentals.org/webgpu/lessons/webgpu-importing-textures.html", "https://developer.mozilla.org/en-US/docs/Web/API/GPUDevice/importExternalTexture"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU textures, samplers and external images

## 1. Load an image into a texture
```js
const bmp = await createImageBitmap(await (await fetch(url)).blob(), { colorSpaceConversion: 'none' });
const tex = device.createTexture({
  size: [bmp.width, bmp.height], format: 'rgba8unorm-srgb', mipLevelCount: mips(bmp),
  usage: GPUTextureUsage.TEXTURE_BINDING | GPUTextureUsage.COPY_DST | GPUTextureUsage.RENDER_ATTACHMENT });
device.queue.copyExternalImageToTexture({ source: bmp, flipY: false }, { texture: tex }, [bmp.width, bmp.height]);
```
- Destination of copyExternalImageToTexture needs `RENDER_ATTACHMENT` usage as well as COPY_DST.

## 2. Raw data: writeTexture
```js
device.queue.writeTexture({ texture: tex }, data, { bytesPerRow: w * 4, rowsPerImage: h }, [w, h]);
```

## 3. Samplers
```js
const samp = device.createSampler({ magFilter: 'linear', minFilter: 'linear', mipmapFilter: 'linear',
  addressModeU: 'repeat', addressModeV: 'repeat', maxAnisotropy: 16 });
```
Samplers are separate objects bound independently from textures.

## 4. Video
```js
const ext = device.importExternalTexture({ source: videoEl });
```
See the MDN `importExternalTexture` page for the lifetime of the returned texture and the WGSL side.

## Gotchas
- Mipmaps are not generated automatically; see mipmap generation via render or compute passes.
- Filtering `rgba32float` textures needs the `float32-filterable` feature.
- Compressed formats need features: `texture-compression-bc`, `texture-compression-etc2`, `texture-compression-astc`.

## Verify
- [ ] Texture appears correctly oriented and gamma-correct versus the source image.
- [ ] No validation errors about missing usage flags.

## Checked

2026-10-28. Confirmed: copyExternalImageToTexture needs COPY_DST and RENDER_ATTACHMENT usage (MDN, webgpufundamentals importing-textures); `float32-filterable` and the `texture-compression-bc` / `-etc2` / `-astc` feature names (MDN GPUSupportedFeatures).
Removed (not in the fetched pages): source-type list, `-srgb` decode claim, writeTexture alignment claim, anisotropy filter claim, `texture_depth_2d` / `textureSampleCompare`, `texture_external` / `textureSampleBaseClampToEdge` and the zero-copy claim, desktop/mobile labels on compression features, `rgba16float` advice, dead W3C spec link.

Method: documentation only; no commands were run.
