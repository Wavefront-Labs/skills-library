---
id: computing-software.computer-graphics-engineering.directx.d3d12-view-creation-cbv-srv-uav-rtv-dsv
name: d3d12-view-creation-cbv-srv-uav-rtv-dsv
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-binding, createshaderresourceview, cbv-srv-uav-views, rtv-dsv]
level: practitioner
status: docs-checked
description: "Fill D3D12 view descriptors correctly: CBV alignment, typed/structured/raw buffer SRVs and UAVs with counters, texture mip/array ranges, RTVs and read-only DSVs."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/creating-descriptors", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-createunorderedaccessview", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_shader_resource_view_desc", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/uav-counters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating CBV / SRV / UAV / RTV / DSV views

## CBV
```cpp
D3D12_CONSTANT_BUFFER_VIEW_DESC cbv = { buf->GetGPUVirtualAddress() + off, AlignUp(size, 256) };
device->CreateConstantBufferView(&cbv, handle);
```
Place constant data at 256-byte alignment (`D3D12_CONSTANT_BUFFER_DATA_PLACEMENT_ALIGNMENT`).

## Buffer SRVs
```cpp
D3D12_SHADER_RESOURCE_VIEW_DESC s = {};
s.ViewDimension = D3D12_SRV_DIMENSION_BUFFER;
s.Shader4ComponentMapping = D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING;   // set explicitly
// StructuredBuffer<T>:
s.Format = DXGI_FORMAT_UNKNOWN; s.Buffer.StructureByteStride = sizeof(T);
s.Buffer.FirstElement = first; s.Buffer.NumElements = count;
// ByteAddressBuffer (raw):
// s.Format = DXGI_FORMAT_R32_TYPELESS; s.Buffer.Flags = D3D12_BUFFER_SRV_FLAG_RAW; NumElements = bytes/4
// Buffer<float4> (typed): s.Format = DXGI_FORMAT_R32G32B32A32_FLOAT
```

## Texture SRVs
```cpp
s.ViewDimension = D3D12_SRV_DIMENSION_TEXTURE2DARRAY;
s.Format = DXGI_FORMAT_R8G8B8A8_UNORM_SRGB;           // may differ from resource if typeless family
s.Texture2DArray = { /*MostDetailedMip*/0, /*MipLevels*/(UINT)-1, /*FirstArraySlice*/0, /*ArraySize*/6, 0, 0.0f };
```
Depth resources: create as `R32_TYPELESS` (for `D32_FLOAT`) so you can make a `D32_FLOAT` DSV and
an `R32_FLOAT` SRV. For D24S8: `R24G8_TYPELESS` -> SRV `R24_UNORM_X8_TYPELESS` (depth) or
`X24_TYPELESS_G8_UINT` with `PlaneSlice = 1` (stencil).

## UAVs
```cpp
D3D12_UNORDERED_ACCESS_VIEW_DESC u = {};
u.ViewDimension = D3D12_UAV_DIMENSION_BUFFER; u.Format = DXGI_FORMAT_UNKNOWN;
u.Buffer.NumElements = n; u.Buffer.StructureByteStride = sizeof(T);
u.Buffer.CounterOffsetInBytes = counterOff;      // AppendStructuredBuffer/ConsumeStructuredBuffer counter
device->CreateUnorderedAccessView(buf, counterBuf /* or null */, &u, handle);
```
The counter offset must be aligned to `D3D12_UAV_COUNTER_PLACEMENT_ALIGNMENT` (4096). Texture UAVs
bind one mip (`Texture2D.MipSlice`).

## RTV / DSV
```cpp
D3D12_DEPTH_STENCIL_VIEW_DESC d = { DXGI_FORMAT_D32_FLOAT, D3D12_DSV_DIMENSION_TEXTURE2D,
                                    D3D12_DSV_FLAG_READ_ONLY_DEPTH };   // read-only DSV: depth test while sampling as SRV
```
RTVs/DSVs live in non-shader-visible RTV/DSV heaps.

## Gotchas
- A null `pDesc` creates a default view from the resource description; supply a description for
  typeless resources and for buffers (the UAV function needs a valid description for buffers).
- Build `Shader4ComponentMapping` with `D3D12_ENCODE_SHADER_4_COMPONENT_MAPPING` or use the default macro.

## Verify
- [ ] Debug layer clean on view creation; PIX resource view inspection shows expected formats and ranges.

## Checked

2026-10-26. Checked against the Microsoft Learn Creating descriptors page, the CreateShaderResourceView,
CreateUnorderedAccessView and D3D12_BUFFER_UAV reference pages, the d3d12.h constants
(D3D12_UAV_COUNTER_PLACEMENT_ALIGNMENT 4096, D3D12_CONSTANT_BUFFER_DATA_PLACEMENT_ALIGNMENT 256,
D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING) and the DXGI_FORMAT list (win32, sdk-api and DirectX-Headers repositories,
commits to 2026-10). Removed the unconfirmed 64 KB size cap, sRGB-UAV prohibition, zero-mapping bug claim and
null-descriptor read-zero claim.
Method: documentation only; no commands were run.
