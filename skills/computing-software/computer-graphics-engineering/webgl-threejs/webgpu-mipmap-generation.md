---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-mipmap-generation
name: webgpu-mipmap-generation
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, webgpu-mipmaps, mipmap-generation, texture-views, srgb-mipmaps]
level: advanced
status: docs-checked
description: "Generate mipmaps in WebGPU, which has no generateMipmap: a render-pass blit per mip level using single-level texture views."
sources: ["https://webgpufundamentals.org/webgpu/lessons/webgpu-importing-textures.html#a-generating-mips-on-the-gpu", "https://toji.dev/webgpu-best-practices/img-textures#generating-mipmaps"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mipmap generation in WebGPU

## 1. Allocate the chain
```js
const mipLevelCount = Math.floor(Math.log2(Math.max(w, h))) + 1;
const tex = device.createTexture({ size: [w, h], format, mipLevelCount,
  usage: GPUTextureUsage.TEXTURE_BINDING | GPUTextureUsage.COPY_DST | GPUTextureUsage.RENDER_ATTACHMENT });
```

## 2. Render-pass blit
```js
const pipeline = device.createRenderPipeline({ layout: 'auto',
  vertex: { module, entryPoint: 'vs' },                      // fullscreen triangle from vertex_index
  fragment: { module, entryPoint: 'fs', targets: [{ format }] } });
const sampler = device.createSampler({ minFilter: 'linear', magFilter: 'linear' });
const enc = device.createCommandEncoder();
for (let level = 1; level < mipLevelCount; level++) {
  const bg = device.createBindGroup({ layout: pipeline.getBindGroupLayout(0), entries: [
    { binding: 0, resource: sampler },
    { binding: 1, resource: tex.createView({ baseMipLevel: level - 1, mipLevelCount: 1 }) } ] });
  const pass = enc.beginRenderPass({ colorAttachments: [{
    view: tex.createView({ baseMipLevel: level, mipLevelCount: 1 }), loadOp: 'clear', storeOp: 'store' }] });
  pass.setPipeline(pipeline); pass.setBindGroup(0, bg); pass.draw(3); pass.end();
}
device.queue.submit([enc.finish()]);
```
Cache the pipeline per format.

WebGPU has no `generateMipmap`: you must set every mip level explicitly, either by generating them at runtime as above or, for compressed textures, by shipping the mip levels in the file.

## Gotchas
- The texture must be created with its mip level count and with `RENDER_ATTACHMENT` usage for this method (`COPY_DST` is also needed for `copyExternalImageToTexture`).

## Verify
- [ ] Each level, viewed separately, shows the expected downsampling.

## Checked
2026-11-01. Confirmed against WebGPU Fundamentals (importing textures: mip count is log2(max size) + 1, RENDER_ATTACHMENT and COPY_DST usage, per-level views with baseMipLevel and mipLevelCount 1) and Toji's WebGPU best practices (explicit mip levels, generation by render pass, compressed textures store mips in the file). Removed: sRGB handling, compute downsampling, array/cube-map, non-power-of-two and compressed-render claims, and the W3C spec link (not readable).
Method: documentation only; no commands were run.
