---
id: computing-software.computer-graphics-engineering.directx.d3d12-root-signature-1-1-flags
name: d3d12-root-signature-1-1-flags
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, root-signature, root-signature-1-1, serializeversionedrootsignature, descriptor-range-flags]
level: advanced
status: docs-checked
description: "Build D3D12 root signatures with version 1.1: descriptor/data volatility flags, static vs volatile semantics, root signature flags, and versioned serialization."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/root-signature-version-1-1", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_descriptor_range_flags", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/root-signature-limits", "https://microsoft.github.io/DirectX-Specs/d3d/ResourceBinding.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root signature 1.1 flags

Version 1.1 lets you promise how descriptors and the data they point to change, so drivers
can optimise. Breaking a promise is invalid behaviour: results are undefined and can differ between hardware. The debug
layer can validate the promises, including the defaults you get when you set no flags.

## Descriptor range flags
| Flag | Promise | Use |
|---|---|---|
| (no data flag, SRV and CBV ranges) | defaults to `DATA_STATIC_WHILE_SET_AT_EXECUTE` | most material data |
| (no data flag, UAV ranges) | defaults to `DATA_VOLATILE` | UAVs, typically written |
| `DESCRIPTORS_VOLATILE` | descriptors in the heap may change after the table is set, until execution; default data assumptions still apply | bindless tables updated late |
| `DATA_VOLATILE` | data may change at any time; equivalent to 1.0 data behaviour | |
| `DATA_STATIC_WHILE_SET_AT_EXECUTE` | data does not change while the table or root descriptor is set during execution | |
| `DATA_STATIC` | data is initialised before the descriptor or table is set during recording and cannot change until the list or bundle has finished executing for the last time | constant LUTs, static meshes |
| `DESCRIPTORS_STATIC_KEEPING_BUFFER_BOUNDS_CHECKS` | static descriptors, but the driver may not promote buffers to root descriptors, so bounds checks stay | robust access |

- Without `DESCRIPTORS_VOLATILE` descriptors are static, and out-of-bounds buffer view accesses are then undefined
  (possibly a device reset). If you depend on safe out-of-bounds behaviour, mark the ranges `DESCRIPTORS_VOLATILE`.
- `DESCRIPTORS_VOLATILE` cannot be combined with `DATA_STATIC`, but can be combined with the other data flags.
  `DESCRIPTORS_VOLATILE | DATA_VOLATILE` is equivalent to root signature 1.0.
- For SM 6.6 heaps (`CBV_SRV_UAV_HEAP_DIRECTLY_INDEXED`), descriptor ranges are not used.

## Building with d3dx12 helpers
```cpp
CD3DX12_DESCRIPTOR_RANGE1 ranges[1];
ranges[0].Init(D3D12_DESCRIPTOR_RANGE_TYPE_SRV, UINT_MAX, 0, 0,
               D3D12_DESCRIPTOR_RANGE_FLAG_DESCRIPTORS_VOLATILE);          // unbounded bindless SRVs
CD3DX12_ROOT_PARAMETER1 params[3];
params[0].InitAsConstants(16, 0);                                          // b0: 16 DWORD root constants
params[1].InitAsConstantBufferView(1, 0, D3D12_ROOT_DESCRIPTOR_FLAG_DATA_STATIC_WHILE_SET_AT_EXECUTE);
params[2].InitAsDescriptorTable(1, ranges, D3D12_SHADER_VISIBILITY_PIXEL);
CD3DX12_VERSIONED_ROOT_SIGNATURE_DESC desc;
desc.Init_1_1(3, params, 1, &staticSampler,
    D3D12_ROOT_SIGNATURE_FLAG_ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT |
    D3D12_ROOT_SIGNATURE_FLAG_DENY_HULL_SHADER_ROOT_ACCESS |
    D3D12_ROOT_SIGNATURE_FLAG_DENY_DOMAIN_SHADER_ROOT_ACCESS |
    D3D12_ROOT_SIGNATURE_FLAG_DENY_GEOMETRY_SHADER_ROOT_ACCESS);
ComPtr<ID3DBlob> blob, err;
D3DX12SerializeVersionedRootSignature(&desc, D3D_ROOT_SIGNATURE_VERSION_1_1, &blob, &err);
device->CreateRootSignature(0, blob->GetBufferPointer(), blob->GetBufferSize(), IID_PPV_ARGS(&rootSig));
```
Query `D3D12_FEATURE_ROOT_SIGNATURE` (`HighestVersion`) before using 1.1. Root signature 1.2 adds
`D3D12_STATIC_SAMPLER_DESC1` and `D3D12_ROOT_SIGNATURE_DESC2` (documented in the Vulkan-on-12 spec for non-normalized
texture sampling coordinates).

## Size budget
64 DWORDs total: root constant = 1 DWORD each, root descriptor = 2, descriptor table = 1. Static samplers do not count.
Put per-draw data in root constants, frequently changing CBVs as root descriptors, everything else in tables.

## Root signature flags worth setting
- `DENY_*_SHADER_ROOT_ACCESS` for unused stages.
- `CBV_SRV_UAV_HEAP_DIRECTLY_INDEXED` / `SAMPLER_HEAP_DIRECTLY_INDEXED` for SM 6.6 bindless.
- `ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT` only if you use an input layout.

## Verify
- [ ] The serialization error blob is empty; debug-layer validation of the flags reports no violated promise.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Root signature version 1.1" and "Root signature limits"
(MicrosoftDocs/win32), `D3D12_DESCRIPTOR_RANGE_FLAGS` (MicrosoftDocs/sdk-api), DirectX-Specs ResourceBinding
(all last commits October 2026). Confirmed: flag semantics, defaults, flag combination rules, volatile out-of-bounds
behaviour, 64 DWORD costs, version 1.2 additions. Clarified: the UAV default (volatile), the
meaning of `DESCRIPTORS_STATIC_KEEPING_BUFFER_BOUNDS_CHECKS`, and the version 1.2 additions. Removed unconfirmed claims:
"1.1 on Windows 10 1607+", the "falls back to 1.0" remark on the d3dx12 helper, and "smaller root signatures are
faster to change".
Method: documentation only; no commands were run.
