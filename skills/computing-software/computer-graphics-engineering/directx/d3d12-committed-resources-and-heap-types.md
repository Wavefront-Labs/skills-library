---
id: computing-software.computer-graphics-engineering.directx.d3d12-committed-resources-and-heap-types
name: d3d12-committed-resources-and-heap-types
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-memory, createcommittedresource, heap-type, optimized-clear-value]
level: practitioner
status: docs-checked
description: "Create D3D12 committed resources in the right heap type (DEFAULT, UPLOAD, READBACK, GPU_UPLOAD, CUSTOM), with initial states, clear values and heap flags."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-createcommittedresource", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_heap_type", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_heap_flags", "https://microsoft.github.io/DirectX-Specs/d3d/D3D12GPUUploadHeaps.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Committed resources and heap types

`CreateCommittedResource` creates a resource and an implicit heap sized for it. It is the simple path;
use it for render targets, large textures and anything long-lived, and use placed resources when you
need pooling or aliasing.

## Heap types
| Type | CPU access | GPU | Use |
|---|---|---|---|
| `DEFAULT` | none | most bandwidth | textures, RT/DS, static buffers, UAVs |
| `UPLOAD` | optimised for CPU writes; reads are commonly inefficient | less than maximum bandwidth | CPU-write-once, GPU-read-once data; staging; small per-frame constants |
| `READBACK` | write-back cached, suited to CPU reads | less than maximum bandwidth | GPU-write-once data read by the CPU, query results |
| `GPU_UPLOAD` | CPU-visible, write-combined on discrete GPUs | GPU-local memory | CPU-written data the GPU reads repeatedly |
| `CUSTOM` | you set page property and memory pool | | UMA tuning, multi-adapter, special cases |

`GPU_UPLOAD` creation fails unless `D3D12_FEATURE_DATA_D3D12_OPTIONS16::GPUUploadHeapSupported` is true;
on discrete GPUs that depends on the whole frame buffer being CPU visible. For `UPLOAD`, `READBACK` and
`GPU_UPLOAD` heap types the `CPUPageProperty` and `MemoryPoolPreference` must be `UNKNOWN`; use
`GetCustomHeapProperties` when building a `CUSTOM` heap.

```cpp
CD3DX12_HEAP_PROPERTIES heap(D3D12_HEAP_TYPE_DEFAULT);
auto desc = CD3DX12_RESOURCE_DESC::Tex2D(DXGI_FORMAT_R16G16B16A16_FLOAT, w, h, 1, 1, 1, 0,
                                         D3D12_RESOURCE_FLAG_ALLOW_RENDER_TARGET);
D3D12_CLEAR_VALUE clear = { DXGI_FORMAT_R16G16B16A16_FLOAT, {0, 0, 0, 1} };
device->CreateCommittedResource(&heap, D3D12_HEAP_FLAG_NONE, &desc,
    D3D12_RESOURCE_STATE_RENDER_TARGET, &clear, IID_PPV_ARGS(&hdrTarget));
```
- **Optimized clear value** (`pOptimizedClearValue`): for textures with the render-target or depth-stencil flag,
  choose the value you will most commonly clear with. Other values work but are not as efficient. For buffers it
  must be `nullptr`.
- **Initial state**: a resource in an `UPLOAD` heap must be created in `GENERIC_READ` and cannot change away
  from it; a resource in a `READBACK` heap must be created in `COPY_DEST` and cannot change away from it.
- `D3D12_HEAP_FLAG_CREATE_NOT_ZEROED` lets the OS skip zeroing the new heap, lowering creation overhead. It is not
  guaranteed: memory coming from other processes is still zeroed.

## Gotchas
- Committed resources occupy their own implicit heap, so thousands of tiny committed buffers waste memory;
  suballocate small buffers from one large buffer. Placement alignment defaults are 64 KB for buffers and most
  textures and 4 MB for MSAA textures (smaller alignments exist for small textures and, with the tight
  alignment feature, for buffers; see `d3d12-resource-alignment-and-small-resources`).
- Do not put data that shaders read repeatedly in an `UPLOAD` heap: the heap-type documentation says it is
  best for write-once, read-once data and lists re-initialising a resource every frame as a poor use.

## Verify
- [ ] The debug layer shows no clear-value mismatch warnings for render targets and depth buffers.

## Checked
Date: 2026-10-26. Documentation: `ID3D12Device::CreateCommittedResource`, `D3D12_HEAP_TYPE`, `D3D12_HEAP_FLAGS`
(MicrosoftDocs/sdk-api, last commit 2026-10-08) and the DirectX-Specs GPU upload heaps spec (2026-10-22).
Confirmed: required initial states for UPLOAD and READBACK; optimized clear value semantics; NOT_ZEROED
behaviour; GPU_UPLOAD support cap (OPTIONS16) and cache properties; UPLOAD and READBACK usage guidance;
alignment defaults. Removed unconfirmed claims: "Buffers ignore initial state", "fast clears require the clear
value", "at least 64 KB per committed resource" (superseded by tight alignment), "ReBAR" naming, and the
D3D12MA recommendation.
Method: documentation only; no commands were run.
