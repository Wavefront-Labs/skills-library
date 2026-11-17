---
id: computing-software.computer-graphics-engineering.directx.d3d11-srv-and-uav-views
name: d3d11-srv-and-uav-views
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d11, d3d11-srv, d3d11-uav, read-write-hazard]
level: practitioner
status: docs-checked
description: "Create and bind D3D11 shader resource and unordered access views, avoid the automatic unbinding of read/write hazards, and use structured, raw and typed buffers."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-resources-buffers-intro", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-resources-limits", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/typed-unordered-access-view-loads", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-omsetrendertargetsandunorderedaccessviews", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createunorderedaccessview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D11 SRVs and UAVs

## Structured buffer with both views
```cpp
D3D11_BUFFER_DESC bd = {};
bd.ByteWidth = sizeof(Particle) * N;
bd.Usage = D3D11_USAGE_DEFAULT;
bd.BindFlags = D3D11_BIND_SHADER_RESOURCE | D3D11_BIND_UNORDERED_ACCESS;
bd.MiscFlags = D3D11_RESOURCE_MISC_BUFFER_STRUCTURED;
bd.StructureByteStride = sizeof(Particle);
device->CreateBuffer(&bd, nullptr, &buf);
D3D11_SHADER_RESOURCE_VIEW_DESC sd = {}; sd.Format = DXGI_FORMAT_UNKNOWN;
sd.ViewDimension = D3D11_SRV_DIMENSION_BUFFER; sd.Buffer.NumElements = N;
device->CreateShaderResourceView(buf.Get(), &sd, &srv);
D3D11_UNORDERED_ACCESS_VIEW_DESC ud = {}; ud.Format = DXGI_FORMAT_UNKNOWN;
ud.ViewDimension = D3D11_UAV_DIMENSION_BUFFER; ud.Buffer.NumElements = N;
ud.Buffer.Flags = D3D11_BUFFER_UAV_FLAG_APPEND;      // optional: Append/Consume counter
device->CreateUnorderedAccessView(buf.Get(), &ud, &uav);
```
Raw buffers: `MiscFlags = D3D11_RESOURCE_MISC_BUFFER_ALLOW_RAW_VIEWS`, view format
`DXGI_FORMAT_R32_TYPELESS` with `D3D11_BUFFEREX_SRV_FLAG_RAW` (SRV via `BufferEx`) /
`D3D11_BUFFER_UAV_FLAG_RAW`. Typed buffers: a real format, no structured flag.

## Binding
```cpp
ctx->CSSetUnorderedAccessViews(0, 1, uav.GetAddressOf(), &initialCount);   // -1 keeps counter
ctx->Dispatch(groups, 1, 1);
ID3D11UnorderedAccessView* nullUav = nullptr;
ctx->CSSetUnorderedAccessViews(0, 1, &nullUav, nullptr);                   // unbind before reading as SRV
ctx->VSSetShaderResources(0, 1, srv.GetAddressOf());
```
Pixel shader UAVs bind together with render targets:
`OMSetRenderTargetsAndUnorderedAccessViews` (slots start after the RTVs).

## The automatic hazard unbinding
A resource cannot be bound for read and write at the same time:
binding it as UAV/RTV with `OMSetRenderTargetsAndUnorderedAccessViews` unbinds conflicting SRVs,
compute-shader UAVs and stream-output targets. Always explicitly unbind outputs before binding as
inputs and vice versa.

## Gotchas
- Compute-shader UAV slots: `D3D11_PS_CS_UAV_REGISTER_COUNT` (8); cs_4_0/cs_4_1 have only one UAV.
  Typed UAV loads are required only for `R32_FLOAT`, `R32_UINT` and `R32_SINT`; other formats need
  `TypedUAVLoadAdditionalFormats` (and `D3D11_FORMAT_SUPPORT2_UAV_TYPED_LOAD` per format).
- `StructureByteStride` must match the format size you use for views of the buffer.

## Verify
- [ ] Debug layer shows no resource-binding hazard warnings.

## Checked

2026-10-26. Checked against Microsoft Learn: resource limits table, typed UAV loads page, OMSetRenderTargetsAndUnorderedAccessViews,
CSSetUnorderedAccessViews, D3D11_BUFFER_DESC and D3D11_BUFFEREX_SRV_FLAG (win32 and sdk-api repositories, commits to
2026-10). Confirmed: 8 compute UAV slots and 1 on cs_4_x, typed-load format list and caps bit, -1 keeps the counter,
conflicting views are unbound by the OM set call. Removed the unconfirmed 64-UAV figure, stride-multiple-of-4 rule and
structured-buffer padding claim.
Method: documentation only; no commands were run.
