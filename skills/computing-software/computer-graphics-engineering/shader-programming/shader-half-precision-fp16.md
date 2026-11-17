---
id: computing-software.computer-graphics-engineering.shader-programming.shader-half-precision-fp16
name: shader-half-precision-fp16
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-optimisation, half-precision, fp16, min16float, float16-t, packed-math, register-pressure, shaderfloat16, enable-16bit-types]
level: advanced
status: docs-checked
description: "Use 16-bit floats in shaders for speed and register savings: HLSL float16_t vs min16float, GLSL/Vulkan float16 features, packed math, and which calculations can't tolerate fp16."
sources: ["https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-scalar", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_feature_data_d3d12_options4", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GL_EXT_shader_explicit_arithmetic_types.txt", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#features-shaderFloat16"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Half precision (fp16) in shaders

**Goal:** halve register usage and double ALU throughput on hardware with packed fp16
(several desktop and mobile GPUs; check the target), without visible quality loss.

## 1. Two ways in HLSL
| type | meaning | compile |
|---|---|---|
| `min16float` | minimum 16-bit; drivers may use any greater precision | any SM; behaviour varies |
| `float16_t`, `half` with 16-bit enabled | 16-bit float | `dxc -enable-16bit-types -T ps_6_2` or later, needs `D3D12_FEATURE_DATA_D3D12_OPTIONS4::Native16BitShaderOpsSupported` |
Vulkan/GLSL: `shaderFloat16` (VkPhysicalDeviceShaderFloat16Int8Features) +
`GL_EXT_shader_explicit_arithmetic_types` (or its `_float16` variant) → `float16_t`, `f16vec3`; storage in
buffers needs `storageBuffer16BitAccess`. Or `mediump` → RelaxedPrecision (driver's choice).

## 2. Where fp16 is safe
Range ±65504, ~3.3 decimal digits (10-bit mantissa).
- Colours (HDR up to 65504 fine), normalised vectors, NdotL/NdotH, BRDF terms,
  tone mapping, post-processing kernels, blend weights.
- Packed math: some GPUs execute two fp16 lanes per instruction — vectorise in pairs to benefit (check the ISA).

## 3. Where it breaks
- Positions, depth, matrices, UVs on large textures (see precision qualifiers skill).
- `dot(v, v)` of unnormalised large vectors overflows → Inf → NaN downstream.
- Specular `pow(NdotH, 2048)` underflows to 0 early; roughness → alpha² near 0 loses all
  precision (GGX D term at low roughness): compute D in fp32 or clamp roughness.
- Accumulations over many iterations (blur sums with many taps) lose precision: accumulate
  in fp32, sample in fp16.

## 4. Conversions cost
Mixing fp16 and fp32 can insert conversion instructions; gains can vanish if the shader converts
constantly. Keep whole chains in fp16 and convert at boundaries. Use 16-bit constant buffer /
texture formats (`R16G16B16A16_FLOAT`) to feed fp16 math directly.

## 5. Measure
Check vendor ISA disassembly (for AMD, Radeon GPU Analyzer) for packed 16-bit instructions and a drop in register count. Verify GPU time and
occupancy, not just instruction counts.

## Gotchas
- Throughput gains differ by GPU; on some hardware the gain comes only from register savings.
- Denormals: fp16 denormals may flush to zero depending on hardware; very small values vanish.
- Debugging precision issues: temporarily compile with 16-bit disabled to confirm the cause.

## Verify
- [ ] Image diff (FLIP) between fp32 and fp16 builds below visibility threshold.
- [ ] ISA shows packed fp16 instructions and lower register counts in converted shaders.
- [ ] GPU time improves on target hardware (not just theoretical).

## Checked

Checked 2026-10-26 against Microsoft sdk-api (D3D12_FEATURE_DATA_D3D12_OPTIONS4) and HLSL scalar types docs, DXC SPIR-V docs and options (main, 2026-10-23), GLSL extension GL_EXT_shader_explicit_arithmetic_types, Vulkan-Docs features chapter. Confirmed: `min16float` is a minimum-precision type; `-enable-16bit-types` flag and its `half`/`float16_t` to `OpTypeFloat 16` mapping; `Native16BitShaderOpsSupported` and the shader model 6_2 requirement; `shaderFloat16` and `storageBuffer16BitAccess` features; `float16_t`/`f16vec3` types from GL_EXT_shader_explicit_arithmetic_types. Removed as unconfirmed: the NVIDIA architecture claim, the AMD packed instruction mnemonic, the Mali offline compiler remark and the per-vendor hardware list.

Method: documentation only; no commands were run.
