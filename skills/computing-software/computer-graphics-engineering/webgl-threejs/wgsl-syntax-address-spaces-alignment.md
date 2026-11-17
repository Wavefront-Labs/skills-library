---
id: computing-software.computer-graphics-engineering.webgl-threejs.wgsl-syntax-address-spaces-alignment
name: wgsl-syntax-address-spaces-alignment
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, wgsl, wgsl-alignment, address-spaces, wgsl-structs, uniformity-analysis]
level: practitioner
status: docs-checked
description: "Write correct WGSL: types and declarations, select(), struct and array alignment and padding, and mirroring layouts in JS."
sources: ["https://webgpufundamentals.org/webgpu/lessons/webgpu-wgsl.html", "https://webgpufundamentals.org/webgpu/lessons/webgpu-memory-layout.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WGSL syntax, address spaces and alignment

## 1. Syntax essentials
```wgsl
struct VSOut { @builtin(position) pos: vec4f, @location(0) uv: vec2f };
@group(0) @binding(0) var<uniform> u: Uniforms;
@group(0) @binding(1) var tex: texture_2d<f32>;
@group(0) @binding(2) var samp: sampler;
@vertex fn vs(@location(0) p: vec3f, @location(1) uv: vec2f) -> VSOut {
  var o: VSOut; o.pos = u.viewProj * vec4f(p, 1.0); o.uv = uv; return o;
}
@fragment fn fs(i: VSOut) -> @location(0) vec4f { return textureSample(tex, samp, i.uv); }
```
- No implicit conversions between `i32` and `f32`: write `f32(a) + b`; `1` is an `i32` and `2.0` an `f32`. `vec3f` is the alias of `vec3<f32>`.
- `select(falseExpression, trueExpression, condition)` replaces the ternary operator.

## 2. Alignment (uniform and storage)
- Every type has an alignment: it must start at a multiple of that many bytes. `vec3<f32>` has alignment 16, so each `vec3<f32>`, whether in a matrix or an array, ends up with extra space.
- Struct alignment is the maximum of its members' alignments; struct size is the end of the last member rounded up to the struct alignment.
- `array<E, N>` has alignment `AlignOf(E)` and size `N * roundUp(AlignOf(E), SizeOf(E))`.
- Arrays and structs follow their own rules, so a single-`vec3f` array and a single-`vec3f` struct are laid out differently.
Mirror the layout in JS with explicit offsets, or use a layout helper (webgpu-utils `makeShaderDataDefinitions`).

## Verify
- [ ] Struct sizes asserted in JS against the WGSL layout rules.

## Checked
2026-11-01. Confirmed against WebGPU Fundamentals (WGSL lesson: no implicit i32/f32 conversion, select; memory-layout lesson: alignment rules, struct and array formulas, vec3 alignment 16, makeShaderDataDefinitions). Removed: the W3C spec links (page not readable by the fetch tool), address-space table, 64 KB binding limit, per-type size figures, uniformity-error and interpolation notes, getCompilationInfo check.
Method: documentation only; no commands were run.
