---
id: computing-software.computer-graphics-engineering.directx.d3d11-dynamic-buffers-map-discard
name: d3d11-dynamic-buffers-map-discard
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d11, direct3d-11, map-discard, map-no-overwrite, d3d11-usage-dynamic, d3d11-constant-buffers, updatesubresource, ring-buffer, buffer-renaming]
level: practitioner
status: docs-checked
description: "Update Direct3D 11 dynamic vertex, index and constant buffers without stalls: MAP_WRITE_DISCARD vs NO_OVERWRITE ring buffers, UpdateSubresource trade-offs, CB update frequency."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/how-to--use-dynamic-resources", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ne-d3d11-d3d11_map", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-map", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-resources-buffers-constant-how-to"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D11 dynamic buffers: MAP_DISCARD and NO_OVERWRITE

**Goal:** stream CPU-generated data each frame in D3D11 without the driver stalling or
running out of renamed buffer memory.

## 1. Create dynamic
```cpp
D3D11_BUFFER_DESC bd{};
bd.ByteWidth = 4 << 20; bd.Usage = D3D11_USAGE_DYNAMIC;
bd.BindFlags = D3D11_BIND_VERTEX_BUFFER; bd.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;
device->CreateBuffer(&bd, nullptr, &vb);
```

## 2. The ring pattern (vertex/index data)
```cpp
D3D11_MAP mode = D3D11_MAP_WRITE_NO_OVERWRITE;          // "I promise not to touch in-use bytes"
if (cursor + bytes > capacity) { mode = D3D11_MAP_WRITE_DISCARD; cursor = 0; }  // driver renames
D3D11_MAPPED_SUBRESOURCE m; ctx->Map(vb, 0, mode, 0, &m);
memcpy((uint8_t*)m.pData + cursor, src, bytes);
ctx->Unmap(vb, 0);
ctx->Draw(count, cursor / stride);                       // or set offset in IASetVertexBuffers
cursor += bytes;
```
- `WRITE_DISCARD`: the previous contents become undefined. Use it once per wrap, not per draw.
- `WRITE_NO_OVERWRITE` returns immediately; correctness is on you (append only).
- `WRITE_NO_OVERWRITE` is valid only on vertex and index buffers in the original runtime; the
  D3D11.1 runtime also allows it on dynamic constant buffers and SRVs of dynamic buffers
  (check `MapNoOverwriteOnDynamicConstantBuffer` in `D3D11_FEATURE_DATA_D3D11_OPTIONS`).

## 3. Constant buffers
- Group by update frequency: per-frame, per-view, per-material, per-object. Never put
  per-object data in the same CB as per-frame data.
- Many per-object CBs: use D3D11.1 `VSSetConstantBuffers1` with **offsets** into one large CB
  (offsets and counts are in 16-byte shader constants and must be multiples of 16 constants,
  i.e. 256 bytes; at most 4096 constants per view).
- `UpdateSubresource` on `DEFAULT` buffers suits rarely changing data.

## 4. Choosing usage
| data | usage |
|---|---|
| never changes | `IMMUTABLE` with initial data |
| changes rarely (level load, edits) | `DEFAULT` + `UpdateSubresource` |
| changes every frame | `DYNAMIC` + Map |
| CPU readback | `STAGING` + `CopyResource` + Map (read N frames later) |

## Gotchas
- `WRITE_DISCARD` requires a resource created with dynamic usage and CPU write access, so a
  `DEFAULT` buffer cannot be mapped for discard; with `D3D11_MAP_FLAG_DO_NOT_WAIT`, `Map` returns
  `DXGI_ERROR_WAS_STILL_DRAWING` while the GPU is still using the resource.
- Partial writes after DISCARD: the rest of the buffer contents are **undefined**, not the
  previous data.

## Verify
- [ ] Discards per frame ≈ number of ring wraps, not number of draws.
- [ ] D3D11 debug layer clean.

## Checked

2026-10-26. Checked against Microsoft Learn: D3D11_MAP enumeration, ID3D11DeviceContext::Map and VSSetConstantBuffers1, the
dynamic-resources how-to (win32 and sdk-api repositories, commits to 2026-10). Confirmed: NO_OVERWRITE limited to
vertex/index buffers before D3D11.1 and the MapNoOverwriteOnDynamicConstantBuffer cap, DISCARD leaves contents
undefined, offsets multiple of 16 constants (256 bytes), 4096-constant range, WAS_STILL_DRAWING with DO_NOT_WAIT.
Removed the NVIDIA article source, the unconfirmed debug-layer discard warning and driver-internal behaviour claims.
Method: documentation only; no commands were run.
