---
id: computing-software.computer-graphics-engineering.shader-programming.slang-shading-language
name: slang-shading-language
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, slang, slangc, shader-modules, generics, autodiff]
level: advanced
status: docs-checked
description: "Write shaders in Slang: modules, interfaces and generics, compile with slangc to SPIR-V/DXIL/MSL/WGSL, reflection API, and automatic differentiation."
sources: ["https://shader-slang.org/slang/user-guide/", "https://github.com/shader-slang/slang/blob/master/docs/command-line-slangc-reference.md", "https://shader-slang.org/slang/user-guide/autodiff.html", "https://shader-slang.org/slang/user-guide/compiling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slang shading language

Slang is HLSL-compatible with modules, generics and interfaces, compiling to
SPIR-V, DXIL, Metal, WGSL, CUDA and CPU.

## 1. Modules and interfaces
```slang
// lights.slang
module lights;
public interface ILight { public float3 illuminate(float3 p, float3 n); }
public struct PointLight : ILight {
  public float3 pos; public float3 color;
  public float3 illuminate(float3 p, float3 n) { float3 l = pos - p; return color * max(dot(n, normalize(l)), 0) / dot(l, l); }
}
```
```slang
// shade.slang
import lights;
float3 shade<L : ILight>(L light, float3 p, float3 n) { return light.illuminate(p, n); }
```
Generics are specialised at compile time: no dynamic dispatch cost.

## 2. Compile
```bash
slangc shade.slang -target spirv -entry fsMain -stage fragment -o shade.spv
slangc shade.slang -target dxil -profile sm_6_6 -entry fsMain -stage fragment -o shade.dxil
slangc shade.slang -target metal -entry fsMain -o shade.metal
slangc shade.slang -target wgsl -entry fsMain -stage fragment -o shade.wgsl
```
With `[shader("fragment")]` attributes slangc can infer `-entry` and `-stage` only for SPIR-V, Metal, CUDA and OptiX targets; for HLSL, DXIL, WGSL and others keep passing `-entry` and `-stage`.

## 3. Reflection and parameter blocks
`ParameterBlock<Material>` groups parameters (one descriptor set on Vulkan). Reflection is available only through the compilation API (`IComponentType::getLayout()`), not from the `slangc` command line; it gives offsets and bindings per target.

## 4. Autodiff
```slang
[Differentiable] float loss(float x) { return x * x; }
DifferentialPair<float> dp = diffPair(3.0);
bwd_diff(loss)(dp, 1.0);     // dp.d == 6
```
Used for differentiable rendering and neural shading.

## Gotchas
- Check reflection for layout: packing and matrix layout follow the target.
- Module caching: `slangc my_library.slang -o my_library.slang-module` precompiles a module.

## Verify
- [ ] Same entry point compiled to two targets renders identical reference images.

## Checked

Checked 2026-10-26 against Slang user guide and slangc reference (main branch, October 2026). Confirmed: `-target` values `spirv`, `dxil`, `metal`, `wgsl` and the `-stage fragment`/`pixel` names in the slangc reference; the `[shader()]` attribute inference limits for `-entry`/`-stage` (user guide, compiling chapter); `.slang-module` output; `-profile sm_6_x` naming; `fwd_diff`/`bwd_diff`, `DifferentialPair`, `diffPair` and `[Differentiable]` (autodiff chapter); `getLayout()` is the reflection entry point and is API-only; `module`/`import`/`public` (modules chapter). Corrected: DXIL and WGSL examples now pass `-stage`; removed unconfirmed 'Khronos-hosted', 'one layout works everywhere' and version-pinning remarks.

Method: documentation only; no commands were run.
