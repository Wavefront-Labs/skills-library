---
id: computing-software.computer-graphics-engineering.directx.d3d12-render-pass-api
name: d3d12-render-pass-api
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, command-list, beginrenderpass, d3d12-render-passes, render-pass-tier]
level: advanced
status: docs-checked
description: "Use D3D12 render passes (BeginRenderPass) to declare load/store/resolve behaviour for tile-based and bandwidth-limited GPUs, and check render pass tiers."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-render-passes", "https://microsoft.github.io/DirectX-Specs/d3d/RenderPasses.html", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_render_pass_tier", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist4-beginrenderpass"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 render pass API

`ID3D12GraphicsCommandList4::BeginRenderPass` replaces `OMSetRenderTargets` + `Clear*` +
`DiscardResource` with one declaration of what happens to each attachment at the start and end of the pass.
Microsoft positions render passes mainly for tile-based deferred rendering (TBDR) architectures, where knowing the data
dependencies lets the driver avoid unnecessary loads and stores to main memory.

## Example
```cpp
D3D12_RENDER_PASS_RENDER_TARGET_DESC rt = {};
rt.cpuDescriptor = rtvHandle;
rt.BeginningAccess.Type = D3D12_RENDER_PASS_BEGINNING_ACCESS_TYPE_CLEAR;
rt.BeginningAccess.Clear.ClearValue = { DXGI_FORMAT_R8G8B8A8_UNORM, {0,0,0,1} };
rt.EndingAccess.Type = D3D12_RENDER_PASS_ENDING_ACCESS_TYPE_PRESERVE;

D3D12_RENDER_PASS_DEPTH_STENCIL_DESC ds = {};
ds.cpuDescriptor = dsvHandle;
ds.DepthBeginningAccess.Type = D3D12_RENDER_PASS_BEGINNING_ACCESS_TYPE_CLEAR;
ds.DepthBeginningAccess.Clear.ClearValue = { DXGI_FORMAT_D32_FLOAT, { .DepthStencil = {0.0f, 0} } };
ds.DepthEndingAccess.Type = D3D12_RENDER_PASS_ENDING_ACCESS_TYPE_DISCARD;   // depth not needed later
ds.StencilBeginningAccess.Type = D3D12_RENDER_PASS_BEGINNING_ACCESS_TYPE_NO_ACCESS;
ds.StencilEndingAccess.Type = D3D12_RENDER_PASS_ENDING_ACCESS_TYPE_NO_ACCESS;

cmdList4->BeginRenderPass(1, &rt, &ds, D3D12_RENDER_PASS_FLAG_NONE);
// draws
cmdList4->EndRenderPass();
```

## Access types
| Beginning | Meaning |
|---|---|
| `DISCARD` | previous contents irrelevant |
| `PRESERVE` | keep the previous contents |
| `CLEAR` | clear to the given value |
| `NO_ACCESS` | attachment not accessed in this pass |
| **Ending** | |
| `DISCARD` | contents not needed after the pass |
| `PRESERVE` | contents written back |
| `RESOLVE` | resolve an MSAA source into a destination (the destination is expected in `RESOLVE_DEST`; resolve operations in a pass do not implicitly change resource states) |
| `NO_ACCESS` | attachment not accessed |

## Flags
- `D3D12_RENDER_PASS_FLAG_ALLOW_UAV_WRITES`: required to issue UAV writes inside the pass so the driver can opt out of
  tiling if necessary. A write in a pass is not valid to read until a later pass, and UAV barriers are not
  permitted inside a pass.
- `SUSPENDING_PASS` / `RESUMING_PASS`: split a pass across command lists for multithreaded recording. A suspending
  pass followed by a resuming pass needs identical views and access flags and no intervening GPU operations, and the
  command lists must be executed in the same `ExecuteCommandLists` call.

## Tiers
`D3D12_FEATURE_DATA_D3D12_OPTIONS5::RenderPassesTier`: `TIER_0` = emulated in software by the runtime (may give no
performance benefit); `TIER_1` = driver implemented, render target and depth writes may be accelerated, UAV writes not
efficiently supported in a pass; `TIER_2` = also likely more efficient UAV writes (provided they are not read until a
later pass).

## Gotchas
- Render passes cannot be nested and cannot span command lists, except as suspend/resume pairs.
- These calls are disallowed inside a pass (the runtime removes the command list): `BeginRenderPass`,
  `ClearRenderTargetView`, `ClearDepthStencilView`, `ClearUnorderedAccess*`, `ClearState`, `Copy*`, `CopyTiles`,
  `DiscardResource`, `Dispatch`, `OMSetRenderTargets`, `ResolveQueryData`, `ResolveSubresource(Region)`, atomic
  copies and `SetProtectedResourceSession`.
- Some barriers are allowed inside a pass (for example `UNORDERED_ACCESS` to `INDIRECT_ARGUMENT`, or `COPY_DEST` to
  a shader resource state). Not allowed: `RENDER_TARGET` or `DEPTH_WRITE` to a read state on a currently bound
  RTV or DSV, any aliasing barrier, and UAV barriers.
- Use a clear value in the pass's `CLEAR` access instead of calling a clear method inside the pass.

## Verify
- [ ] Debug layer clean; on a tiled GPU, PIX or vendor timing shows reduced memory traffic.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Direct3D 12 render passes", `D3D12_RENDER_PASS_TIER`
(MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08) and the DirectX-Specs RenderPasses spec (2026-10-22).
Confirmed: access types, ALLOW_UAV_WRITES rule, suspend/resume rules, tier wording, disallowed call list,
conformant and non-conformant barrier examples, resolve state behaviour. Corrected: the draft said no barriers are
allowed in a pass (some are) and omitted `Dispatch` from the disallowed list. Removed unconfirmed claims: Qualcomm and
Arm specifics, "no slower on Tier 0", the optimized-clear-value remark, and garbage on tilers after a discard.
Method: documentation only; no commands were run.
