---
id: computing-software.computer-graphics-engineering.directx.d3d12-predication
name: d3d12-predication
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, command-list, predication, setpredication, occlusion-predication]
level: advanced
status: docs-checked
description: "Skip D3D12 draws/dispatches on the GPU with SetPredication: occlusion-query results or GPU-written buffers as predicates, without CPU readback."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/predication", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-setpredication", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-executebundle", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-resolvequerydata"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 predication

`SetPredication(buffer, offset, op)` makes subsequent rendering and resource-manipulation commands conditional
on a 64-bit value in a buffer, evaluated by the GPU. No readback, no stall. When the GPU executes
`SetPredication` it snaps the value; later changes to the buffer do not retroactively change the predication
state. Unlike D3D11, predication is decoupled from queries, so any data you write can drive it.

## Occlusion-query predication
```cpp
// pass 1: draw cheap bounding boxes with colour/depth writes off
cmd->BeginQuery(occHeap.Get(), D3D12_QUERY_TYPE_BINARY_OCCLUSION, i);
DrawBoundingBox(cmd, obj[i]);
cmd->EndQuery(occHeap.Get(), D3D12_QUERY_TYPE_BINARY_OCCLUSION, i);
// resolve into a buffer (destination must be in COPY_DEST), then transition for predication
cmd->ResolveQueryData(occHeap.Get(), D3D12_QUERY_TYPE_BINARY_OCCLUSION, 0, n, predBuf.Get(), 0);
Transition(cmd, predBuf, D3D12_RESOURCE_STATE_COPY_DEST, D3D12_RESOURCE_STATE_PREDICATION);
// pass 2: real draws, skipped if no samples passed
for (UINT i = 0; i < n; ++i) {
    cmd->SetPredication(predBuf.Get(), i * sizeof(UINT64), D3D12_PREDICATION_OP_EQUAL_ZERO);
    DrawObject(cmd, obj[i]);           // not performed when the query result == 0
}
cmd->SetPredication(nullptr, 0, D3D12_PREDICATION_OP_EQUAL_ZERO);   // null buffer disables predication
```
Commands are not performed if the predicate data equals the operation: `EQUAL_ZERO` skips when the value is zero
and `NOT_EQUAL_ZERO` skips when it is non-zero.

## Arbitrary GPU predicates
Any buffer you write (for example from a compute culling pass writing 0 or 1 per object) can drive predication. The
source buffer can be in any heap type, and must be in `D3D12_RESOURCE_STATE_PREDICATION` (an alias of
`INDIRECT_ARGUMENT`) when `SetPredication` is called; the debug layer errors otherwise.

## Which commands are predicated
`DrawInstanced`, `DrawIndexedInstanced`, `Dispatch`, `CopyTextureRegion`, `CopyBufferRegion`, `CopyResource`,
`CopyTiles`, `ResolveSubresource`, `ClearDepthStencilView`, `ClearRenderTargetView`,
`ClearUnorderedAccessViewUint/Float` and `ExecuteIndirect`. **Not predicated:** `ResolveQueryData`, `BeginQuery`,
`EndQuery`. Predication is allowed on direct, compute and copy command lists.

## Trade-offs
- Using same-frame occlusion results adds a dependency between pass 1 and pass 2.
- For many objects, GPU-driven culling with `ExecuteIndirect` and a count buffer avoids recording a predicated draw
  per object on the CPU.

## Gotchas
- The offset must be a multiple of 8 bytes, the resource must be a buffer, and the offset must fit in it.
- `SetPredication` cannot be called inside a bundle. Bundles inherit the predication state of the list that
  executes them, and operations inside the bundle are predicated; `ExecuteBundle` itself is not.
- Direct command lists begin with predication disabled; predication state is not inherited between lists.
  The debug layer warns if a predicate is still set when `ExecuteCommandLists` is called.

## Verify
- [ ] A capture shows predicated-off draws as skipped; frame time drops in heavily occluded views.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Predication" and `ID3D12GraphicsCommandList::SetPredication`,
`ResolveQueryData`, `ExecuteBundle` (MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08). Confirmed: value
snapshot, null-buffer disable, operation semantics, PREDICATION state and alias, 8-byte alignment, any heap type,
list of predicated operations, bundle behaviour, initial disabled state. Corrected: `ResolveQueryData` is not
predicated (the draft listed it as predicated); bundles inherit predication (the draft said bundles cannot use it
at all); the buffer may be in any heap type, not only a default heap. Removed unconfirmed popping claims.
Method: documentation only; no commands were run.
