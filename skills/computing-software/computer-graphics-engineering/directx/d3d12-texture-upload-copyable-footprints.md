---
id: computing-software.computer-graphics-engineering.directx.d3d12-texture-upload-copyable-footprints
name: d3d12-texture-upload-copyable-footprints
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, d3d12-memory, copytextureregion, getcopyablefootprints, texture-upload, row-pitch-alignment, updatesubresources, copy-queue]
level: practitioner
status: docs-checked
description: "Upload textures in Direct3D 12 correctly: GetCopyableFootprints for 256-byte row pitch and 512-byte placement, CopyTextureRegion per subresource, BC block rows."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/upload-and-readback-of-texture-data", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-getcopyablefootprints", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 texture upload with copyable footprints

**Goal:** textures (all mips, arrays, cube faces, compressed formats) copied from an
upload buffer into a default-heap texture without skewed rows or misaligned offsets.

## 1. Ask the device for the layout
```cpp
D3D12_RESOURCE_DESC td = tex->GetDesc();
UINT n = td.MipLevels * td.DepthOrArraySize;               // subresource count (x planes for planar formats)
std::vector<D3D12_PLACED_SUBRESOURCE_FOOTPRINT> fp(n);
std::vector<UINT> rows(n); std::vector<UINT64> rowBytes(n); UINT64 total;
device->GetCopyableFootprints(&td, 0, n, uploadBaseOffset, fp.data(), rows.data(), rowBytes.data(), &total);
```
Footprints already include the rules: **RowPitch multiple of 256**
(`D3D12_TEXTURE_DATA_PITCH_ALIGNMENT`), placement offsets aligned to **512**
(`D3D12_TEXTURE_DATA_PLACEMENT_ALIGNMENT`), as in the Microsoft upload sample. `rows` is in **block rows** for BC formats
(height/4).

## 2. Fill the upload buffer row by row
```cpp
for (UINT s = 0; s < n; ++s)
  for (UINT r = 0; r < rows[s]; ++r)
    memcpy(mapped + fp[s].Offset - uploadBaseOffset + r * fp[s].Footprint.RowPitch,
           src[s].data + r * src[s].rowPitch, rowBytes[s]);         // copy only the real bytes
```
A single `memcpy` of the whole image works only if the source pitch equals the 256-aligned
pitch — it usually doesn't (e.g. 100-pixel-wide RGBA8 = 400 bytes vs 512).

## 3. Record the copies
```cpp
for (UINT s = 0; s < n; ++s) {
    CD3DX12_TEXTURE_COPY_LOCATION dst(tex, s);
    CD3DX12_TEXTURE_COPY_LOCATION src(uploadBuf, fp[s]);
    cmd->CopyTextureRegion(&dst, 0, 0, 0, &src, nullptr);
}
// tex: COPY_DEST -> PIXEL_SHADER_RESOURCE | NON_PIXEL_SHADER_RESOURCE
```
`UpdateSubresources` in d3dx12 wraps all of this; for streaming use your own ring allocator.

## 4. Copy queue
On a `D3D12_COMMAND_LIST_TYPE_COPY` queue, textures can only be in `COMMON` /
`COPY_DEST` / `COPY_SOURCE`. Create in `COMMON`, copy (implicit promotion to `COPY_DEST`),
let it decay back to `COMMON` at the end of the ExecuteCommandLists, then the graphics
queue promotes it to shader-resource on first use (after waiting on the copy fence).

## Gotchas
- Subresource index = `mip + arraySlice * mipLevels (+ plane * mips * arraySize)`;
  `D3D12CalcSubresource` avoids mistakes.
- Big textures: the footprint total can exceed your ring; split by subresource.

## Verify
- [ ] Odd-width textures (e.g. 100x37) display correctly at every mip.
- [ ] Copy-queue uploads show no state errors with GPU-based validation enabled.

## Checked

2026-10-26. Checked against the Microsoft Learn Upload and readback of texture data page, ID3D12Device::GetCopyableFootprints,
the Subresources page and the barrier page on common state promotion/decay (win32 and sdk-api repositories, commits to
2026-10). Confirmed: pitch alignment 256 and placement alignment 512, footprint-driven row copies, copy-queue decay
to COMMON, promotion of textures from COMMON to copy states. Removed the unconfirmed block-compression and DDS/KTX
ordering notes.
Method: documentation only; no commands were run.
