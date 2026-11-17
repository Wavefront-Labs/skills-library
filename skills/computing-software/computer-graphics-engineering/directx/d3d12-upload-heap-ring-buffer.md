---
id: computing-software.computer-graphics-engineering.directx.d3d12-upload-heap-ring-buffer
name: d3d12-upload-heap-ring-buffer
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, d3d12-memory, upload-heap, upload-ring-buffer, linear-allocator, constant-buffer-alignment, gpu-upload-heap, rebar, fence]
level: advanced
status: docs-checked
description: "Stream per-frame constants and dynamic geometry in Direct3D 12 with a persistently mapped upload-heap ring buffer, 256-byte alignment, and fence-based reclamation."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/uploading-resources", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/D3D12GPUUploadHeaps.md", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/memory-management-strategies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 upload heap ring buffer

**Goal:** constant buffers and dynamic vertex data written by the CPU each frame with no
per-allocation resource creation and no CPU/GPU races.

## 1. One big upload buffer, mapped forever
```cpp
CD3DX12_HEAP_PROPERTIES up(D3D12_HEAP_TYPE_UPLOAD);
auto desc = CD3DX12_RESOURCE_DESC::Buffer(64ull << 20);              // 64 MiB
device->CreateCommittedResource(&up, D3D12_HEAP_FLAG_NONE, &desc,
    D3D12_RESOURCE_STATE_GENERIC_READ, nullptr, IID_PPV_ARGS(&ring));
uint8_t* cpu; ring->Map(0, nullptr, (void**)&cpu);                   // never Unmap
D3D12_GPU_VIRTUAL_ADDRESS gpu = ring->GetGPUVirtualAddress();
```
Resources in an upload heap must be created with `D3D12_RESOURCE_STATE_GENERIC_READ` and cannot be
changed away from it.

## 2. Allocate linearly, reclaim by fence
```cpp
struct Alloc { void* cpu; D3D12_GPU_VIRTUAL_ADDRESS gpu; };
Alloc allocate(size_t size, size_t align = 256) {     // CBVs require 256-byte alignment
    size_t off = alignUp(head, align);
    if (off + size > capacity) off = 0;                // wrap
    waitUntilFree(off, off + size);                    // check against tail recorded per frame fence
    head = off + size;
    return { cpu + off, gpu + off };
}
// end of frame: record {fenceValue, head}; when fence completes, tail = that head
```
Then bind directly by GPU VA — no descriptors needed for root CBVs:
```cpp
auto a = allocate(sizeof(DrawConstants));
memcpy(a.cpu, &consts, sizeof consts);
cmd->SetGraphicsRootConstantBufferView(1, a.gpu);
```
Vertex/index data: fill a `D3D12_VERTEX_BUFFER_VIEW` with `BufferLocation = a.gpu`.

## 3. When to copy to DEFAULT instead
Data read many times by the GPU (static meshes, large structured buffers read per pixel)
should be copied to a `D3D12_HEAP_TYPE_DEFAULT` resource: the default heap has the most GPU
bandwidth, while the upload heap trades GPU bandwidth for CPU write access and is best for
CPU-write-once, GPU-read-once data (profile if in doubt). Rule of thumb: written every frame and
read about once → upload heap; read many times → copy to default.

## 4. GPU upload heaps (ReBAR)
`D3D12_HEAP_TYPE_GPU_UPLOAD` (check
`D3D12_FEATURE_DATA_D3D12_OPTIONS16::GPUUploadHeapSupported`; creation fails if unsupported) is
CPU-visible **VRAM** (resizable BAR) that avoids an upload-plus-default copy. Its page property is
`WRITE_COMBINE`, the same as upload heaps, and reading it back from the CPU is inefficient.

## Gotchas
- Reading from mapped upload memory is extremely slow (write-combined): never `+=` into it.
- 256-byte CBV alignment wastes space for small structs; consider a structured buffer indexed by
  draw ID when draw counts are large.
- Ring overflow must block or grow; silently wrapping over in-flight data causes
  flickering constants under load.

## Verify
- [ ] No `CreateCommittedResource` calls per frame in a CPU profile.
- [ ] Ring high-water mark logged; capacity has headroom at worst case.
- [ ] Artificial GPU slowdown causes waits, never corrupted constants.

## Checked

2026-10-26. Checked against the Microsoft Learn Uploading resources page, the DirectX-Specs GPU upload heaps spec, d3d12.h
(D3D12_HEAP_TYPE_GPU_UPLOAD, D3D12_FEATURE_DATA_D3D12_OPTIONS16.GPUUploadHeapSupported, 256-byte CBV placement
constant) (win32, DirectX-Specs and DirectX-Headers repositories, commits to 2026-10). Confirmed: GENERIC_READ upload
resources, GPU upload heap = CPU-visible VRAM with WRITE_COMBINE page property, support query field, creation fails
when unsupported. Removed the unconfirmed Agility SDK version number, PCIe and system-RAM statements.
Method: documentation only; no commands were run.
