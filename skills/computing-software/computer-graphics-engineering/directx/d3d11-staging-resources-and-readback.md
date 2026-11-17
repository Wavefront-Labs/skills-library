---
id: computing-software.computer-graphics-engineering.directx.d3d11-staging-resources-and-readback
name: d3d11-staging-resources-and-readback
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d11, staging-resource, d3d11-readback, map-do-not-wait]
level: practitioner
status: docs-checked
description: "Read GPU results back in D3D11 with staging resources: CopyResource, Map with D3D11_MAP_FLAG_DO_NOT_WAIT, ring of stagings to avoid stalls, and row pitch handling."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/how-to--use-dynamic-resources", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ne-d3d11-d3d11_usage", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-map", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-copyresource"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D11 staging resources and readback

`D3D11_USAGE_STAGING` resources are the only CPU-readable ones. The GPU copies into them; the
CPU maps them.

## Create
```cpp
D3D11_TEXTURE2D_DESC sd = srcDesc;                 // same size/format as the source
sd.Usage = D3D11_USAGE_STAGING; sd.BindFlags = 0;
sd.CPUAccessFlags = D3D11_CPU_ACCESS_READ; sd.MiscFlags = 0;
sd.SampleDesc = { 1, 0 };                          // resolve MSAA sources first (ResolveSubresource)
device->CreateTexture2D(&sd, nullptr, &staging[i]);
```

## Non-blocking readback ring
```cpp
ctx->CopyResource(staging[frame % N].Get(), gpuTex.Get());   // queued
// N-1 frames later:
D3D11_MAPPED_SUBRESOURCE m;
HRESULT hr = ctx->Map(staging[(frame + 1) % N].Get(), 0, D3D11_MAP_READ, D3D11_MAP_FLAG_DO_NOT_WAIT, &m);
if (hr == DXGI_ERROR_WAS_STILL_DRAWING) { /* not ready, try next frame */ }
else if (SUCCEEDED(hr)) {
    for (UINT y = 0; y < h; ++y) memcpy(dst + y * w * 4, (uint8_t*)m.pData + y * m.RowPitch, w * 4);
    ctx->Unmap(staging[(frame + 1) % N].Get(), 0);
}
```
Without `DO_NOT_WAIT`, `Map` waits for the GPU to finish with the resource.

## Partial reads
`CopySubresourceRegion` with a `D3D11_BOX` copies only what you need (e.g. 1x1 pixel under the
cursor for ID picking, or a small region for auto-exposure) into a small staging texture.

## Queries to know when ready
A `D3D11_QUERY_EVENT` issued after the copy can be polled with `GetData` (flags from
`D3D11_ASYNC_GETDATA_FLAG`) without mapping.

## Gotchas
- `RowPitch` is padded; copy row by row.
- Staging textures can't be bound to the pipeline; only Copy*/Map.
- Reading back synchronously forces the CPU to wait for the GPU; use a ring of staging resources.
- Buffers: same pattern with `D3D11_BUFFER_DESC` staging and `CopyResource`.

## Verify
- [ ] Profiler shows no CPU stalls in `Map`; readback values correct with a few frames latency.

## Checked

2026-10-26. Checked against Microsoft Learn: ID3D11DeviceContext::Map (DXGI_ERROR_WAS_STILL_DRAWING with DO_NOT_WAIT), CopyResource
(same type, identical dimensions, compatible formats), GetData and D3D11_QUERY (win32 and sdk-api repositories,
commits to 2026-10). Removed the unconfirmed glFinish comparison and a full-frame-latency figure.
Method: documentation only; no commands were run.
