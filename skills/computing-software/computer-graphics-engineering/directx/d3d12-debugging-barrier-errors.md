---
id: computing-software.computer-graphics-engineering.directx.d3d12-debugging-barrier-errors
name: d3d12-debugging-barrier-errors
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-barriers, barrier-validation, gpu-based-validation-states, missing-barrier]
level: advanced
status: docs-checked
description: "Find D3D12 barrier bugs: debug-layer state messages, GPU-based validation for runtime states, PIX state inspection, and symptoms of missing UAV/aliasing barriers."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-d3d12-debug-layer-gpu-based-validation", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12sdklayers/nf-d3d12sdklayers-id3d12debugcommandlist-assertresourcestate", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12sdklayers/nf-d3d12sdklayers-id3d12debug-enabledebuglayer", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12sdklayers/nf-d3d12sdklayers-id3d12debug1-setenablesynchronizedcommandqueuevalidation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging barrier errors

## Tools, in order
1. **Debug layer** (CPU validation): enable it before creating the device (`D3D12GetDebugInterface` then
   `EnableDebugLayer`; enabling it after device creation makes the runtime remove the device). Read messages
   through the info queue (see `d3d12-info-queue-filtering-and-callbacks`).
2. **GPU-based validation** (GBV): patches shaders and injects validation work so it can check at GPU
   execution time. Microsoft documents it as finding use of uninitialised or incompatible descriptors,
   descriptors referencing deleted resources, promoted resource states and state decay, descriptor heap
   overruns, shader access of resources in incompatible states, and bad samplers.
   ```cpp
   ComPtr<ID3D12Debug1> dbg1; debug.As(&dbg1);
   dbg1->SetEnableGPUBasedValidation(TRUE);
   dbg1->SetEnableSynchronizedCommandQueueValidation(TRUE);   // default is on
   ```
   GBV can slow things down a lot: use it on smaller scenes or during bring-up. Its output is produced after the
   `ExecuteCommandLists` call finishes on the GPU, so it is asynchronous with CPU-timeline validation.
3. **AssertResourceState** (`ID3D12DebugCommandList`), for debug builds:
   ```cpp
   ComPtr<ID3D12DebugCommandList> dcl; cmd->QueryInterface(IID_PPV_ARGS(&dcl));
   dcl->AssertResourceState(tex, D3D12CalcSubresource(0,0,0,1,1), D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE);
   ```
   The `State` argument can be several `D3D12_RESOURCE_STATES` flags OR-ed together, and the subresource can
   be `D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES`.
4. **Force-full-barriers experiment**: temporarily route every transition through a conservative path (for
   example `COMMON` plus a UAV barrier after every dispatch); if the bug disappears it is a missing or incorrect
   barrier. Bisect by restoring the real barriers.

## Common causes to check by hand
- A UAV-to-UAV dependency between two dispatches on the same resource needs
  `CD3DX12_RESOURCE_BARRIER::UAV(resource)`. A UAV barrier changes no state. It is not in Microsoft's list of
  what GBV checks, so review compute chains manually (or use enhanced barriers, where the access is explicit).
- Reading a render target or depth buffer without a transition to a read state.
- Aliased resources used without an aliasing barrier (or, with enhanced barriers, without the sync, access and
  layout transition plus a discard when required).
- GPU-written indirect arguments or counts: transition `UNORDERED_ACCESS` to `INDIRECT_ARGUMENT`.

## Gotchas
- `StateBefore` must match the actual state at execution time; mismatches are real corruption risks, not just
  validation noise.
- GBV emulates COPY command lists with COMPUTE command lists, which may change how hardware performs copies.

## Verify
- [ ] A targeted repro is clean under GBV; the symptom is gone after the fix.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Using D3D12 debug layer GPU-based validation",
`ID3D12Debug::EnableDebugLayer`, `ID3D12DebugCommandList::AssertResourceState`, `ID3D12Debug1` methods
(MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08). Confirmed: GBV scope list, slowdown and
asynchronous-output notes, COPY emulation, API names, synchronized command queue validation being on by default, AssertResourceState parameters, debug-layer-before-device
rule. Removed unconfirmed claims: vendor-specific symptom table, the "10x or more" slowdown figure, the claim
that GBV never flags a missing UAV barrier (restated as "not in the documented scope"), PIX resource-history
features, and queue-type/render-pass checks attributed to the debug layer.
Method: documentation only; no commands were run.
