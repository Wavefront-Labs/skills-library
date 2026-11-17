---
id: computing-software.computer-graphics-engineering.directx.hlsl-matrix-layout-and-mul-order
name: hlsl-matrix-layout-and-mul-order
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, hlsl, row-major-matrices, hlsl-mul, pack-matrix]
level: practitioner
status: docs-checked
description: "Get HLSL matrices right: column_major default packing vs row_major, mul(v, M) vs mul(M, v), DirectXMath/GLM interop, and the transpose-on-upload trap."
sources: ["https://learn.microsoft.com/en-us/windows/win32/dxmath/pg-xnamath-getting-started", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-appendix-pre-pragma-pack-matrix", "https://learn.microsoft.com/en-us/windows/win32/direct3dtools/dx-graphics-tools-fxc-syntax", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLSL matrix layout and mul order

Two independent conventions get mixed up:
1. **Packing** (how 16 floats in memory map to rows/columns): `column_major` (HLSL default) or `row_major`.
2. **Math convention** (row vectors `v * M` or column vectors `M * v`): decided by which side of
   `mul` the vector goes.

## The combinations
| CPU library | Stored as | HLSL declaration | Shader |
|---|---|---|---|
| DirectXMath (row vectors, row-major storage) | `XMMATRIX` as-is | `row_major float4x4 M;` | `mul(v, M)` |
| DirectXMath, uploaded transposed (`XMMatrixTranspose`) | transposed | default `float4x4 M;` (column_major) | `mul(v, M)` |

The middle row is the classic sample-code pattern: DirectXMath matrices are transposed on
upload *because* HLSL's default packing is column-major; the math stays `mul(v, M)`.

Rule of thumb: memory bytes of a row-vector matrix with row-major packing equal the bytes of
the column-vector transpose with column-major packing. So "transpose on upload" and "flip
mul order" are equivalent fixes; do exactly one of them.

## Setting packing
```hlsl
#pragma pack_matrix(row_major)            // file-wide
row_major float4x4 gWorld;                // per variable
```
DXC: `-Zpr` (row major) / `-Zpc` (column major) command-line defaults.

## Performance note
Pick one convention for clarity and use it everywhere.

## Debugging a wrong matrix
- Translation in the wrong place (object moves diagonally or vanishes): packing/order mismatch.
- Test with a pure translation matrix (1,2,3): in PIX, inspect the cbuffer; row-vector convention
  expects translation in the last *row* of the logical matrix.

## Gotchas
- Constant-buffer sizes of non-square matrices differ from what a C++ struct assumes; check
  offsets with reflection.
- SPIR-V via DXC flips the meaning: DXC maps HLSL `row_major` to SPIR-V `ColMajor` decorations to
  preserve semantics; let the compiler handle it, don't double-transpose for Vulkan.

## Verify
- [ ] Translation-only and rotation-only test matrices render objects where expected; only one transpose exists in the pipeline.

## Checked

2026-10-26. Checked against the DirectXMath getting-started page (row-major matrices, row vectors, pre-multiplication) and the
D3DX migration note on transposing for column-major shaders, the HLSL pack_matrix page (column_major default), the fxc
options (/Zpr, /Zpc) and docs/SPIR-V.rst (row_major/column_major translated to ColMajor/RowMajor decorations) (win32
and DirectXShaderCompiler repositories, commits to 2026-10). Removed the unconfirmed GLM row, mul performance claim
and non-square cbuffer register claim.
Method: documentation only; no commands were run.
