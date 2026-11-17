---
id: computing-software.computer-graphics-engineering.directx.directstorage-asset-loading
name: directstorage-asset-loading
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, d3d12-advanced, directstorage, gdeflate, gpu-decompression, asset-streaming, nvme, dstorage-queue]
level: advanced
status: docs-checked
description: "Load assets with DirectStorage on Windows: request queues straight into D3D12 buffers and textures, GDeflate GPU decompression, batching, fences and status arrays."
sources: ["https://github.com/microsoft/DirectStorage/blob/main/Docs/DeveloperGuidance.md", "https://github.com/microsoft/DirectStorage/blob/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DirectStorage asset loading

**Goal:** stream large textures/meshes from storage to VRAM with minimal CPU,
decompressing on the GPU with the built-in GDeflate format.

## 1. Setup
```cpp
ComPtr<IDStorageFactory> factory; DStorageGetFactory(IID_PPV_ARGS(&factory));
DSTORAGE_QUEUE_DESC qd{};
qd.SourceType = DSTORAGE_REQUEST_SOURCE_FILE;
qd.Capacity   = 1024;                               // slots; each enqueued operation uses one until it completes
qd.Priority   = DSTORAGE_PRIORITY_NORMAL;
qd.Device     = d3dDevice.Get();
ComPtr<IDStorageQueue> queue; factory->CreateQueue(&qd, IID_PPV_ARGS(&queue));
ComPtr<IDStorageFile> file; factory->OpenFile(L"assets.pak", IID_PPV_ARGS(&file));
```
By default DirectStorage expects `dstoragecore.dll` next to the game executable (set `DStorageSDKPath`
to use another folder).

## 2. Enqueue requests
```cpp
DSTORAGE_REQUEST r{};
r.Options.SourceType = DSTORAGE_REQUEST_SOURCE_FILE;
r.Options.DestinationType = DSTORAGE_REQUEST_DESTINATION_TEXTURE_REGION;   // or _BUFFER, _MULTIPLE_SUBRESOURCES
r.Options.CompressionFormat = DSTORAGE_COMPRESSION_FORMAT_GDEFLATE;
r.Source.File = { file.Get(), offset, compressedSize };
r.UncompressedSize = rawSize;
r.Destination.MultipleSubresources = { texture.Get(), 0 /*first subresource*/ };
queue->EnqueueRequest(&r);
// completion
queue->EnqueueSignal(fence.Get(), ++fenceValue);   // D3D12 fence
queue->Submit();
```
An `IDStorageStatusArray` stores the results of operations; enqueue a status entry to read per-request
error codes (`HRESULT`).

## 3. Pack format
- Texture request data must be laid out in a format suitable for `CopyTextureRegion`;
  `ID3D12Device::GetCopyableFootprints` gives the layout.
- Compress offline with `IDStorageCompressionCodec` (`DStorageCreateCompressionCodec` with
  `DSTORAGE_COMPRESSION_FORMAT_GDEFLATE`).
- No 4 KiB alignment or size restriction applies (unlike Win32 asynchronous I/O), so do not pad data.
- Destination resources must already exist.

## 4. Throughput
- Queue slots are limited (set at queue creation) and stay in use until the operation completes.
- GPU decompression uses two staging buffers in VRAM (input and output), each sized by
  `IDStorageFactory::SetStagingBufferSize()`.
- Custom CPU decompression is possible via `IDStorageCustomDecompressionQueue`.

## Gotchas
- A request whose uncompressed size exceeds the staging buffer size fails; raise
  `SetStagingBufferSize()` or split the request.
- Before using the loaded resource on a D3D12 queue, wait on the fence signalled through
  `EnqueueSignal`.

## Verify
- Status array reports S_OK for all requests; a corrupt pack file reports errors cleanly.

## Checked

2026-10-26. Checked against the microsoft/DirectStorage repository README and Docs/DeveloperGuidance.md (commit of 2026-10-21):
queue operation slots, staging buffers and SetStagingBufferSize failure rule, GPU decompression staging in VRAM,
GDeflate codec creation call, IDStorageStatusArray, custom decompression queue, no 4 KiB alignment restriction,
CopyTextureRegion layout via GetCopyableFootprints, dstoragecore.dll location. Removed the unconfirmed minimum Windows
build, default 32 MiB staging size, 64 KiB tile size, DSTORAGE_MAX_QUEUE_CAPACITY, NuGet DLL list, PIX tracks and
storage-media comments.
Method: documentation only; no commands were run.
