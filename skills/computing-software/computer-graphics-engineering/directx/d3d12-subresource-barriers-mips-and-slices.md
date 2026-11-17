---
id: computing-software.computer-graphics-engineering.directx.d3d12-subresource-barriers-mips-and-slices
name: d3d12-subresource-barriers-mips-and-slices
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-barriers, subresource-barrier, d3d12calcsubresource, mip-generation-d3d12]
level: advanced
status: docs-checked
description: "Transition individual D3D12 subresources (mips, array slices, planes) for mip generation and per-face rendering, computing subresource indices correctly."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/subresources", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/d3d12calcsubresource", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subresource barriers: mips, slices, planes

## Subresource index
```cpp
UINT sub = D3D12CalcSubresource(mip, arraySlice, planeSlice, mipLevels, arraySize);
// documented as MipSlice + ArraySlice * MipLevels, plus the plane term (see the Subresources page)
```
Planes: depth is often plane 0 and stencil plane 1 for depth-stencil formats; planar YCbCr formats use planes for sub-sampled data.

## Mip generation with compute
Each pass reads mip N-1 and writes mip N; they must be in different states:
```cpp
for (UINT m = 1; m < mips; ++m) {
    D3D12_RESOURCE_BARRIER b[2] = {
        CD3DX12_RESOURCE_BARRIER::Transition(tex, D3D12_RESOURCE_STATE_UNORDERED_ACCESS,
            D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE, m - 1),     // source mip -> SRV
    };
    cmd->ResourceBarrier(1, b);
    cmd->SetComputeRootDescriptorTable(0, srvForMip[m - 1]);
    cmd->SetComputeRootDescriptorTable(1, uavForMip[m]);
    cmd->Dispatch(DivUp(w >> m, 8), DivUp(h >> m, 8), 1);
}
// finally transition the last mip (still UAV) to SRV state too
```
Start with the whole texture in `UNORDERED_ACCESS` (except mip 0 if it came from a copy). After
the loop every mip must be in the same state if you want to transition the whole resource with
`D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES` later; otherwise track per subresource.

## Per-face / per-slice rendering
Rendering cube faces one at a time: transition face `f` (all its mips or just mip 0) to
`RENDER_TARGET`, others can be sampled concurrently (e.g. reading the previous face for
filtering). The RTV must target that slice (`Texture2DArray.FirstArraySlice = f, ArraySize = 1`).

## ALL_SUBRESOURCES vs individual
- `D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES` transitions all subresources of the resource at once.
- Per-subresource barriers for large mip chains generate many barriers: batch them in one
  `ResourceBarrier` call.

## Enhanced barriers alternative
`D3D12_TEXTURE_BARRIER` with `Subresources = { IndexOrFirstMipLevel, NumMipLevels, FirstArraySlice,
NumArraySlices, FirstPlane, NumPlanes }` expresses ranges directly, avoiding per-index loops.

## Gotchas
- State tracking code must store per-subresource states once any partial transition happens.

## Verify
- [ ] Debug layer clean during mip generation; PIX shows the expected state per mip between dispatches.

## Checked

2026-10-26. Checked against the Microsoft Learn Subresources, D3D12CalcSubresource and resource barrier pages and the d3d12.h
D3D12_BARRIER_SUBRESOURCE_RANGE structure (win32 and DirectX-Headers repositories, commits to 2026-10). Confirmed:
subresource index formula basis and plane slice description, ALL_SUBRESOURCES flag, the six range fields of the enhanced
barrier subresource range. Removed the unconfirmed claim about all-mip UAVs and the NV12 plane layout statement.
Method: documentation only; no commands were run.
