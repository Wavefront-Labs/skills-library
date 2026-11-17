---
id: computing-software.computer-graphics-engineering.directx.d3d12-video-memory-budget-queries
name: d3d12-video-memory-budget-queries
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-memory, queryvideomemoryinfo, budget-change-notification, vram-budget-d3d12]
level: advanced
status: docs-checked
description: "Track D3D12 VRAM use against the OS budget with IDXGIAdapter3::QueryVideoMemoryInfo, budget change events, SetVideoMemoryReservation, and react before paging."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/memory-management-strategies", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/residency", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/nf-dxgi1_4-idxgiadapter3-queryvideomemoryinfo", "https://github.com/GPUOpen-LibrariesAndSDKs/D3D12MemoryAllocator/blob/master/include/D3D12MemAlloc.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Video memory budget queries

## Query
```cpp
ComPtr<IDXGIAdapter3> adapter3; adapter.As(&adapter3);
DXGI_QUERY_VIDEO_MEMORY_INFO local, nonLocal;
adapter3->QueryVideoMemoryInfo(0, DXGI_MEMORY_SEGMENT_GROUP_LOCAL, &local);       // VRAM
adapter3->QueryVideoMemoryInfo(0, DXGI_MEMORY_SEGMENT_GROUP_NON_LOCAL, &nonLocal); // system RAM visible to GPU
// local.Budget, local.CurrentUsage, local.AvailableForReservation, local.CurrentReservation
```
`Budget` is what the OS memory manager wants this process to use right now; it changes as other
apps start/stop. For UMA adapters the non-local value is always zero (Microsoft memory management strategies page).

## Budget change notifications
```cpp
HANDLE evt = CreateEvent(nullptr, FALSE, FALSE, nullptr); DWORD cookie;
adapter3->RegisterVideoMemoryBudgetChangeNotificationEvent(evt, &cookie);
// in your streaming thread: WaitForSingleObject(evt, 0) == WAIT_OBJECT_0 -> re-query and adapt
```

## Reacting
- Keep `CurrentUsage` within `Budget`. Over budget the OS may evict resources to system memory only
  as a last resort; applications should not rely on that and should manage their budget instead.
- Responses: drop top mips of streamed textures, shrink streaming pool, evict (`Evict`) or release
  unused resources, lower render resolution or shadow resolution.
- `ID3D12Device::MakeResident` / `Evict` let you control what is resident; D3D12MA can help with
  budget-aware allocation.

## Reservation
`SetVideoMemoryReservation(0, LOCAL, bytes)` sends the OS the minimum physical memory your
application needs (up to `AvailableForReservation`).

## With D3D12MA
`allocator->GetBudget(&localBudget, &nonLocalBudget)` returns the budget information;
`D3D12MA::ALLOCATION_FLAG_WITHIN_BUDGET` makes an allocation fail with `E_OUTOFMEMORY` if it would exceed the budget.

## Gotchas
- The budget fluctuates as background processes wake and sleep and can change dramatically when the
  user switches away; test with competing apps.

## Verify
- [ ] Overlay shows usage/budget; launching a second VRAM-heavy app triggers quality reduction rather than stutter.

## Checked

2026-10-26. Checked against the Microsoft Learn Memory Management Strategies and Residency pages, the IDXGIAdapter3
QueryVideoMemoryInfo, RegisterVideoMemoryBudgetChangeNotificationEvent and SetVideoMemoryReservation reference pages,
and the D3D12MemAlloc.h header (GetBudget, ALLOCATION_FLAG_WITHIN_BUDGET) (win32, sdk-api and GPUOpen repositories,
commits to 2026-10). Confirmed: local/non-local meaning, UMA non-local always zero, budget fluctuation, over-budget
eviction as a last resort, reservation purpose. Removed the 90-95 percent threshold, the D3DX12Residency.h reference,
the 8 GB example and the CurrentUsage composition claim.
Method: documentation only; no commands were run.
