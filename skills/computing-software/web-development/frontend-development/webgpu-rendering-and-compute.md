---
id: computing-software.web-development.frontend-development.webgpu-rendering-and-compute
name: webgpu-rendering-and-compute
category: computing-software
field: web-development
product: frontend-development
tags: [webgpu, wgsl, gpu-compute, graphics, javascript]
level: advanced
status: docs-checked
description: "Getting started with WebGPU: adapter and device setup, canvas context, WGSL shaders, buffers and bind groups, a compute pass, feature detection with WebGL fallback, and debugging."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API
  - https://webgpufundamentals.org/
  - https://www.w3.org/TR/webgpu/
  - https://www.w3.org/TR/WGSL/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU rendering and compute basics

WebGPU is a successor to WebGL with an explicit, lower-level API plus general compute. It requires a secure context and is available in workers via `WorkerNavigator.gpu`. Per MDN browser-compat-data (checked 2026-10-26): Chrome and Edge 113 on ChromeOS, macOS and Windows (Linux with Intel Gen12+ GPUs from 144), Chrome Android 121, Safari 26, Firefox 141 on Windows (macOS Apple silicon from Firefox 145/147; no Linux; no service workers). Always feature-detect.

## 1. Setup and feature detection
```js
if (!navigator.gpu) return initWebGLFallback();
const adapter = await navigator.gpu.requestAdapter({ powerPreference: "high-performance" });
if (!adapter) return initWebGLFallback();          // blocklisted GPU or driver
const device = await adapter.requestDevice();
device.lost.then(info => { console.warn("GPU lost", info.reason); if (info.reason !== "destroyed") restart(); });
const ctx = canvas.getContext("webgpu");
const format = navigator.gpu.getPreferredCanvasFormat();
ctx.configure({ device, format, alphaMode: "premultiplied" });
```

## 2. Compute pass (double every number)
```js
const module = device.createShaderModule({ code: `
  @group(0) @binding(0) var<storage, read_write> data: array<f32>;
  @compute @workgroup_size(64) fn main(@builtin(global_invocation_id) id: vec3u) {
    if (id.x < arrayLength(&data)) { data[id.x] *= 2.0; }
  }` });
const pipeline = device.createComputePipeline({ layout: "auto", compute: { module, entryPoint: "main" } });
const buf = device.createBuffer({ size: input.byteLength, usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_SRC | GPUBufferUsage.COPY_DST });
device.queue.writeBuffer(buf, 0, input);
const read = device.createBuffer({ size: input.byteLength, usage: GPUBufferUsage.MAP_READ | GPUBufferUsage.COPY_DST });
const bind = device.createBindGroup({ layout: pipeline.getBindGroupLayout(0), entries: [{ binding: 0, resource: { buffer: buf } }] });
const enc = device.createCommandEncoder();
const pass = enc.beginComputePass(); pass.setPipeline(pipeline); pass.setBindGroup(0, bind);
pass.dispatchWorkgroups(Math.ceil(input.length / 64)); pass.end();
enc.copyBufferToBuffer(buf, 0, read, 0, input.byteLength);
device.queue.submit([enc.finish()]);
await read.mapAsync(GPUMapMode.READ); const out = new Float32Array(read.getMappedRange().slice(0)); read.unmap();
```
A buffer with `MAP_READ` may carry no usage flags other than `COPY_DST` (WebGPU spec), so a storage buffer cannot also be `MAP_READ`; copy to a staging buffer. Guard the index: the last workgroup can overrun the array.

## 3. Render loop essentials
Each frame: `ctx.getCurrentTexture().createView()` as the colour attachment, `beginRenderPass` with `loadOp: "clear"`, draw, `submit`. Handle resize by setting `canvas.width` and `canvas.height` from the element's client size times `devicePixelRatio` (cap it for performance), and recreate size-dependent textures such as depth buffers.

## 4. Gotchas
- Buffer layout follows WGSL alignment rules (`AlignOf(vec3<f32>)` is 16 in the WGSL spec). Pad structs or use a layout helper such as the `webgpu-utils` library.
- Errors are asynchronous: wrap setup in `device.pushErrorScope("validation")` / `popErrorScope()` and label every object (`label: "particles"`) so messages are readable.
- Many apps are better served by an engine such as three.js (which ships a `WebGPURenderer`) or Babylon.js than by raw WebGPU.

## Verify
- [ ] Works on a WebGPU browser and falls back cleanly where `navigator.gpu` or the adapter is missing; no validation errors in the console; device-loss path tested via `device.destroy()`.

## Checked

Checked 2026-10-26 against MDN WebGPU API, GPU.requestAdapter(), GPU.getPreferredCanvasFormat(), GPUCanvasContext.configure() and GPUDevice.lost (mdn/content main), MDN browser-compat-data (api/GPU.json), the WebGPU spec source (gpuweb/gpuweb spec/index.bs: MAP_READ usage restriction, pushErrorScope) and the WGSL source (wgsl/index.bs: `vec3u`, `@workgroup_size`, vec3 alignment 16), plus the three.js and webgpu-utils repositories. `requestAdapter()` resolves to null when no adapter is available, `getPreferredCanvasFormat()` returns `rgba8unorm` or `bgra8unorm`, `alphaMode` values, and `info.reason !== "destroyed"` follow MDN. Corrected the browser-support line (Linux and macOS coverage differ per BCD) and removed the unconfirmed auto-reconfigure claim on resize.

Method: documentation only; no commands were run.
