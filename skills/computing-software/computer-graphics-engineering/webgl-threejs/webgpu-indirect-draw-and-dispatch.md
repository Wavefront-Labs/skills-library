---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-indirect-draw-and-dispatch
name: webgpu-indirect-draw-and-dispatch
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, webgpu-indirect, drawindirect, dispatchworkgroupsindirect, gpu-culling, gpu-driven-rendering]
level: advanced
status: docs-checked
description: "Drive WebGPU draws and dispatches from GPU buffers: indirect argument layouts, compute culling that writes instance counts, atomics, and no-multi-draw limits."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/GPURenderPassEncoder/drawIndirect", "https://developer.mozilla.org/en-US/docs/Web/API/GPURenderPassEncoder/drawIndexedIndirect", "https://developer.mozilla.org/en-US/docs/Web/API/GPUComputePassEncoder/dispatchWorkgroupsIndirect", "https://toji.dev/webgpu-best-practices/indirect-draws"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indirect drawing and dispatch in WebGPU

## 1. Argument buffers
```js
// drawIndirect: vertexCount, instanceCount, firstVertex, firstInstance          (4 x u32 = 16 B)
// drawIndexedIndirect: indexCount, instanceCount, firstIndex, baseVertex(i32), firstInstance (20 B)
// dispatchWorkgroupsIndirect: x, y, z                                             (12 B)
const args = device.createBuffer({ size: 20,
  usage: GPUBufferUsage.INDIRECT | GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST });
device.queue.writeBuffer(args, 0, new Uint32Array([indexCount, 0, 0, 0, 0]));
pass.drawIndexedIndirect(args, 0);      // offset multiple of 4
```
A non-zero `firstInstance` needs the `indirect-first-instance` feature; without it the indirect call is treated as a no-op (MDN). The buffer needs the `INDIRECT` usage and the offset must be a multiple of 4.

## 2. GPU culling writes the count
```wgsl
struct DrawArgs { indexCount: u32, instanceCount: atomic<u32>, firstIndex: u32, baseVertex: i32, firstInstance: u32 };
@group(0) @binding(0) var<storage, read> objects: array<Obj>;
@group(0) @binding(1) var<storage, read_write> visible: array<u32>;
@group(0) @binding(2) var<storage, read_write> args: DrawArgs;
@compute @workgroup_size(64) fn cull(@builtin(global_invocation_id) id: vec3u) {
  if (id.x >= arrayLength(&objects)) { return; }
  if (inFrustum(objects[id.x].sphere)) { let slot = atomicAdd(&args.instanceCount, 1u); visible[slot] = id.x; }
}
```
Reset `instanceCount` to 0 each frame (writeBuffer or a tiny compute pass) before culling.
The vertex shader reads `objects[visible[instance_index]]`.

## 3. Limits
- One indirect call draws one set of arguments: issue one call per mesh type/material and merge geometry into a few big buffers.
- Indirect dispatch: compute the workgroup count on GPU (e.g. ceil(count/64)) in a 1-thread pass.

## Gotchas
- Clamp counts in the culling shader so the indirect arguments stay valid.

## Verify
- [ ] Visible instance count (debug readback) drops when looking away.
- [ ] CPU time independent of object count.

## Checked

2026-10-28. Confirmed on MDN: `drawIndirect` takes four tightly packed 32-bit unsigned integers (16 bytes), `drawIndexedIndirect` five (20 bytes) in `drawIndexed` argument order, buffer needs `GPUBufferUsage.INDIRECT`, `indirectOffset` is a multiple of 4, non-zero `firstInstance` needs the `indirect-first-instance` feature (otherwise the call is a no-op); `dispatchWorkgroupsIndirect` needs INDIRECT usage and a 4-byte-aligned offset. The toji.dev indirect-draws page was fetched for the usage pattern.
Removed (not in the fetched pages): the `multi-draw-indirect` development note, per-call validation cost claim, storage/indirect cross-pass claim, dead W3C spec links. The WGSL culling shader is an illustrative sketch, not copied from a page.

Method: documentation only; no commands were run.
