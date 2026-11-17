---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-compute-pipelines-and-storage-buffers
name: webgpu-compute-pipelines-and-storage-buffers
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webgpu-api, webgpu-compute, storage-buffers, wgsl-compute, workgroups]
level: advanced
status: docs-checked
description: "Write WebGPU compute: WGSL @compute shaders, storage buffers, bind groups, dispatchWorkgroups, and reading results back with mapAsync."
sources: ["https://webgpufundamentals.org/webgpu/lessons/webgpu-compute-shaders.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU compute pipelines

## 1. Shader
```wgsl
@group(0) @binding(0) var<storage, read> input : array<f32>;
@group(0) @binding(1) var<storage, read_write> output : array<f32>;
@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id : vec3u) {
  if (id.x >= arrayLength(&input)) { return; }
  output[id.x] = input[id.x] * 2.0;
}
```

## 2. Pipeline and dispatch
```js
const module = device.createShaderModule({ code });
const pipeline = device.createComputePipeline({ layout: 'auto', compute: { module, entryPoint: 'main' } });
const inBuf = device.createBuffer({ size: n * 4, usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST });
const outBuf = device.createBuffer({ size: n * 4, usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_SRC });
const readBuf = device.createBuffer({ size: n * 4, usage: GPUBufferUsage.MAP_READ | GPUBufferUsage.COPY_DST });
device.queue.writeBuffer(inBuf, 0, data);
const bg = device.createBindGroup({ layout: pipeline.getBindGroupLayout(0),
  entries: [{ binding: 0, resource: { buffer: inBuf } }, { binding: 1, resource: { buffer: outBuf } }] });
const enc = device.createCommandEncoder();
const pass = enc.beginComputePass();
pass.setPipeline(pipeline); pass.setBindGroup(0, bg);
pass.dispatchWorkgroups(Math.ceil(n / 64));
pass.end();
enc.copyBufferToBuffer(outBuf, 0, readBuf, 0, n * 4);
device.queue.submit([enc.finish()]);
await readBuf.mapAsync(GPUMapMode.READ);
const result = new Float32Array(readBuf.getMappedRange().slice(0)); readBuf.unmap();
```

## 3. Limits and patterns
- Default `maxComputeWorkgroupSizeX` and `maxComputeWorkgroupSizeY` are 256 and `maxComputeWorkgroupSizeZ` is 64; the product of the three `@workgroup_size` values may not exceed `maxComputeInvocationsPerWorkgroup` (256), so `@workgroup_size(16, 16, 2)` is invalid.
- `global_invocation_id = workgroup_id * workgroup_size + local_invocation_id`.
- Feed compute output to rendering by binding the same buffer as `vertex` or `storage` in the
  render pipeline: no readback needed.

## Gotchas
- Read results through a separate `MAP_READ | COPY_DST` buffer filled with `copyBufferToBuffer`, then `mapAsync(GPUMapMode.READ)`.
- Always bounds-check `id.x` against the array length, since dispatch rounds up to whole workgroups.

## Verify
- [ ] Compare a CPU reference on random input.

## Checked
2026-10-31. Confirmed against the WebGPU Fundamentals compute-shader lesson: storage `read_write` bindings, `@workgroup_size`, the global_invocation_id formula, workgroup size limits (256/256/64, 256 invocations), MAP_READ | COPY_DST read buffer and `mapAsync(GPUMapMode.READ)`. Removed: `maxStorageBufferBindingSize` default, workgroup memory and atomics notes, out-of-bounds behaviour, per-frame readback advice and `device.lost` advice (W3C WebGPU spec not readable here).
Method: documentation only; no commands were run.
