---
id: computing-software.computer-graphics-engineering.directx.d3d12-uav-barriers
name: d3d12-uav-barriers
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-barriers, uav-barrier, unordered-access, compute-dependencies]
level: practitioner
status: docs-checked
description: "Insert D3D12 UAV barriers between dependent dispatches/draws that write and read the same UAV, and avoid redundant ones that serialise the GPU."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_resource_uav_barrier", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 UAV barriers

**Goal:** make dispatch B see dispatch A's UAV writes when the resource stays in
`UNORDERED_ACCESS` (no state change, so a transition barrier does not apply).

## 1. Usage
```cpp
cl->Dispatch(gx, gy, 1);                                        // pass A writes buf
D3D12_RESOURCE_BARRIER u = CD3DX12_RESOURCE_BARRIER::UAV(buf);  // UAV(nullptr) = all UAVs
cl->ResourceBarrier(1, &u);
cl->Dispatch(gx, gy, 1);                                        // pass B reads buf
```
A UAV barrier means all prior read or write UAV accesses to the resource must complete before later accesses begin. Without it,
consecutive dispatches may overlap and B can read stale or partial data.

## 2. When to skip it
- Two draws or dispatches that only read the UAV need no barrier.
- Two that write to the same UAV need none if the app knows the accesses are safe in any order.
- A transition barrier from UNORDERED_ACCESS to another state is a state change and is the barrier for that case.
- A NULL resource in the UAV barrier means any UAV access could require the barrier; name specific resources to keep unrelated work overlapping.

## 3. Common chains
- Prefix sum / reduction passes: barrier between every level.
- Indirect args written by compute then `ExecuteIndirect`: transition the args buffer to
  `D3D12_RESOURCE_STATE_INDIRECT_ARGUMENT`.
- Ray tracing: acceleration structures stay in `RAYTRACING_ACCELERATION_STRUCTURE` state and are synchronised with UAV barriers; put one on the BLAS before the TLAS build that references it.

## Gotchas
- A missing UAV barrier is a race that may work on one GPU and fail on another; the debug layer's state validation is described as conservative and not exhaustive, so test on several GPUs.
- Barriers can create idle gaps between short dispatches; merge small passes or batch independent ones between barriers, and submit several barriers in one `ResourceBarrier` call.

## Verify
- [ ] Results bit-identical across runs and vendors.
- [ ] No back-to-back barriers with nothing dependent between them.

## Checked

Checked 2026-10-26 against the Microsoft Learn D3D12 resource-barrier page and the DXR spec in DirectX-Specs (repository current to 2026-10-22). Confirmed: UAV barrier definition, when it is not needed (read-only, or writes safe in any order), NULL resource meaning, batching advice, debug-layer validation being conservative, acceleration structures synchronised by UAV barriers. Removed: the claim that D3D11 inserted these implicitly, the claim that atomic histograms never need one, vendor-specific behaviour claims, and the 'drains the shader pipe' wording.
Method: documentation only; no commands were run.
