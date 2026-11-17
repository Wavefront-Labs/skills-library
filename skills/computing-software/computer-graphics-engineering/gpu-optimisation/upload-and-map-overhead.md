---
id: computing-software.computer-graphics-engineering.gpu-optimisation.upload-and-map-overhead
name: upload-and-map-overhead
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, cpu-overhead, upload-overhead, ring-buffer, persistent-mapping, copy-queue, write-combined-memory, rebar]
level: advanced
status: draft
description: "Cut CPU-GPU upload overhead: persistent mapped ring buffers, staging and copy queues, avoiding implicit syncs on Map, write-combined memory rules and ReBAR/upload heaps."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/uploading-resources", "https://gpuopen.com/learn/vulkan-device-memory/", "https://developer.nvidia.com/blog/optimizing-dx12-resource-uploads-to-the-gpu-using-gpu-upload-heaps/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Upload and map overhead

## 1. Per-frame dynamic data (constants, instance data)
Use a **persistently mapped ring buffer** in upload (host-visible) memory, sized for N frames in
flight:
```cpp
// once: create upload buffer, map forever
void* base; uploadBuf->Map(0, nullptr, &base);
// per allocation:
size_t off = align(head, 256); head = off + size;   // 256 = D3D12 CBV alignment
memcpy((char*)base + off, data, size);
// per frame: head wraps to the frame's region; fence ensures GPU finished with it
```
No `Map/Unmap` per draw; no driver renaming.

## 2. Write-combined memory rules
Upload heaps are write-combined, uncached for CPU reads:
- Write sequentially, full cache lines, with `memcpy`; never read back (reads are extremely slow).
- Don't do read-modify-write on mapped pointers (`+=`), build data in cached memory then copy.

## 3. Static resources (textures, meshes)
- Upload via a staging buffer and GPU copy into device-local memory (`CopyBufferRegion`,
  `CopyTextureRegion`, `vkCmdCopyBufferToImage`).
- Use a **dedicated copy/transfer queue** for streaming so graphics isn't blocked; synchronise with
  fences/semaphores and queue ownership transfers in Vulkan.
- Batch small uploads into large staging allocations.
- DirectStorage (D3D12) / GPU decompression for large asset streaming.

## 4. ReBAR / GPU upload heaps
With Resizable BAR, the CPU can write directly into VRAM: D3D12 `D3D12_HEAP_TYPE_GPU_UPLOAD`
(Agility SDK 1.611+), Vulkan memory types with both DEVICE_LOCAL and HOST_VISIBLE. Good for
per-frame data read many times by the GPU (avoids PCIe reads per access); still write-combined.

## 5. Avoid implicit syncs (GL/D3D11)
- `glBufferSubData`/`Map(WRITE_DISCARD)` on buffers in use cause driver copies or stalls; use
  orphaning, unsynchronised mapping with your own fences, or persistent mapping (`glBufferStorage`
  with `MAP_PERSISTENT_BIT | MAP_COHERENT_BIT`).

## Gotchas
- Forgetting to wait on the fence for a ring region overwrites data the GPU is still reading:
  flickering geometry.
- Mapping in a non-coherent Vulkan memory type requires `vkFlushMappedMemoryRanges`.

## Verify
- [ ] CPU profiler shows no time in Map/Unmap or driver copy routines per frame.
- [ ] Upload bandwidth per frame measured; copy queue overlap visible in timeline.
