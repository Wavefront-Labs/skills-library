---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-render-pipeline-and-passes
name: webgpu-render-pipeline-and-passes
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, wgsl, webgpu-render-pipeline, render-pass, command-encoder, vertex-buffer-layout, depth-stencil, render-bundles]
level: practitioner
status: docs-checked
description: "Draw with raw WebGPU: render pipeline descriptors (vertex layouts, depth, blending, MSAA), command encoders and render passes with load/store ops, resolve targets."
sources: ["https://webgpufundamentals.org/webgpu/lessons/webgpu-fundamentals.html", "https://webgpufundamentals.org/webgpu/lessons/webgpu-multisampling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU render pipelines and passes

**Goal:** a correct, efficient frame: pipelines created up front, one command encoder per
frame, passes with deliberate load/store behaviour.

## 1. Pipeline
```js
const pipeline = device.createRenderPipeline({
  label: 'mesh', layout: pipelineLayout,
  vertex: { module, entryPoint: 'vs', buffers: [{
    arrayStride: 32, stepMode: 'vertex', attributes: [
      { shaderLocation: 0, offset: 0,  format: 'float32x3' },   // position
      { shaderLocation: 1, offset: 12, format: 'float32x3' },   // normal
      { shaderLocation: 2, offset: 24, format: 'float32x2' } ]}]},  // uv
  fragment: { module, entryPoint: 'fs', targets: [{ format: canvasFormat,
    blend: undefined /* opaque */ }] },
  primitive: { topology: 'triangle-list', cullMode: 'back', frontFace: 'ccw' },
  depthStencil: { format: 'depth24plus', depthWriteEnabled: true, depthCompare: 'less' },
  multisample: { count: 4 },
});
```
Pipelines bake most state, so create variants at load time, not mid-frame. In WebGPU version 1 `multisample.count` and a texture's `sampleCount` can only be 1 or 4 (webgpufundamentals); the pipeline only works with attachments of the same sample count (MDN).

## 2. Frame and pass
```js
const enc = device.createCommandEncoder({ label: 'frame' });
const pass = enc.beginRenderPass({
  colorAttachments: [{ view: msaaView, resolveTarget: ctx.getCurrentTexture().createView(),
                       clearValue: [0.1, 0.1, 0.12, 1], loadOp: 'clear', storeOp: 'discard' }],
  depthStencilAttachment: { view: depthView, depthClearValue: 1, depthLoadOp: 'clear', depthStoreOp: 'discard' },
});
pass.setPipeline(pipeline);
pass.setBindGroup(0, frameBG);
pass.setVertexBuffer(0, vbo); pass.setIndexBuffer(ibo, 'uint32');
pass.drawIndexed(indexCount);
pass.end();
device.queue.submit([enc.finish()]);
```
- `storeOp: 'discard'` discards the pass result for that attachment: use it on the MSAA colour (the resolve target keeps the image) and on depth you don't reuse.
- `loadOp: 'load'` only when you need previous contents.
- With a `resolveTarget`, the view must have a sample count above 1 and the resolve target a sample count of 1, with matching size and format (MDN beginRenderPass).

## 3. Uploads
`device.queue.writeBuffer` / `writeTexture` for small/medium updates;
`mappedAtCreation: true` for initial data; avoid mapping round-trips per frame.
`copyExternalImageToTexture` for ImageBitmap/video frames.

## Gotchas
- `getCurrentTexture()` is called inside the render function each frame; the webgpufundamentals lesson relies on this so a resized canvas needs no extra work.

## Verify
- [ ] No pipeline creation during steady-state frames (performance timeline).
- [ ] MSAA edges correct; resolved image displayed; validation clean.
- [ ] JS CPU time per frame measured.

## Checked

2026-10-28. Confirmed: MSAA count 1 or 4 in WebGPU version 1 and the `sampleCount` rules (webgpufundamentals multisampling, MDN createRenderPipeline), `storeOp` "discard" and the `resolveTarget` requirements (MDN beginRenderPass), `getCurrentTexture()` called per frame in render (webgpufundamentals fundamentals), `arrayStride` / `stepMode` in the vertex buffer layout (MDN).
Removed (not in the fetched pages): `createRenderPipelineAsync`, bandwidth and tiler claims, depth24plus/depth32float advice, `stripIndexFormat` and `arrayStride` multiple-of-4 rules, render bundles section, dead W3C spec links. The pipeline and pass snippets are illustrative skeletons, not copied from a page.

Method: documentation only; no commands were run.
