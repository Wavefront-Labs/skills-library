---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-tsl-compute-shaders
name: threejs-tsl-compute-shaders
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webgpurenderer, tsl, tsl-compute, storage-buffer, instancedarray, computeasync, gpu-particles]
level: advanced
status: docs-checked
description: "Run GPU compute from three.js with TSL: storage buffers via instancedArray, compute nodes dispatched with renderer.compute, reading results in materials."
sources: ["https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js TSL compute shaders

**Goal:** simulate hundreds of thousands of particles/agents on the GPU and render them
directly, without CPU round-trips.

## 1. Storage buffers
```js
import * as THREE from 'three/webgpu';
import { Fn, If, instancedArray, instanceIndex, uniform, vec3, hash, deltaTime } from 'three/tsl';
const COUNT = 200_000;
const positions  = instancedArray(COUNT, 'vec3');      // GPU storage buffer
const velocities = instancedArray(COUNT, 'vec3');
const gravity = uniform(-9.8);
```

## 2. Compute kernels
```js
const init = Fn(() => {
  const p = positions.element(instanceIndex);
  p.assign(vec3(hash(instanceIndex), hash(instanceIndex.add(1)), hash(instanceIndex.add(2))).sub(0.5).mul(10));
})().compute(COUNT);

const step = Fn(() => {
  const p = positions.element(instanceIndex), v = velocities.element(instanceIndex);
  v.y.addAssign(gravity.mul(deltaTime));
  p.addAssign(v.mul(deltaTime));
  If(p.y.lessThan(0), () => { p.y.assign(0); v.y.assign(v.y.negate().mul(0.6)); });
})().compute(COUNT);

renderer.compute(init);                                // once
renderer.setAnimationLoop(() => { renderer.compute(step); renderer.render(scene, camera); });
```
`.compute(count, workgroupSize)`: the default workgroup size is `[ 64 ]`.

## 3. Render from the buffer
Feed the buffer node into a node material input such as `positionNode` (`SpriteNodeMaterial` is one of the TSL node materials). Copy the exact binding call from the examples of the three.js release you pin.

## 4. Reading back
Reading a storage buffer back to the CPU is a GPU-to-CPU transfer: keep it out of the steady-state loop. Look up the readback method in the release you pin.

## Gotchas
- Writing to `positions.element(otherIndex)` from many threads = races; use atomics
  (`atomicAdd` and the other `atomic*` functions exist in TSL) or double-buffering.
- Compute and render share the queue; heavy kernels reduce frame rate, so measure GPU time.

## Verify
- [ ] Simulation runs at frame rate for the target COUNT on WebGPU.
- [ ] No CPU readback in the steady-state loop.

## Checked

2026-10-28. Confirmed in the three.js TSL wiki: `instancedArray(count, type)`, `.element(index)`, `Fn(...)().compute(count)`, `compute(node, count, workgroupSize = [ 64 ])`, `renderer.compute(...)`, `atomicAdd` and the other atomics, `SpriteNodeMaterial`, `positionNode`.
Removed (not in the fetched pages): `computeAsync`, `getArrayBufferAsync`, `toAttribute`, `trackTimestamp`, the WebGL2 transform-feedback fallback claims, the tail-guard claim, the r170 version note, dead example links.

Method: documentation only; no commands were run.
