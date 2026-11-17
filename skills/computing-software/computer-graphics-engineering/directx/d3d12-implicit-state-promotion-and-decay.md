---
id: computing-software.computer-graphics-engineering.directx.d3d12-implicit-state-promotion-and-decay
name: d3d12-implicit-state-promotion-and-decay
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-barriers, state-promotion, state-decay, common-state, copy-queue]
level: advanced
status: docs-checked
description: "Rely on D3D12 implicit state promotion and decay for buffers, simultaneous-access textures and copy queues, and drop the barriers you do not need."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12#common-state-promotion", "https://microsoft.github.io/DirectX-Specs/d3d/D3D12EnhancedBarriers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 implicit state promotion and decay

**Goal:** know which resources leave `D3D12_RESOURCE_STATE_COMMON` automatically and return to it
when an `ExecuteCommandLists` operation completes, so you skip redundant barriers and avoid debug-layer errors.

## 1. Promotion (COMMON to X on first GPU access, no barrier)
- **Buffers** and textures created with `D3D12_RESOURCE_FLAG_ALLOW_SIMULTANEOUS_ACCESS` are promoted to the
  state needed: any state in the promotion table, covering either one write flag or one or more read flags
  (for example `COPY_DEST`, `UNORDERED_ACCESS`, `RENDER_TARGET` for a buffer, or `GENERIC_READ`).
- **Other textures**: promote only to `COPY_SOURCE`, `COPY_DEST`, `NON_PIXEL_SHADER_RESOURCE` and
  `PIXEL_SHADER_RESOURCE`. Render target and depth use always need an explicit barrier.
- Depth-stencil resources can never be implicitly promoted.
- Read states can accumulate (for example `PIXEL_SHADER_RESOURCE` then `NON_PIXEL | PIXEL_SHADER_RESOURCE`), but
  once you write (for example `COPY_DEST`) a barrier is needed to leave it (for example to `RENDER_TARGET`, or from
  the combined read states to a write state).

## 2. Decay (X to COMMON when the ExecuteCommandLists operation completes on the GPU)
These resources decay: anything accessed on a copy queue, buffers on any queue type, textures with simultaneous
access, and any resource implicitly promoted to a read-only state. Decay does not occur between command lists
executed together in the same `ExecuteCommandLists` call.
Buffers and simultaneous-access textures decay whether they were explicitly transitioned or implicitly promoted.
A buffer uploaded on the copy queue can therefore be read on the direct queue with no barriers.

## 3. Practical use
```cpp
// Copy queue: upload into a COMMON buffer; no barriers needed on either queue.
copyCL->CopyBufferRegion(vb, 0, upload, 0, size);
// Direct queue (after a fence wait): bind as VB; promotes COMMON to VERTEX_AND_CONSTANT_BUFFER.
```
Your state tracker must model this: after a list executes, record decayed resources as `COMMON`, or you will emit a
barrier with the wrong `StateBefore`. When recording an explicit transition on a resource that is in `COMMON`,
either `COMMON` or any promotable state is valid as `StateBefore`.

## Gotchas
- Promotion acts like an implicit barrier; later accesses that change state need explicit barriers.
- Ordinary textures written on the direct queue do not decay.
- Avoid explicit transitions to `COMMON` unless needed (for example the next access is on a copy queue):
  Microsoft warns that excessive transitions to `COMMON` can dramatically slow the GPU.

## Verify
- [ ] The debug layer shows no before-state mismatch errors after removing barriers.
- [ ] Copy-queue uploads are used on the direct queue without any transitions.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Using resource barriers to synchronize resource states in
Direct3D 12" (MicrosoftDocs/win32, last commit 2026-10-08), sections on common state promotion and decay; the
enhanced barriers spec for promotion limits on textures. Confirmed: the promotion table (buffers versus
non-simultaneous textures, depth never promoted), one-write-or-many-reads rule, the four decay conditions, no decay
within one ExecuteCommandLists call, `StateBefore` COMMON-or-promotable rule, and the warning on COMMON transitions.
Removed unconfirmed claims: "promotion is per command list" and "simultaneous access disables DCC on many GPUs".
Method: documentation only; no commands were run.
