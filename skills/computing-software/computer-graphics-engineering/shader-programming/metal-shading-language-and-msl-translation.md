---
id: computing-software.computer-graphics-engineering.shader-programming.metal-shading-language-and-msl-translation
name: metal-shading-language-and-msl-translation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, metal-shading-language, msl, metal, apple-gpu, spirv-cross, metal-shader-converter, moltenvk]
level: practitioner
status: draft
description: "Write and port Metal Shading Language shaders: address spaces, binding attributes, threadgroup memory, and translating HLSL/SPIR-V via SPIRV-Cross or Metal Shader Converter."
sources: ["https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf", "https://developer.apple.com/metal/shader-converter/", "https://github.com/KhronosGroup/SPIRV-Cross"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metal Shading Language (MSL)

MSL is C++14-based. Shaders are compiled to AIR with `xcrun metal` and linked into a `.metallib`.

## 1. Essentials
```metal
#include <metal_stdlib>
using namespace metal;

struct VSOut { float4 pos [[position]]; float2 uv; };

struct Uniforms { float4x4 mvp; };

vertex VSOut vs_main(uint vid [[vertex_id]],
                     const device float4* positions [[buffer(0)]],
                     constant Uniforms& u [[buffer(1)]]) {
    VSOut o; o.pos = u.mvp * positions[vid]; o.uv = positions[vid].xy * 0.5 + 0.5; return o;
}

fragment half4 fs_main(VSOut in [[stage_in]],
                       texture2d<half> tex [[texture(0)]],
                       sampler s [[sampler(0)]]) {
    return tex.sample(s, in.uv);
}

kernel void cs_main(device float* data [[buffer(0)]],
                    uint gid [[thread_position_in_grid]],
                    threadgroup float* scratch [[threadgroup(0)]]) { /* ... */ }
```
Address spaces: `device` (read/write buffers), `constant` (uniform, cached, size known), `thread`,
`threadgroup` (shared memory), `threadgroup_imageblock` (tile memory on Apple GPUs).

## 2. Building
```bash
xcrun -sdk macosx metal -c shader.metal -o shader.air -gline-tables-only -frecord-sources
xcrun -sdk macosx metallib shader.air -o shader.metallib
```
`-frecord-sources` lets the Xcode GPU debugger show source. Use `-sdk iphoneos` for iOS.

## 3. Translating from HLSL or SPIR-V
- **SPIRV-Cross**: `spirv-cross shader.spv --msl --msl-version 20100 --output shader.metal`.
  Options for argument buffers (`--msl-argument-buffers`), decoration-driven bindings, iOS vs
  macOS (`--msl-ios`). MoltenVK uses this path at runtime.
- **Metal Shader Converter** (Apple): converts DXIL (from DXC) directly to a metallib, with a
  runtime header to emulate D3D12 root signatures via argument buffers. Preferred for D3D12 ports.
  `metal-shaderconverter shader.dxil -o shader.metallib`.

## 4. Porting gotchas
| HLSL/GLSL habit | MSL reality |
|---|---|
| `half` is float on desktop | `half` is real 16-bit on Apple GPUs; use it for colour math, it doubles ALU throughput |
| bindings by set/binding | bindings by `[[buffer(n)]]`, `[[texture(n)]]` index per stage, or argument buffers |
| `float3` in buffers is 12 bytes | `float3` is 16 bytes in MSL; use `packed_float3` to match a CPU layout |
| implicit derivatives in compute | not available; compute uses explicit LOD |
| push constants | `setVertexBytes`/`setFragmentBytes` (up to 4 KB) |

## Gotchas
- Vertex buffer indices share the `[[buffer(n)]]` space with other buffers; translators offset one
  set to avoid collisions; keep your own layout consistent.
- Function constants (`[[function_constant(0)]]`) are Metal's specialisation constants; prefer them
  over preprocessor permutations to reduce library size.

## Verify
- [ ] `xcrun metal` builds with `-Werror` clean.
- [ ] Translated shaders validated in Xcode GPU frame capture (shader validation enabled).
