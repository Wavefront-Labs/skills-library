---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-buffers-mapasync-writebuffer
name: webgpu-buffers-mapasync-writebuffer
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, mapasync, writebuffer, mappedatcreation, staging-buffer, gpubufferusage]
level: practitioner
status: docs-checked
description: "Create and update WebGPU buffers efficiently: usage flags, mappedAtCreation, queue.writeBuffer vs staging buffers, mapAsync readback, alignment and size rules."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/GPUQueue/writeBuffer", "https://developer.mozilla.org/en-US/docs/Web/API/GPUBuffer/mapAsync", "https://toji.dev/webgpu-best-practices/buffer-uploads"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU buffers: creation, writeBuffer and mapAsync

## 1. Creation with initial data
```js
const vbuf = device.createBuffer({ size: verts.byteLength, usage: GPUBufferUsage.VERTEX, mappedAtCreation: true });
new Float32Array(vbuf.getMappedRange()).set(verts);
vbuf.unmap();
```
Static data: `mappedAtCreation: true` fills the buffer at creation (see the toji.dev buffer-uploads page for the trade-offs).

## 2. Per-frame updates: queue.writeBuffer
```js
const ubo = device.createBuffer({ size: 256, usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST });
device.queue.writeBuffer(ubo, 0, uniformsF32);          // data size and buffer offset: multiples of 4 bytes (MDN)
device.queue.writeBuffer(ubo, 64, data, srcOffsetElems, sizeElems);
```
`writeBuffer` is the simple path for uniforms and small updates; use a staging buffer only when profiling shows a need.

## 3. Staging ring (large streaming uploads)
Create `MAP_WRITE | COPY_SRC` staging buffers (the usage pair toji.dev uses), map and fill them, `unmap`, then `encoder.copyBufferToBuffer(staging, 0, dst, 0, size)`. Re-map staging buffers after the submit completes.

## 4. Readback
```js
const read = device.createBuffer({ size, usage: GPUBufferUsage.MAP_READ | GPUBufferUsage.COPY_DST });
enc.copyBufferToBuffer(src, 0, read, 0, size);
device.queue.submit([enc.finish()]);
await read.mapAsync(GPUMapMode.READ);
const out = new Float32Array(read.getMappedRange().slice(0));   // copy before unmap
read.unmap();
```
Read-mode mapping needs a `MAP_READ` buffer and write-mode mapping a `MAP_WRITE` buffer; the mapped range size must be a multiple of 4 (MDN). The toji.dev read-back staging buffer uses `MAP_READ | COPY_DST`, so copy into it rather than mapping a storage buffer.

## 5. Rules
- `writeBuffer`: data size and `bufferOffset` are multiples of 4 bytes.
- `mapAsync`: the mapped range is a multiple of 4; never await a map synchronously every frame in the render loop.

## Verify
- [ ] No validation errors on misaligned writes.
- [ ] Readback values match CPU reference.

## Checked

2026-10-28. Confirmed on MDN (GPUQueue.writeBuffer, GPUBuffer.mapAsync): 4-byte multiples for data size, buffer offset and mapped range; MAP_READ and MAP_WRITE usage required for the two map modes. Confirmed on toji.dev buffer-uploads: MAP_WRITE | COPY_SRC and MAP_READ | COPY_DST staging buffers.
Removed (not in the fetched pages): mappedAtCreation size rule and cheapest-path claim, immediate-copy claim, copyBufferToTexture 256-byte rule, detached-range claim, `minUniformBufferOffsetAlignment` figure, `destroy()` claim, dead W3C spec link.

Method: documentation only; no commands were run.
