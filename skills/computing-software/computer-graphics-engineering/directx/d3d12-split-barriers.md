---
id: computing-software.computer-graphics-engineering.directx.d3d12-split-barriers
name: d3d12-split-barriers
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-barriers, split-barriers, resource-barriers, begin-only, end-only]
level: advanced
status: docs-checked
description: "Use D3D12 split barriers (BEGIN_ONLY/END_ONLY) to overlap state transitions with unrelated GPU work, and know when they help."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/D3D12EnhancedBarriers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 split barriers

**Goal:** start a transition early and finish it just before the resource is used, so the driver
can do decompression/cache flushes while other work runs.

## 1. Pattern
```cpp
D3D12_RESOURCE_BARRIER b = CD3DX12_RESOURCE_BARRIER::Transition(
    gbufferAlbedo, D3D12_RESOURCE_STATE_RENDER_TARGET, D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE,
    D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES, D3D12_RESOURCE_BARRIER_FLAG_BEGIN_ONLY);
cl->ResourceBarrier(1, &b);          // right after the G-buffer pass
// ... shadow pass, SSAO on other targets ...
b.Flags = D3D12_RESOURCE_BARRIER_FLAG_END_ONLY;
cl->ResourceBarrier(1, &b);          // right before lighting reads it
```
Both halves must use identical before/after states. While the barrier is pending, the (sub)resource cannot be read or written by
the GPU, and the only legal transition barrier on it is the matching END_ONLY barrier.

## 2. When it pays
- Microsoft's description: split barriers hint that a resource in state A will next be used in state B later, letting the GPU
  optimise transition work and possibly reduce stalls, especially in multi-engine scenarios or when transitions are sparse.
- Little gain is likely for cheap transitions; treat it as a hint and measure.
- Enhanced barriers (`ID3D12GraphicsCommandList7::Barrier`) use explicit `SyncBefore/SyncAfter` scopes and express split barriers with
  `D3D12_BARRIER_SYNC_SPLIT`; check `D3D12_FEATURE_DATA_D3D12_OPTIONS12::EnhancedBarriersSupported`.

## 3. Batching rule
Microsoft advises batching multiple transitions into one `ResourceBarrier` call wherever possible. Split barriers are a
scheduling hint, not a replacement for batching.

## Gotchas
- Track pending splits in your render graph: a BEGIN without its END leaves the resource unusable.
- Back buffers start in `D3D12_RESOURCE_STATE_COMMON`, which is the same value as `PRESENT`.

## Verify
- [ ] Debug layer and GPU-based validation clean.
- [ ] GPU timing shows the lighting pass starting earlier than with a single barrier.

## Checked

Checked 2026-10-26 against the Microsoft Learn D3D12 resource-barrier page and the DirectX-Specs Enhanced Barriers spec (repository current to 2026-10-22). Confirmed: BEGIN_ONLY/END_ONLY pending semantics and the only legal barrier while pending, hint purpose, batching advice, ID3D12GraphicsCommandList7::Barrier, SyncBefore/SyncAfter, D3D12_BARRIER_SYNC_SPLIT, EnhancedBarriersSupported in OPTIONS12, PRESENT == COMMON. Removed: AMD DCC/HTILE specifics, Agility SDK 1.7 gate (not stated in the spec), and the command-list/queue rule for splitting across lists, which the legacy page does not state.
Method: documentation only; no commands were run.
