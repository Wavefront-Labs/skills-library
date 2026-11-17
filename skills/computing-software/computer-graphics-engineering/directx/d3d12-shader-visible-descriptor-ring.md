---
id: computing-software.computer-graphics-engineering.directx.d3d12-shader-visible-descriptor-ring
name: d3d12-shader-visible-descriptor-ring
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-binding, descriptor-ring, shader-visible-heap, descriptor-allocator]
level: advanced
status: docs-checked
description: "Manage the single shader-visible CBV/SRV/UAV heap in D3D12: persistent bindless region plus a per-frame ring for transient tables, with fence-based reuse."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/descriptor-heaps", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/shader-visible-descriptor-heaps", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/copying-descriptors", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-setdescriptorheaps"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader-visible descriptor heap management

Only one CBV/SRV/UAV and one sampler heap can be set at a time (`SetDescriptorHeaps`), and on some
hardware switching between heaps requires a GPU wait for idle. So allocate one large shader-visible
heap and partition it. The header limits are `D3D12_MAX_SHADER_VISIBLE_DESCRIPTOR_HEAP_SIZE_TIER_1`
and `_TIER_2` (1,000,000 descriptors each).

## Layout
```text
[ 0 .............. P ) persistent: bindless textures/buffers, allocated at load, freed with fence
[ P .............. N ) ring: transient per-frame tables (copied from CPU staging heaps)
```

## Ring allocator
```cpp
struct DescriptorRing {
    UINT base, size, head = 0;                     // indices into the shader-visible heap
    std::deque<std::pair<UINT64, UINT>> retired;   // (fenceValue, headAtEndOfFrame)
    UINT tail = 0;
    UINT Allocate(UINT count) {
        if (head + count > size) head = 0;         // wrap (skip tail fragment)
        // ensure we don't overrun descriptors still in flight
        while (inFlight(head, count)) WaitForOldestFrame();
        UINT idx = base + head; head += count; return idx;
    }
    void EndFrame(UINT64 fence) { retired.push_back({fence, head}); }
    void Release(UINT64 completed) { while (!retired.empty() && retired.front().first <= completed) { tail = retired.front().second; retired.pop_front(); } }
};
```
Each frame, copy the descriptors a draw needs into a contiguous ring range
(`CopyDescriptorsSimple` from non-shader-visible staging heaps), then
`SetGraphicsRootDescriptorTable(param, gpuHandle(idx))`.

## Persistent (bindless) region
- Free-list allocator of single slots for textures; the slot index goes into material data.
- Free a slot only after the fence for the last frame that may have referenced it.
- With SM 6.6 `ResourceDescriptorHeap[i]`, shaders index this region directly; most engines
  move almost everything here and keep the ring small.

## Sampler heap
A shader-visible sampler heap holds at most 2048 samplers (`D3D12_MAX_SHADER_VISIBLE_SAMPLER_HEAP_SIZE`): allocate all unique samplers persistently
at startup (deduplicate by desc); no ring needed.

## Gotchas
- Compute handle offsets with `GetDescriptorHandleIncrementSize`.
- Writing (CreateShaderResourceView) into a slot the GPU is reading is a race; that's why the ring
  is fenced.
- There is often a limit (typically around 96 MB across all processes) on write-combined GPU memory
  available to descriptor heaps; do not create large numbers of large shader-visible heaps.

## Verify
- [ ] Ring never wraps into in-flight ranges (debug assert); single `SetDescriptorHeaps` per command list.

## Checked

2026-10-26. Checked against the Microsoft Learn descriptor heaps and shader-visible descriptor heaps pages, SetDescriptorHeaps and
the d3d12.h constants (win32, sdk-api and DirectX-Headers repositories, commits to 2026-10). Confirmed: one heap per
type (max 2 set at once), GPU wait-for-idle on heap switch on some hardware, 1,000,000 tier-1/2 heap limit, 2048
sampler limit, root descriptor/table costs, write-combined limit around 96 MB. Removed the unconfirmed
CopyDescriptors-from-shader-visible slowness and heap-start-handle claims.
Method: documentation only; no commands were run.
