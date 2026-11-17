---
id: computing-software.computer-graphics-engineering.directx.directx-resource-barriers-and-heaps
name: directx-resource-barriers-and-heaps
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [directx, d3d12, resource-barriers, resource-states, heaps, descriptor-heaps, placed-resources, committed-resources, aliasing-barrier, residency, upload-heap, default-heap, debug-layer, gpu-validation]
level: advanced
status: docs-checked
description: "Get D3D12 resource states, barrier transitions and heap types (upload/default/readback, committed/placed) right and avoid flicker and corruption bugs."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/residency", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/memory-management-strategies", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_heap_type"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 resource barriers and heaps

**Goal:** keep every resource in a state the GPU operation it's about to do expects,
and place it in the right heap — the two things D3D12 makes you manage explicitly
that D3D11 hid, and the usual source of flicker/corruption/crashes that only show
up on some hardware.

## Resource states and transition barriers
D3D12 tracks a resource's current usage as an explicit state
(`D3D12_RESOURCE_STATE_*`): `COMMON`, `RENDER_TARGET`, `PIXEL_SHADER_RESOURCE`,
`COPY_DEST`, `UNORDERED_ACCESS`, `DEPTH_WRITE`, etc. Before an operation that needs
a different state than the resource is currently in, insert a **transition
barrier**:
```cpp
D3D12_RESOURCE_BARRIER b{};
b.Type = D3D12_RESOURCE_BARRIER_TYPE_TRANSITION;
b.Transition.pResource = tex;
b.Transition.StateBefore = D3D12_RESOURCE_STATE_RENDER_TARGET;
b.Transition.StateAfter  = D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE;
cmdList->ResourceBarrier(1, &b);
```
- `StateBefore` **must match the resource's actual current state** at that point
  in the command list — a mismatch is a correctness bug that the debug layer reports.
- Track state per-resource per-command-list yourself; D3D12 does not do this for you.
- A **UAV barrier** (not a state transition) indicates that all read or write UAV accesses to a
  resource must complete before later UAV accesses to the same resource can begin; it is needed
  between dependent UAV passes (e.g. compute write then compute read).
- Batch barriers (pass an array to one `ResourceBarrier` call) rather than one call per resource.
- **Enhanced barriers** replace states with explicit sync/access/layout; check
  `EnhancedBarriersSupported` in `D3D12_FEATURE_DATA_D3D12_OPTIONS12`. Legacy transition
  barriers remain valid.

## Heap types
- **DEFAULT**: the most GPU bandwidth, no CPU access. Most resources live here and are
  populated through upload heaps. Static meshes, textures, render targets.
- **UPLOAD**: CPU access optimised for uploading, less GPU bandwidth; best for CPU-write-once,
  GPU-read-once data. Resources must be created in `GENERIC_READ` and cannot change away
  from it. Typical use: write here, `CopyBufferRegion`/`CopyTextureRegion` into a DEFAULT-heap
  resource.
- **READBACK**: GPU writes, CPU reads — for GPU timestamp queries, occlusion
  results, compute output you need on CPU.
- **Committed vs placed resources**: committed = its own implicit heap (simple,
  one allocation per resource — allocation count limits and fragmentation at scale).
  Placed = you manage a large heap and place multiple resources into offsets within
  it (`CreatePlacedResource`) — needed for custom allocators, resource aliasing,
  and avoiding OS allocation overhead at thousands of resources.
- **Aliasing barrier**: indicates a transition between usages of two different resources
  whose mappings overlap in the same heap (placed or reserved resources), e.g. a transient
  render target pool.

## Residency and budgets
- `IDXGIAdapter3::QueryVideoMemoryInfo` reports the current video memory budget, which
  fluctuates as other processes run. The OS demotes memory to system memory only as an
  extreme last resort; applications should manage their budget rather than rely on that.
- Heaps can be evicted from residency (`Evict`) and made resident again (`MakeResident`)
  for explicit control, for example in streaming.

## Verify
- [ ] D3D12 debug layer + GPU-based validation enabled in all dev/test builds —
      most state-transition bugs are silent without it.
- [ ] Every UAV read-after-write (same resource, same or later command list) has an
      explicit UAV barrier, not just a state transition.
- Upload-heap data is read by the GPU about once; data read repeatedly is copied to a DEFAULT heap.
- [ ] Video memory budget monitored under the actual target asset set, not just a
      test scene, before shipping a streaming budget.

## Checked

2026-10-26. Checked against the Microsoft Learn resource-barrier, residency and memory management pages, the D3D12_HEAP_TYPE
reference and d3d12.h (win32, sdk-api and DirectX-Headers repositories, commits to 2026-10). Confirmed: DEFAULT/UPLOAD
descriptions and the GENERIC_READ rule, UAV barrier definition, aliasing barrier definition, over-budget behaviour,
EnhancedBarriersSupported field. Removed the unconfirmed claims that release builds hang on state mismatches and that
batching lets the driver reorder.
Method: documentation only; no commands were run.
