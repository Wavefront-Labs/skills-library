---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-timestamp-queries
name: webgpu-timestamp-queries
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, webgpu-timestamp-query, gpu-profiling, query-set, resolvequeryset]
level: advanced
status: docs-checked
description: "Measure GPU pass times in WebGPU with timestamp-query: feature request, timestampWrites on passes, resolveQuerySet, readback without stalls, and precision caveats."
sources: ["https://developer.chrome.com/blog/new-in-webgpu-121", "https://webgpufundamentals.org/webgpu/lessons/webgpu-timing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU timestamp queries

## 1. Enable
```js
const adapter = await navigator.gpu.requestAdapter();
const canTime = adapter.features.has('timestamp-query');
const device = await adapter.requestDevice({ requiredFeatures: canTime ? ['timestamp-query'] : [] });
```

## 2. Record per pass
```js
const qs = device.createQuerySet({ type: 'timestamp', count: 2 });
const resolve = device.createBuffer({ size: 16, usage: GPUBufferUsage.QUERY_RESOLVE | GPUBufferUsage.COPY_SRC });
const result = device.createBuffer({ size: 16, usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ });

const pass = enc.beginRenderPass({ colorAttachments: [...],
  timestampWrites: { querySet: qs, beginningOfPassWriteIndex: 0, endOfPassWriteIndex: 1 } });
// ... draw ... pass.end();
enc.resolveQuerySet(qs, 0, 2, resolve, 0);
if (result.mapState === 'unmapped') enc.copyBufferToBuffer(resolve, 0, result, 0, 16);
device.queue.submit([enc.finish()]);
if (result.mapState === 'unmapped') result.mapAsync(GPUMapMode.READ).then(() => {
  const t = new BigUint64Array(result.getMappedRange());
  gpuMs = Number(t[1] - t[0]) / 1e6;     // nanoseconds
  result.unmap();
});
```
Compute passes take the same `timestampWrites`. Skip the copy while the result buffer is still
mapped (pending) instead of stalling; use a small ring of result buffers for every-frame numbers.

## 3. Interpreting
- Values are nanoseconds (resolved as 64-bit unsigned integers) but are quantised to 100 microseconds because of timing-attack concerns; in Chrome the "WebGPU Developer Features" flag (chrome://flags/#enable-webgpu-developer-features) disables quantisation during development. Average over many frames.

## Gotchas
- GPUs may reset the timestamp counter occasionally, giving negative deltas between timestamps; discard those samples.
- Always feature-detect `timestamp-query` and hide the GPU timer UI otherwise.

## Verify
- [ ] Reported GPU ms grows proportionally when doubling resolution of a fill-bound pass.
- [ ] No frame waits on mapAsync (CPU timeline stays smooth).

## Checked

2026-10-28. Confirmed in the Chrome "What's New in WebGPU 121" post and webgpufundamentals timing lesson: `timestamp-query` feature, `timestampWrites` with `beginningOfPassWriteIndex` / `endOfPassWriteIndex`, `resolveQuerySet`, results as nanoseconds in 64-bit unsigned integers (skill's `BigInt64Array` corrected to `BigUint64Array`), 100 microsecond quantisation and the developer-features flag, negative deltas after counter resets.
Removed (not in the fetched pages): `writeTimestamp` removal claim, tiler overlap claim, Safari/Firefox support claim, the "zero or negative on power-state changes" wording, dead W3C spec link.

Method: documentation only; no commands were run.
