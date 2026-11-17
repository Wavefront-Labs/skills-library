---
id: computing-software.computer-graphics-engineering.directx.hlsl-core-intrinsics-and-math
name: hlsl-core-intrinsics-and-math
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, hlsl, hlsl-intrinsics, saturate, texture-sampling-hlsl]
level: practitioner
status: docs-checked
description: "Know the HLSL intrinsics that matter: saturate/lerp/mad, rcp/rsqrt, bit ops, f16tof32 packing, derivatives, texture Sample/Load/Gather variants, and GLSL equivalents."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-pow", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-ddx", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-fmod", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_SM_6_6_Derivatives.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLSL core intrinsics

## Math
| HLSL | GLSL | Note |
|---|---|---|
| `saturate(x)` | `clamp(x,0,1)` | free output modifier on most GPUs |
| `lerp(a,b,t)` | `mix` | |
| `mad(a,b,c)` | `fma`-ish | multiply-add |
| `frac(x)` | `fract` | |
| `rcp(x)`, `rsqrt(x)` | `1.0/x`, `inversesqrt` | reciprocal, reciprocal square root |
| `fmod(x,y)` | `mod` differs! | check negative operands against both definitions |
| `atan2(y,x)` | `atan(y,x)` | |
| `mul(a,b)` | `*` | matrix/vector product; order matters (see matrix layout) |
| `ddx/ddy`, `ddx_fine/coarse`, `fwidth` | `dFdx/dFdy` | pixel shaders; SM 6.6 adds quad derivatives to compute, mesh and amplification shaders |
| `clip(x)` | `if (x<0) discard;` | |
| `asuint/asfloat` | `floatBitsToUint/uintBitsToFloat` | |
| `f32tof16/f16tof32` | `packHalf2x16` parts | 16-bit packing in uint |
| `countbits, firstbithigh, firstbitlow, reversebits` | `bitCount, findMSB, findLSB, bitfieldReverse` | |

## Texture methods
```hlsl
Texture2D<float4> tex : register(t0); SamplerState s : register(s0);
SamplerComparisonState sc : register(s1); Texture2D<float> shadow : register(t1);
tex.Sample(s, uv);                         // implicit LOD (PS only, or CS with derivatives)
tex.SampleLevel(s, uv, lod);               // explicit LOD, any stage
tex.SampleGrad(s, uv, ddx(uv), ddy(uv));   // explicit gradients (e.g. inside divergent branches)
tex.SampleBias(s, uv, bias);
tex.Load(int3(px, mip));                   // texelFetch
tex.Gather(s, uv);                         // 4 texels' red channel (GatherGreen/Blue/Alpha)
shadow.SampleCmpLevelZero(sc, uv, depthRef);   // hardware PCF
tex.GetDimensions(mip, w, h, levels);
tex.CalculateLevelOfDetail(s, uv);
```

## Precision and speed
- `pow(x, y)` returns NaN for x < 0 (HLSL `pow` reference table); clamp the base if it can be negative.
- Guard `normalize` against zero-length vectors.
- `sincos(x, s, c)` computes sine and cosine together.

## Gotchas
- `Sample` needs derivatives; inside divergent control flow use `SampleGrad` or `SampleLevel`.
- `fmod` and GLSL `mod` can differ for negative operands, which matters for ported tiling code.

## Verify
- [ ] Ported shaders produce identical images to GLSL references (image diff) including negative-coordinate tiling.

## Checked

2026-10-26. Checked against the Microsoft Learn HLSL intrinsic pages for ddx (pixel-shader only), pow (NaN for negative base),
fmod and the DirectX-Specs SM 6.6 derivatives spec (win32 and DirectX-Specs repositories, commits to 2026-10).
Confirmed: ddx is pixel-shader only in the base docs and SM 6.6 extends derivatives to compute, mesh and amplification;
pow(x<0) is NaN. Removed the unconfirmed claims on mad fusing, rcp/rsqrt approximation, fmod versus GLSL floor
semantics, GetDimensions speed, trig rate and integer division cost.
Method: documentation only; no commands were run.
