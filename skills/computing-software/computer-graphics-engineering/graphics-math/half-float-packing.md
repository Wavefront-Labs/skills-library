---
id: computing-software.computer-graphics-engineering.graphics-math.half-float-packing
name: half-float-packing
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-encoding, half-float-packing, fp16, half-precision, packhalf2x16, vertex-compression]
level: practitioner
status: verified
description: "Pack and unpack IEEE half floats: range and precision limits, packHalf2x16/f16tof32 intrinsics, CPU conversion with F16C, denormals and rounding, and when to use 16-bit formats."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/packHalf2x16.xhtml", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/f32tof16", "https://en.wikipedia.org/wiki/Half-precision_floating-point_format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Half float packing and unpacking

## Format (binary16)
1 sign, 5 exponent (bias 15), 10 mantissa bits.
- Max finite 65504 (65520 and above round to Inf); smallest normal 6.10e-5; smallest subnormal 5.96e-8.
- Relative precision 2^-11 (about 0.05 percent, 3.3 decimal digits). Integer spacing above 2048 is 2,
  above 4096 is 4: **world positions in half precision are unusable** beyond a few metres of mm accuracy.

## GPU
```glsl
uint packed = packHalf2x16(vec2(a, b));    // GLSL 4.20 / ES 3.0
vec2 ab = unpackHalf2x16(packed);
```
HLSL: `f32tof16(x)` returns the half in the low 16 bits of a uint, `f16tof32`. With native 16-bit
types (SM 6.2 `-enable-16bit-types`, Vulkan `shaderFloat16`) use `half`/`float16_t` directly.
Texture/vertex formats `R16G16B16A16_FLOAT`, `R16G16_FLOAT` convert in hardware.

## CPU
- x86 F16C: `_mm_cvtps_ph(v, _MM_FROUND_TO_NEAREST_INT)` and `_mm_cvtph_ps`.
- C++23 `std::float16_t`; numpy `np.float16`; ARM `__fp16`/`_Float16`.
- Software conversion must round to nearest even and handle Inf/NaN/subnormals; meshoptimizer's
  `meshopt_quantizeHalf` is a compact reference (confirm in the meshoptimizer README).

## Good uses
HDR colour (render targets up to 65504 with 0.05 percent precision), normals/tangents/UVs in vertex
buffers (UVs within [0, 1] to a few repeats), animation data, ML inference activations.

## Bad uses
Positions in large scenes, depth, accumulators (sums lose small addends quickly), texture coordinates
for large atlases (UVs in [0.5, 1) resolve to 1/2048 and those in [0.25, 0.5) to 1/4096: marginal for 4k textures, not enough for 16k).

## Verify
Round-trip a range of values through your pack/unpack and through the GPU path; compare with
`np.float16` including 65504, 65520 (overflows to Inf), 1e-5 (subnormal) and NaN.
