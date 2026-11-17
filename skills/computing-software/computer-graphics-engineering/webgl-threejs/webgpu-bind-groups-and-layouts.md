---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-bind-groups-and-layouts
name: webgpu-bind-groups-and-layouts
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, wgsl, bind-groups, bind-group-layout, pipeline-layout, layout-auto, dynamic-offsets, uniform-buffer-alignment, wgsl-struct-layout]
level: practitioner
status: docs-checked
description: "Organise WebGPU resources with explicit bind group layouts by update frequency, avoid layout:'auto' pitfalls, use dynamic offsets for per-draw data."
sources: ["https://webgpufundamentals.org/webgpu/lessons/webgpu-bind-group-layouts.html", "https://webgpufundamentals.org/webgpu/lessons/webgpu-memory-layout.html", "https://webgpufundamentals.org/webgpu/lessons/webgpu-fundamentals.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU bind groups and layouts

**Goal:** resource binding that scales to many materials and objects with few `setBindGroup`
calls, and buffers whose JS layout matches WGSL.

## 1. Group by update frequency
```wgsl
@group(0) @binding(0) var<uniform> frame : FrameUniforms;         // per frame
@group(1) @binding(0) var<uniform> material : MaterialUniforms;   // per material
@group(1) @binding(1) var albedo : texture_2d<f32>;
@group(1) @binding(2) var samp : sampler;
@group(2) @binding(0) var<uniform> object : ObjectUniforms;       // per draw (dynamic offset)
```
Set group 0 once per pass, group 1 per material change, group 2 per draw.

## 2. Explicit layouts (avoid layout: 'auto' for shared resources)
```js
const objectBGL = device.createBindGroupLayout({ label: 'object', entries: [
  { binding: 0, visibility: GPUShaderStage.VERTEX | GPUShaderStage.FRAGMENT,
    buffer: { type: 'uniform', hasDynamicOffset: true } } ]});
const pipelineLayout = device.createPipelineLayout({ bindGroupLayouts: [frameBGL, materialBGL, objectBGL] });
```
`layout: 'auto'` makes each pipeline derive its own layout; a bind group made from a layout
created by an auto-layout pipeline cannot be used with a different pipeline. Fine for demos,
wrong when bind groups are shared across pipelines. An auto layout also encodes the shader's
needs (for example a filterable-texture binding rejects an unfilterable texture).

## 3. Dynamic offsets for per-object data
Set `hasDynamicOffset: true` on the binding in a manually created layout, then pass one
offset per dynamic binding (in binding order) to `setBindGroup`. Offsets must be a multiple of
256 in the guide's examples; a device may support smaller ones, see
`minUniformBufferOffsetAlignment` / `minStorageBufferOffsetAlignment` in the device limits.
```js
const stride = 256;
device.queue.writeBuffer(objectBuf, 0, allObjectData);       // once per frame
for (let i = 0; i < n; i++) {
  pass.setBindGroup(2, objectBG, [i * stride]);
  pass.drawIndexed(mesh[i].count, 1, mesh[i].first);
}
```
Dynamic offsets are slightly slower than static ones, because range checks happen at
`setBindGroup` time instead of bind group creation; this matters only for thousands of calls.

## 4. WGSL layout rules
- Every type has an alignment; `vec3<f32>` has 16-byte alignment, so in a matrix or array each
  vec3 gets padding.
- Struct alignment is the max of its members' alignments; array alignment is its element's
  alignment and its size is N x roundUp(align(E), size(E)).
- A silent mismatch between JS offsets and WGSL layout gives wrong data with no error. Use a
  layout helper (webgpu-utils `makeShaderDataDefinitions`) and assert sizes in JS.

## Gotchas
- Bind groups are immutable; recreate when a resource (e.g. resized render target) changes.

## Verify
- [ ] JS-side struct offsets asserted against WGSL layout.
- [ ] No pipelines use 'auto' layouts with shared bind groups.

## Checked
2026-10-31. Confirmed against WebGPU Fundamentals "Bind Group Layouts" (auto layout incompatibility,
hasDynamicOffset, per-binding offsets, 256-multiple example, minUniformBufferOffsetAlignment, dynamic offset cost),
"Memory Layout" (vec3 alignment, struct and array rules, webgpu-utils) and "Fundamentals" (layout 'auto' note). Removed
unconfirmed: default maxBindGroups, minBindingSize value, uniform array and mat3x3 byte sizes, storage-buffer
instancing advice, sampleType and usage-conflict gotchas, bind group counts.
Method: documentation only; no commands were run.
