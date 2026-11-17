---
id: computing-software.computer-graphics-engineering.directx.d3d12-bundles
name: d3d12-bundles
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, directx-12, d3d12-command-submission, d3d12-bundles, command-lists, executebundle]
level: advanced
status: docs-checked
description: "Record reusable Direct3D 12 bundles: what state they inherit, what is forbidden, ExecuteBundle cost, and when bundles beat or lose to plain command lists."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/recording-command-lists-and-bundles", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-executebundle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct3D 12 bundles

**Goal:** record a small, fixed sequence of draws once and replay it every frame with
`ExecuteBundle`, saving CPU recording time. Microsoft describes bundles as a second level of command lists for
grouping a small number of API commands; the driver does as much pre-processing as possible at bundle
creation so they are cheap to execute.

## 1. Create and record
```cpp
device->CreateCommandAllocator(D3D12_COMMAND_LIST_TYPE_BUNDLE, IID_PPV_ARGS(&bundleAlloc));
device->CreateCommandList(0, D3D12_COMMAND_LIST_TYPE_BUNDLE, bundleAlloc.Get(), pso.Get(), IID_PPV_ARGS(&bundle));
bundle->SetGraphicsRootSignature(rootSig.Get());
bundle->IASetPrimitiveTopology(D3D_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
bundle->IASetVertexBuffers(0, 1, &vbv); bundle->IASetIndexBuffer(&ibv);
bundle->DrawIndexedInstanced(count, 1, 0, 0, 0);
bundle->Close();
// per frame, inside the direct command list:
cmdList->SetDescriptorHeaps(1, heaps);             // bundle heaps must match the caller's
cmdList->ExecuteBundle(bundle.Get());
```

## 2. State rules
- **Inherited:** a bundle inherits all state from the parent command list on which `ExecuteBundle` is called,
  except the pipeline state object and primitive topology. Set both inside the bundle.
- **Leaks back:** all state set in a bundle affects the state of the parent command list.
- **Caller must be a direct command list**, and the bundle must be closed. Otherwise the runtime silently
  drops the call, and `Close` on the caller returns `E_INVALIDARG`.
- **PSO consistency:** all pipeline state objects referenced by a bundle must have the same render target
  formats, depth buffer format and sample descriptions.
- **Not allowed in a bundle** (the runtime drops the call; the debug layer reports an error): any Clear
  method, any Copy method, `DiscardResource`, `ExecuteBundle`, `ResourceBarrier`, `ResolveSubresource`,
  `SetPredication`, `BeginQuery`, `EndQuery`, `SOSetTargets`, `OMSetRenderTargets`, `RSSetViewports`,
  `RSSetScissorRects`. `SetDescriptorHeaps` is allowed only if the heaps match the calling list's.
- **Predication:** `ExecuteBundle` is not itself predicated; predicated operations inside the bundle follow
  the predication state inherited from the caller.
- Per-frame data therefore goes through root arguments set by the caller, for example a root CBV per frame.

## 3. When worth it
Bundles suit many static draws recorded on one thread that you replay repeatedly; Microsoft describes them as
intended for a small number of commands. Profile against plain recording before adopting them.

## Gotchas
- The debug layer validates that the bundle's allocator has not been reset since `Close`, at `ExecuteBundle` time
  and when the parent list executes. Do not reset or destroy it while any list that executes the bundle is in
  flight; fence like any allocator.
- The debug layer errors if a resource referenced by the command list has been destroyed.

## Verify
- [ ] Debug layer clean; the capture shows the bundle's draws under `ExecuteBundle`.
- [ ] CPU record time for the static set drops versus re-recording.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Creating and recording command lists and bundles" and
`ID3D12GraphicsCommandList::ExecuteBundle` (MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08).
Confirmed: inheritance rule (all state except PSO and topology) and leak-back; the full forbidden-call list and
runtime-drop behaviour; direct-caller requirement; matching RT/depth formats; descriptor heap rule; predication
behaviour; allocator-reset validation. Removed unconfirmed claims: the "root signature must match" wording, a
quoted debug-layer message, and vendor advice about bundles (the NVIDIA link was not read).
Method: documentation only; no commands were run.
