---
id: computing-software.computer-graphics-engineering.gpu-optimisation.pcie-transfer-optimisation
name: pcie-transfer-optimisation
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-memory-bandwidth, pcie-bandwidth, copy-queue, readback, pinned-memory, streaming, rebar]
level: advanced
status: docs-checked
description: "Optimise CPU-GPU transfers over PCIe: batching, pinned memory, avoiding GPU reads from system memory, and readback latency hiding."
sources: ["https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/readback-data-using-heaps", "https://gpuopen.com/learn/vulkan-device-memory/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCIe transfer optimisation

## 1. Numbers
Host-to-device transfers over PCIe are the slowest link in GPU computing, with peak bandwidth far
below device-memory bandwidth (NVIDIA transfer blog). GPUOpen's Vulkan memory guide contrasts a
GPU's device-local bandwidth with the PCIe bus limit per direction. Anything the GPU reads
repeatedly should be in VRAM. Look up your link generation and width for actual figures.

## 2. Uploads
- Batch: many small transfers have per-transfer overhead; pack into large staging buffers.
- Pinned (page-locked) host memory gives higher transfer bandwidth than pageable memory: in CUDA
  allocate it with `cudaMallocHost()` or `cudaHostAlloc()` (NVIDIA blog).

## 3. Don't let the GPU read system memory in hot paths
Buffers in upload heaps/host-visible memory read by shaders each draw travel over PCIe every time.
Fine for small per-frame constants read once; terrible for large vertex buffers or textures. Copy to
device-local memory. For small total sizes, GPUOpen recommends `DEVICE_LOCAL` + `HOST_VISIBLE` memory for
CPU uploads, which the GPU reads without crossing PCIe.

## 4. Readbacks
- GPU -> CPU readback via a D3D12 readback heap (see Microsoft's readback page) or, in Vulkan, memory
  that is `HOST_VISIBLE` + `HOST_COHERENT` + `HOST_CACHED`: GPUOpen says this is the only memory type
  with cached CPU reads. Wait on a fence before mapping, ideally a few frames later with a ring of buffers.
- Read only what you need (a small reduction result, not full images).

## 5. Measure
- Use a GPU profiler's PCIe throughput counters, and check the link generation and width your
  system actually negotiates.

## Gotchas
- Running out of VRAM can push resources to system memory: silent PCIe traffic and slowdowns;
  monitor the VRAM budget through your API's memory-budget query.

## Verify
- [ ] No large shader reads from system memory in captures.
- [ ] VRAM usage stays under budget; readbacks never stall the frame.

## Checked
2026-11-01. Confirmed: NVIDIA "How to Optimize Data Transfers in CUDA C/C++" (PCIe slowest link, pinned memory via `cudaMallocHost`/`cudaHostAlloc`, higher bandwidth than pageable); GPUOpen "Vulkan device memory" (`DEVICE_LOCAL`+`HOST_VISIBLE` for small uploads, `HOST_VISIBLE`+`HOST_COHERENT`+`HOST_CACHED` as the cached-read type, PCIe vs device-local bandwidth); Microsoft D3D12 readback-heaps page. Removed unconfirmed: per-generation bandwidth table and ratios, copy-queue and DirectStorage advice, tool commands, laptop link widths, budget API names.
Method: documentation only; no commands were run.
