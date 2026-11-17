---
id: computing-software.computer-graphics-engineering.directx.d3d12-resource-alignment-and-small-resources
name: d3d12-resource-alignment-and-small-resources
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-memory, resource-alignment, small-resource-placement, getresourceallocationinfo]
level: advanced
status: docs-checked
description: "Place D3D12 resources with correct alignment: 64 KB default, 4 KB small textures, 4 MB MSAA, GetResourceAllocationInfo, and buffer suballocation for tiny buffers."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_resource_desc", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-getresourceallocationinfo", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_resource_heap_tier", "https://microsoft.github.io/DirectX-Specs/d3d/D3D12TightPlacedResourceAlignment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource alignment and small resources

## Alignment classes
| Constant | Value | Applies to |
|---|---|---|
| `D3D12_DEFAULT_RESOURCE_PLACEMENT_ALIGNMENT` | 64 KB | buffers (must be 64 KB or 0 in the resource desc, unless tight alignment is used) and most textures |
| `D3D12_SMALL_RESOURCE_PLACEMENT_ALIGNMENT` | 4 KB | small non-MSAA textures with unknown layout and no render-target or depth-stencil flag |
| `D3D12_DEFAULT_MSAA_RESOURCE_PLACEMENT_ALIGNMENT` | 4 MB | MSAA textures (the default when `Alignment` is 0) |
| `D3D12_SMALL_MSAA_RESOURCE_PLACEMENT_ALIGNMENT` | 64 KB | small MSAA textures with unknown layout |

A texture is "small" when its estimated most-detailed mip level fits in the larger alignment: for a normal texture the
runtime assumes near-equilateral 4 KB tiles, so a resource of 16 tiles (64 KB) or fewer can use 4 KB alignment. The
resource-desc `Alignment` for textures may be 0, 4 KB, 64 KB or 4 MB.

## Ask for small alignment
```cpp
D3D12_RESOURCE_DESC d = CD3DX12_RESOURCE_DESC::Tex2D(DXGI_FORMAT_BC7_UNORM, 128, 128, 1, 8);
d.Alignment = D3D12_SMALL_RESOURCE_PLACEMENT_ALIGNMENT;
D3D12_RESOURCE_ALLOCATION_INFO info = device->GetResourceAllocationInfo(0, 1, &d);
if (info.Alignment != D3D12_SMALL_RESOURCE_PLACEMENT_ALIGNMENT) {   // not eligible: retry with default
    d.Alignment = 0; info = device->GetResourceAllocationInfo(0, 1, &d);
}
device->CreatePlacedResource(heap, AlignUp(offset, info.Alignment), &d, initialState, nullptr, IID_PPV_ARGS(&tex));
```
For placed textures you must use `GetResourceAllocationInfo` to learn the size and alignment. `ID3D12Device4::
GetResourceAllocationInfo1` additionally returns a per-resource offset for a batch of resources.

## Small buffers
Without tight alignment, buffers use 64 KB alignment as resources. Many small buffers (constants, small meshes) are
better suballocated from one large buffer (constant buffer views need 256-byte placement alignment). With the Tight
Alignment feature (`D3D12_RESOURCE_FLAG_USE_TIGHT_ALIGNMENT`, released in Agility SDK 1.618 and later, only valid when
the driver reports support through `D3D12_FEATURE_D3D12_TIGHT_ALIGNMENT` / `D3D12_FEATURE_DATA_TIGHT_ALIGNMENT::SupportTier`), placed buffers may have alignment down to
8 bytes with a 256-byte maximum, and committed resources can also benefit but are limited to 4 KB or larger.

## Heap tier constraints
On `D3D12_RESOURCE_HEAP_TIER_1` a heap supports resources from a single category (buffers, RT/DS textures, or other
textures), declared with the `D3D12_HEAP_FLAG_ALLOW_ONLY_*` flags; tier 1 apps cannot create a heap that allows all three.
Tier 2 allows mixing. Check `ResourceHeapTier` and pool accordingly.

## Gotchas
- `SizeInBytes` may exceed what you compute from dimensions; always use the returned value.
- `SizeInBytes` equal to `UINT64_MAX` means an error (invalid description).
- Render targets and depth buffers never qualify for 4 KB alignment.

## Verify
- [ ] Memory statistics show small textures packed at 4 KB granularity; no debug-layer misalignment errors.

## Checked
Date: 2026-10-26. Documentation: `D3D12_RESOURCE_DESC`, `ID3D12Device::GetResourceAllocationInfo`,
`D3D12_RESOURCE_HEAP_TIER` (MicrosoftDocs/sdk-api, last commit 2026-10-08) and the DirectX-Specs Tight Placed
Resource Alignment spec (2026-10-22). Confirmed: alignment table and small-resource definition, allowed Alignment
values, GetResourceAllocationInfo behaviour, UINT64_MAX error value, heap tier categories, tight alignment ranges and
flag. Corrected: the draft said buffers always need 64 KB and committed resources cannot benefit; tight alignment
changes both. Removed the D3D12MA link (not read).
Method: documentation only; no commands were run.
