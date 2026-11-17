---
id: computing-software.computer-graphics-engineering.directx.d3d12-enhanced-barrier-layouts-and-discard
name: d3d12-enhanced-barrier-layouts-and-discard
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-barriers, barrier-layout, texture-discard, enhanced-barriers-layouts]
level: advanced
status: docs-checked
description: "Use D3D12 enhanced barrier texture layouts (COMMON, DIRECT_QUEUE_*, SHADER_RESOURCE, UNDEFINED) and the DISCARD flag for transient targets and queue-specific layouts."
sources: ["https://microsoft.github.io/DirectX-Specs/d3d/D3D12EnhancedBarriers.html", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_barrier_layout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced barrier texture layouts and discard

Enhanced barriers separate **sync** (when), **access** (caches) and **layout** (texture memory
arrangement). Buffers have no layouts; textures do.

## Layouts
| Layout | Meaning |
|---|---|
| `UNDEFINED` | contents don't matter (source only; value `0xffffffff`) |
| `COMMON` | matches legacy `COMMON`; usable without a layout transition for the common access bits (copy, shader read and so on) |
| `PRESENT` | same as `COMMON`; `COMMON` is the layout the swap chain back buffer must have for presentation |
| `GENERIC_READ` | read-only usages combined |
| `RENDER_TARGET`, `UNORDERED_ACCESS`, `DEPTH_STENCIL_WRITE`, `DEPTH_STENCIL_READ` | attachment and UAV use |
| `SHADER_RESOURCE`, `COPY_SOURCE`, `COPY_DEST`, `RESOLVE_SOURCE`, `RESOLVE_DEST` | as named |
| `DIRECT_QUEUE_COMMON`, `DIRECT_QUEUE_SHADER_RESOURCE`, `COMPUTE_QUEUE_COMMON`, `COMPUTE_QUEUE_UNORDERED_ACCESS` and so on | queue-specific variants |

The spec says queue-specific common layouts can differ from `COMMON` on some hardware, offer reduced decompress
operations and let common-layout textures be used as UAVs without a layout transition, and are strongly
recommended whenever possible. Both `LayoutBefore` and `LayoutAfter` must be compatible with the queue type
doing the barrier (for example a compute queue cannot use graphics-only layouts).

## Example: transient target
```cpp
D3D12_TEXTURE_BARRIER tb = {};
tb.SyncBefore = D3D12_BARRIER_SYNC_NONE;            tb.SyncAfter = D3D12_BARRIER_SYNC_RENDER_TARGET;
tb.AccessBefore = D3D12_BARRIER_ACCESS_NO_ACCESS;   tb.AccessAfter = D3D12_BARRIER_ACCESS_RENDER_TARGET;
tb.LayoutBefore = D3D12_BARRIER_LAYOUT_UNDEFINED;   tb.LayoutAfter = D3D12_BARRIER_LAYOUT_RENDER_TARGET;
tb.pResource = transientRT;
tb.Subresources = { 0xffffffff };                   // IndexOrFirstMipLevel = 0xffffffff, NumMipLevels = 0: all subresources
tb.Flags = D3D12_TEXTURE_BARRIER_FLAG_DISCARD;      // initialise compression metadata; contents undefined
D3D12_BARRIER_GROUP g = { D3D12_BARRIER_TYPE_TEXTURE, 1 }; g.pTextureBarriers = &tb;
cmd7->Barrier(1, &g);                               // ID3D12GraphicsCommandList7
```
A layout transition from `UNDEFINED` to any potentially compressed layout (render target, depth-stencil, UAV)
**must** initialise compression metadata when `D3D12_TEXTURE_BARRIER_FLAG_DISCARD` is present. This replaces the
legacy requirement to initialise newly placed or aliased render target and depth resources with a clear, copy or
`DiscardResource` before first use. Then clear or fully overwrite.

## Choosing layouts
- Prefer the queue-specific common layouts over `COMMON` when a texture stays on one queue type.
- Use `COMMON` for resources shared across queue types.
- Global barriers do not change layout, so they cannot replace a transition that needs a layout change.

## Gotchas
- `LayoutBefore` must match the actual layout (validated like legacy states).
- Requires `EnhancedBarriersSupported` in `D3D12_FEATURE_DATA_D3D12_OPTIONS12` (Agility SDK plus a supporting driver).
- Mixing legacy `ResourceBarrier` and enhanced `Barrier` on the same subresource can add performance overhead; the
  spec strongly recommends avoiding it. To switch models, a resource with a legacy state other than `COMMON` must
  first be transitioned to `COMMON`, and a texture with an enhanced layout must be placed in
  `D3D12_BARRIER_LAYOUT_COMMON` (with prior accesses finished and flushed) before a legacy barrier.

## Verify
- [ ] Debug layer clean; aliased targets render correctly on first use; a capture shows no unexpected decompress work.

## Checked
Date: 2026-10-26. Documentation: DirectX-Specs "D3D12 Enhanced Barriers" (repository last commit 2026-10-22), and
`D3D12_BARRIER_LAYOUT` (MicrosoftDocs/sdk-api, last commit 2026-10-08), `d3d12.h` from DirectX-Headers. Confirmed:
layout names; PRESENT as an alias of COMMON and COMMON required for presentation; queue-specific common layout
benefits; DISCARD metadata rule; `0xffffffff` all-subresources encoding; `EnhancedBarriersSupported` in OPTIONS12;
legacy interop rules. Removed unconfirmed claims: "DIRECT_QUEUE_* layouts keep compression that COMMON would
decompress" (restated per spec), and "mixing is allowed with rules" (restated as strongly discouraged).
Method: documentation only; no commands were run.
