---
id: computing-software.computer-graphics-engineering.directx.d3d12-legacy-resource-state-transitions
name: d3d12-legacy-resource-state-transitions
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-barriers, resource-state-transition, d3d12-resource-states, state-tracking]
level: practitioner
status: docs-checked
description: "Transition D3D12 resources between legacy states correctly: common transition table, read-state combinations, per-command-list state tracking and resolving at submit."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_resource_states", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-d3d12-debug-layer-gpu-based-validation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy resource state transitions

## Common transitions
| Usage | Before | After |
|---|---|---|
| Render to texture, then sample | `RENDER_TARGET` | `PIXEL_SHADER_RESOURCE` (add `NON_PIXEL_SHADER_RESOURCE` if compute also reads) |
| Depth write, then sample depth | `DEPTH_WRITE` | `DEPTH_READ \| PIXEL_SHADER_RESOURCE` (depth test while sampling) |
| Compute writes, graphics reads | `UNORDERED_ACCESS` | `NON_PIXEL_SHADER_RESOURCE \| PIXEL_SHADER_RESOURCE` |
| GPU-written indirect args | `UNORDERED_ACCESS` | `INDIRECT_ARGUMENT` |
| Upload to default buffer | `COPY_DEST` | `VERTEX_AND_CONSTANT_BUFFER` / `INDEX_BUFFER` |
| Back buffer | `PRESENT` | `RENDER_TARGET` and back before Present |
| Readback | `X` | `COPY_SOURCE` |

```cpp
auto b = CD3DX12_RESOURCE_BARRIER::Transition(gbuf.Get(),
            D3D12_RESOURCE_STATE_RENDER_TARGET, D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE);
cmd->ResourceBarrier(1, &b);
```
`PRESENT` is a synonym for `COMMON` (both are 0); a back buffer must be in that state when presented and starts in it.

## Combining states
Read-only states can be OR-ed (`GENERIC_READ` is a combination for upload heaps). A write state
(`RENDER_TARGET`, `UNORDERED_ACCESS`, `DEPTH_WRITE`, `COPY_DEST`, `STREAM_OUT`) must be exclusive. A subresource
is in exactly one state, the set of flags supplied to `ResourceBarrier`. Prefer the narrowest read set you
need. Microsoft also advises avoiding explicit transitions to `COMMON` unless necessary.

## Tracking state across command lists
The `StateBefore` you pass must match the actual state at execution time; the before and after states of
consecutive `ResourceBarrier` calls must agree. With parallel command list recording you do not know it at record
time, so a common pattern is:
1. Each command list tracks local states; on first use of a resource in a list, record a "pending" requirement
   instead of a barrier.
2. At submit, on the queue thread, compare pending requirements with the global state and insert a small fix-up
   command list with the needed transitions before the recorded list.
3. Update global state with each list's final states.
Enhanced barriers with layouts reduce the bookkeeping.

## Gotchas
- A `StateBefore` mismatch is a debug-layer error; GPU-based validation checks promoted states and decay too.
- Buffers and simultaneous-access textures are promoted and decayed implicitly; do not add redundant barriers for them.
- Copy queues and compute queues cannot use every state; check `D3D12_RESOURCE_STATES` for which states each
  command list type supports.

## Verify
- [ ] The debug layer (with GPU-based validation for state checks) reports no state mismatches over a full playthrough.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Using resource barriers to synchronize resource states in
Direct3D 12" (MicrosoftDocs/win32, last commit 2026-10-08) and GBV page. Confirmed: PRESENT equals COMMON and back
buffer rules; one-state-per-subresource and consecutive-barrier agreement; promotion and decay behaviour; warning
on COMMON transitions; GBV covering promoted states and decay. Removed unconfirmed claims: the specific
`INVALID_SUBRESOURCE_STATE` message name, the exact list of states copy and compute queues cannot use, the
"ALL_SHADER_RESOURCE is slower on some GPUs" statement, and the MiniEngine reference link.
Method: documentation only; no commands were run.
