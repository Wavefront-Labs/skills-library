---
id: computing-software.computer-graphics-engineering.directx.d3d12-command-list-recording-and-multithreading
name: d3d12-command-list-recording-and-multithreading
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, command-list, command-list-recording, d3d12-multithreading, command-allocator-pool]
level: advanced
status: docs-checked
description: "Record D3D12 command lists in parallel: allocator-per-thread-per-frame, Reset/Close rules, state that does not carry over, and ordered submission."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/recording-command-lists-and-bundles", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/executing-and-synchronizing-command-lists", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-executebundle", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12commandqueue-executecommandlists"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command list recording and multithreading

## Rules
- `ID3D12CommandAllocator` holds the memory; `ID3D12GraphicsCommandList` records into it.
- An allocator can be **reset** only after the GPU finished all command lists recorded from it
  (fence check); otherwise the `Reset` call fails. `ID3D12CommandAllocator::Reset` is not free-threaded.
- An allocator can be associated with no more than one *currently recording* command list at a time.
- A command list can be reset immediately after it is submitted (even while still executing),
  which leaves it in the recording state; its allocator must not be in use.
- Record each list on one thread at a time.

## Per-frame per-thread allocators
```cpp
struct FrameContext { ComPtr<ID3D12CommandAllocator> alloc[MAX_THREADS]; UINT64 fence; };
// frame start (after waiting fence for this frame slot):
for (auto& a : frame.alloc) a->Reset();
// worker t:
lists[t]->Reset(frame.alloc[t].Get(), initialPSO);
lists[t]->SetDescriptorHeaps(1, heaps);           // state does NOT inherit between lists
lists[t]->SetGraphicsRootSignature(rootSig.Get());
lists[t]->RSSetViewports(1, &vp); lists[t]->RSSetScissorRects(1, &sc);
lists[t]->OMSetRenderTargets(1, &rtv, FALSE, &dsv);
recordDraws(lists[t], chunk[t]);
lists[t]->Close();
// main thread, in order:
queue->ExecuteCommandLists(n, ppLists);
```
Each list starts with default state: re-set heaps, root signature, root parameters, viewport,
scissor, render targets, primitive topology. Resource states, however, persist (they're
resource properties), so barriers recorded in list A affect what list B must assume.

## Ordering and barriers across lists
- Lists in one `ExecuteCommandLists` call (or successive calls on one queue) execute in order.
- Plan barriers centrally: a typical pattern records "transition" lists on the main thread
  between worker chunks, or uses enhanced barriers with explicit layouts per pass.
- Split work so each worker owns whole passes or equal-sized draw ranges.

## Submission
`ExecuteCommandLists` takes an array: submit the lists of a frame together rather than one call
per list. Lists must be closed first, and the runtime drops the call if `Close` was not called or
an allocator was reset after the list was recorded.

## Gotchas
- Forgetting `Close()`: the runtime drops the `ExecuteCommandLists` call.
- `Reset` on an allocator does not reduce its underlying size, so one that recorded a huge frame
  keeps that memory.
- Bundles inherit all state from the calling list except the pipeline state object and primitive
  topology; state set in a bundle affects the parent list.

## Verify
- [ ] CPU recording time scales with worker count; debug layer clean; PIX shows lists executing in intended order.

## Checked

2026-10-26. Checked against the Microsoft Learn pages on recording command lists and bundles, executing and synchronizing command
lists, ID3D12CommandQueue::ExecuteCommandLists and ID3D12GraphicsCommandList::ExecuteBundle (win32 and sdk-api
repositories, commits to 2026-10). Confirmed: allocator reset only after GPU completion, one recording list per
allocator, list Reset allowed while executing, allocators not free-threaded, Close required, bundle state inheritance.
Fixed: an early allocator Reset fails rather than corrupting commands; bundles inherit everything except PSO and
topology. Removed the unconfirmed submission-cost and 1-3-calls guidance.
Method: documentation only; no commands were run.
