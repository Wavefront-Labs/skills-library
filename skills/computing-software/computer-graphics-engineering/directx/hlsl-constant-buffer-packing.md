---
id: computing-software.computer-graphics-engineering.directx.hlsl-constant-buffer-packing
name: hlsl-constant-buffer-packing
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, hlsl, cbuffer-packing, packoffset, constant-buffer-layout, 16-byte-boundary, structuredbuffer, constantbuffer-template, dxc-reflection]
level: practitioner
status: docs-checked
description: "Match C++ structs to HLSL cbuffer layout: the 16-byte register boundary rule, array padding, matrix majorness, packoffset, and reflection checks to catch drift."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-packing-rules", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-variable-packoffset", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-appendix-pre-pragma-pack-matrix", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLSL constant buffer packing

**Goal:** CPU structs and HLSL `cbuffer`s agree byte-for-byte across DXC, FXC and
SPIR-V targets.

## 1. The rules
Constant buffers are arrays of 16-byte registers (float4).
- A member **may not straddle** a 16-byte boundary; if it would, it starts at the next one.
  `float3 a; float b;` packs into one register; `float b; float3 a;` also fits
  (a at offset 4, ending exactly at 16). `float2 b; float3 a;` would straddle (8 + 12 = 20),
  so `a` moves to offset 16 and 8 bytes are wasted.
- **Every array element starts on a 16-byte boundary**: `float w[8]` occupies 8 registers.
- A structure forces the next variable to start on the next four-component vector.
- Matrices are **column-major** by default in HLSL (`#pragma pack_matrix` default `column_major`):
  a `float4x4` from row-major C++ (DirectXMath) must be transposed on upload, or declare
  `row_major float4x4`, or compile with `-Zpr` (fxc `/Zpr`).

## 2. Mirror in C++
```cpp
struct alignas(16) PerObject {
    DirectX::XMFLOAT4X4 world;        // 0
    DirectX::XMFLOAT3   tint;  float roughness;   // 64 - packed together
    DirectX::XMFLOAT4   weights[2];   // 80  (instead of float weights[8])
};
static_assert(sizeof(PerObject) % 16 == 0);
static_assert(offsetof(PerObject, weights) == 80);
```
```hlsl
cbuffer PerObject : register(b1) {
    float4x4 world;
    float3   tint;   float roughness;
    float4   weights[2];          // read weights[i >> 2][i & 3]
};
```

## 3. packoffset (explicit placement)
`float roughness : packoffset(c4.w);` pins a member to register 4, component w. Useful when
sharing a layout with legacy code; otherwise prefer natural ordering + asserts.

## 4. Alternatives
- `ConstantBuffer<T>` declares a constant buffer from a struct type.
- `StructuredBuffer<T>` has its own element layout; in DXC SPIR-V output cbuffers default to
  vector-relaxed `std140` and structured buffers to `std430`.
- DXC `-fvk-use-dx-layout` makes SPIR-V output use DirectX layout rules (it needs
  `VK_EXT_scalar_block_layout` on the application side).

## 5. Check automatically
DXC reflection (`IDxcUtils::CreateReflection` → `ID3D12ShaderReflectionConstantBuffer::
GetVariableByName` → `D3D12_SHADER_VARIABLE_DESC::StartOffset`) in a unit test or at load in debug
builds; assert against C++ `offsetof`.

## Gotchas
- Use 4-byte types such as `uint32_t` for flags shared with the CPU rather than C++ `bool`.
- `-enable-16bit-types` enables 16-bit types, which can change layouts; re-check offsets.

## Verify
- [ ] Reflection-vs-offsetof test passes for every cbuffer.
- [ ] PIX buffer view shows expected values for every member.
- [ ] Same shader compiled for SPIR-V with `-fvk-use-dx-layout` reads identical data.

## Checked

2026-10-26. Checked against the Microsoft Learn HLSL packing rules, packoffset and pack_matrix pages, the DirectXMath matrix
convention note, docs/SPIR-V.rst (layout options and std140/std430 defaults), include/dxc/dxcapi.h (CreateReflection) and
the d3d12shader reference (win32, sdk-api and DirectXShaderCompiler repositories, commits to 2026-10). Confirmed:
no straddling of a 16-byte vector, array elements at vector starts, structure forces next variable to a new vector,
column_major default, -Zpr/-Zpc, -fvk-use-dx-layout. Removed the unconfirmed float3x3 size, bool size, half packing,
reflection-stripping and StructuredBuffer performance claims.
Method: documentation only; no commands were run.
