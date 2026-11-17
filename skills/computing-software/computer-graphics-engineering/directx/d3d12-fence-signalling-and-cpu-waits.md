---
id: computing-software.computer-graphics-engineering.directx.d3d12-fence-signalling-and-cpu-waits
name: d3d12-fence-signalling-and-cpu-waits
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-fence, seteventoncompletion, gpu-cpu-sync, frames-in-flight-d3d12]
level: practitioner
status: docs-checked
description: "Synchronise CPU and GPU in D3D12 with fences: Signal/GetCompletedValue, SetEventOnCompletion waits, frames-in-flight, deferred deletion and flush on shutdown."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nn-d3d12-id3d12fence", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12fence-seteventoncompletion", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device1-seteventonmultiplefencecompletion", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/user-mode-heap-synchronization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fences and CPU waits

A D3D12 fence is a 64-bit counter. Queues `Signal(fence, value)` it when preceding work
completes; the CPU reads `GetCompletedValue()` or waits for a value; other queues `Wait(fence, value)`.

## Frames in flight
```cpp
const UINT FRAMES = 2;
UINT64 frameFenceValue[FRAMES] = {}; UINT64 nextValue = 1;
HANDLE evt = CreateEvent(nullptr, FALSE, FALSE, nullptr);

void BeginFrame(UINT slot) {
    if (fence->GetCompletedValue() < frameFenceValue[slot]) {
        fence->SetEventOnCompletion(frameFenceValue[slot], evt);
        WaitForSingleObjectEx(evt, INFINITE, FALSE);
    }
    allocators[slot]->Reset();                 // safe: GPU finished this slot's work
    ProcessDeferredDeletes(fence->GetCompletedValue());
}
void EndFrame(UINT slot) {
    queue->ExecuteCommandLists(...);
    swapChain->Present(1, 0);
    frameFenceValue[slot] = nextValue;
    queue->Signal(fence.Get(), nextValue++);
}
```
One fence per queue with increasing values is enough; store the value per frame slot, per upload batch, per
resource for deletion. Microsoft's guidance is that applications set their own fence values, and a good starting
point is increasing the fence once per frame.

## Deferred deletion
```cpp
void DeferRelease(ComPtr<ID3D12Resource> r) { deleteQueue.push({ nextValue, std::move(r) }); }
void ProcessDeferredDeletes(UINT64 completed) {
    while (!deleteQueue.empty() && deleteQueue.front().value <= completed) deleteQueue.pop();
}
```
Release a resource only when the fence passes the value signalled after its last use.

## Flush (resize, shutdown, device recreation)
```cpp
void Flush() {
    UINT64 v = nextValue++;
    queue->Signal(fence.Get(), v);
    fence->SetEventOnCompletion(v, evt); WaitForSingleObject(evt, INFINITE);
}
```
Do this before `ResizeBuffers` and before releasing anything at shutdown.

## Gotchas
- `SetEventOnCompletion(value, nullptr)` does not return until the fence value is reached: simple, but you cannot add
  a timeout. Use an event for timeouts and multi-object waits.
- A removed device makes `GetCompletedValue()` return `UINT64_MAX` (and signals all fences to that value), so loops
  waiting for "completed >= x" end immediately; check device removal separately.
- A fence may be rewound: its value need not only increment. If two queues or threads signal the same fence there
  can be a race over which value ends up current, so keep one monotonic signaller per fence.
- `ID3D12Device1::SetEventOnMultipleFenceCompletion` waits on several fences at once.

## Verify
- [ ] The CPU does not wait in BeginFrame when the GPU is less than one frame behind; the debug layer reports no
  "resetting allocator in use" errors.

## Checked
Date: 2026-10-26. Documentation: `ID3D12Fence`, `GetCompletedValue`, `SetEventOnCompletion`,
`ID3D12Device1::SetEventOnMultipleFenceCompletion`, `GetDeviceRemovedReason` (MicrosoftDocs/sdk-api, last commit
2026-10-08) and "User mode heap synchronization" (MicrosoftDocs/win32). Confirmed: null-event blocking behaviour;
UINT64_MAX after removal; fence rewind behaviour; per-frame increment guidance. Corrected: the multi-fence wait
method belongs to `ID3D12Device1`, not `ID3D12Device`. Replaced the "allowed but breaks logic" remark with the
documented rewind race. Removed the unverified sample-code link.
Method: documentation only; no commands were run.
