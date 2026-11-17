---
id: computing-software.computer-graphics-engineering.directx.d3d12-barrier-batching
name: d3d12-barrier-batching
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-barriers, barrier-batching, redundant-barriers, gpu-idle-bubbles]
level: advanced
status: docs-checked
description: "Cut D3D12 barrier cost: batch transitions into one ResourceBarrier call, drop redundant and read-to-read transitions, and place barriers to avoid GPU idle bubbles."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12", "https://microsoft.github.io/DirectX-Specs/d3d/D3D12EnhancedBarriers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Barrier batching and minimisation

Microsoft's barrier guidance is to batch multiple transitions into one `ResourceBarrier` call wherever
possible, to rely on common-state promotion and decay instead of explicit transitions, and to avoid
excessive transitions to `COMMON`.

## Batch per pass boundary
```cpp
std::vector<D3D12_RESOURCE_BARRIER> pending;
void Require(Resource& r, D3D12_RESOURCE_STATES s) {
    if (r.state == s || (IsReadOnly(r.state) && (r.state & s) == s)) return;   // already satisfies
    pending.push_back(CD3DX12_RESOURCE_BARRIER::Transition(r.ptr, r.state, s)); r.state = s;
}
void Flush(ID3D12GraphicsCommandList* cmd) {
    if (!pending.empty()) { cmd->ResourceBarrier((UINT)pending.size(), pending.data()); pending.clear(); }
}
// before each pass: Require(...) for every input/output, then Flush() once
```
A subresource is in exactly one state, which is a set of `D3D12_RESOURCE_STATES` flags, so a resource already
in a combined read state (for example `NON_PIXEL_SHADER_RESOURCE | PIXEL_SHADER_RESOURCE`) satisfies a pass
that needs only one of those bits.

## Remove redundancy
- Plan the combined read state up front (all readers in the frame) so the resource transitions once from
  write to read, not between every reader.
- Rely on promotion from `COMMON` and decay back to `COMMON` (buffers, simultaneous-access textures, copy
  queue resources and anything promoted to a read-only state). See `d3d12-implicit-state-promotion-and-decay`.
- Do not transition back to `COMMON` at the end of each list "to be safe": the barrier documentation warns that
  excessive transitions to `COMMON` can dramatically slow the GPU. Use it when the next access is on a copy
  queue or for presentation.
- A UAV barrier is not needed between two draws or dispatches that only read a UAV, nor between writes to the
  same UAV when execution order does not matter.

## Placement
- Issue transitions as late as possible before the consumer. With split barriers (`BEGIN_ONLY` then
  `END_ONLY`), begin them right after the producer so unrelated work can overlap.
- Group passes so writes to many targets end together, then one batch transitions them all
  (for example the G-buffer targets).

## Measure
Use a GPU capture or timing tool to look for idle gaps around barriers, and look for many small barriers between
tiny passes.

## Gotchas
- When `ResourceBarrier` receives an array, the API behaves as if it had been called once per element, in the
  order supplied; the before and after states of consecutive barriers must agree, so do not list the same
  subresource twice with inconsistent states.
- Enhanced barriers give explicit sync and access scopes and are meant to expose capabilities legacy
  barriers could not; see `d3d12-enhanced-barrier-layouts-and-discard`.

## Verify
- [ ] Barrier call count per frame drops in a capture's event list, and the debug layer reports no state mismatches.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Using resource barriers to synchronize resource states in
Direct3D 12" (MicrosoftDocs/win32 repository, last commit 2026-10-08) and the DirectX-Specs enhanced barriers
spec (2026-10-22). Confirmed: batching advice; the array-processed-in-order rule and consistent before/after
states; promotion and decay rules; the warning about excessive transitions to `COMMON`; the UAV-barrier
exceptions; the `BEGIN_ONLY` split flag. Removed unconfirmed vendor-tool claims (RGP barrier view, drain and
cache-flush cost statements) and unconfirmed gpu-vendor source links.
Method: documentation only; no commands were run.
