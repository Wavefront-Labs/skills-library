---
id: computing-software.computer-graphics-engineering.directx.d3d12-readback-heaps-and-gpu-to-cpu-copies
name: d3d12-readback-heaps-and-gpu-to-cpu-copies
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-memory, readback-heap, texture-readback, screenshot-d3d12]
level: practitioner
status: docs-checked
description: "Read GPU data back in D3D12: readback heap buffers, CopyTextureRegion with placed footprints for textures, row pitch alignment, fences and Map ranges."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/readback-data-using-heaps", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/upload-and-readback-of-texture-data", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-getcopyablefootprints", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-copytextureregion"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Readback heaps and GPU-to-CPU copies

To read GPU results on the CPU, copy into a buffer in a `READBACK` heap, wait for the fence, then map. A resource in a
readback heap must be a buffer (`D3D12_RESOURCE_DIMENSION_BUFFER`).

## Texture readback (screenshot)
```cpp
auto texDesc = backBuffer->GetDesc();
D3D12_PLACED_SUBRESOURCE_FOOTPRINT fp; UINT rows; UINT64 rowBytes, total;
device->GetCopyableFootprints(&texDesc, 0, 1, 0, &fp, &rows, &rowBytes, &total);
// readback buffer of size 'total' (CD3DX12_RESOURCE_DESC::Buffer(total)), heap READBACK, state COPY_DEST
Transition(cmd, backBuffer, D3D12_RESOURCE_STATE_PRESENT, D3D12_RESOURCE_STATE_COPY_SOURCE);
CD3DX12_TEXTURE_COPY_LOCATION dst(readback.Get(), fp), src(backBuffer.Get(), 0);
cmd->CopyTextureRegion(&dst, 0, 0, 0, &src, nullptr);
Transition(cmd, backBuffer, D3D12_RESOURCE_STATE_COPY_SOURCE, D3D12_RESOURCE_STATE_PRESENT);
// execute, signal fence, wait (or poll frames later)
D3D12_RANGE r = { 0, (SIZE_T)total }; uint8_t* p; readback->Map(0, &r, (void**)&p);
for (UINT y = 0; y < rows; ++y) memcpy(out + y * w * 4, p + fp.Offset + y * fp.Footprint.RowPitch, w * 4);
D3D12_RANGE none = { 0, 0 }; readback->Unmap(0, &none);   // CPU wrote nothing
```
`Map` does not synchronise with the GPU (D3D12 `Map` behaves like D3D11 `Map` with `NO_OVERWRITE`), so use a fence
to know the GPU has finished writing before you map. The copyable footprint's `RowPitch` is aligned to
`D3D12_TEXTURE_DATA_PITCH_ALIGNMENT` (256 bytes) and the placement alignment is
`D3D12_TEXTURE_DATA_PLACEMENT_ALIGNMENT` (512 bytes): copy row by row, using `RowPitch` for the source stride.

## Buffer readback
`CopyBufferRegion(readback, 0, src, srcOffset, bytes)` after transitioning the source to `COPY_SOURCE`
(a UAV written by compute needs `UNORDERED_ACCESS` to `COPY_SOURCE`).

## Avoid stalls
- Keep one readback buffer per frame in flight and read results from an older frame; waiting on the fence immediately
  after submission stalls the CPU for the whole GPU frame.
- `Map` with the byte range you will read; `Unmap` with an empty written range.
- Readback heaps use write-back CPU caching, which suits multiple small CPU reads.

## Gotchas
- `CopyTextureRegion` on a multisampled or depth-stencil resource must copy the whole subresource (no destination
  offsets, null source box), and the documentation says source and destination should have the same sample count;
  resolve MSAA to a single-sample texture first.
- Back buffers are often BGRA; swizzle when writing image files.
- A resource in a readback heap must be created in, and stay in, `COPY_DEST`.

## Verify
- [ ] The screenshot matches the presented image at odd widths (pitch handling); no CPU wait spikes in a profiler.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Read back data via a buffer", "Uploading texture data via a
buffer", `GetCopyableFootprints`, `CopyTextureRegion`, `ID3D12Resource::Map` and `D3D12_HEAP_TYPE`
(MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08). Confirmed: buffer-only readback resources, Map not
synchronising, 256-byte pitch and 512-byte placement constants, COPY_DEST requirement, write-back CPU caching, full
subresource and sample-count rules for MSAA copies. Removed unconfirmed claims: "D3D12 texture origin is top-left"
and the claim that MSAA copies into buffers are impossible (restated from the sample-count rule).
Method: documentation only; no commands were run.
