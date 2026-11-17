---
id: computing-software.computer-graphics-engineering.opengl.vulkan-staging-buffer-uploads
name: vulkan-staging-buffer-uploads
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-memory, vk-memory-allocation, staging-buffer, gpu-upload, vkcmdcopybuffertoimage, rebar, host-visible-device-local, vma]
level: practitioner
status: docs-checked
description: "Upload meshes and textures to device-local Vulkan memory through staging buffers, batch copies, use ReBAR host-visible VRAM when present, and barrier correctly."
sources: ["https://gpuopen-librariesandsdks.github.io/VulkanMemoryAllocator/html/usage_patterns.html", "https://docs.vulkan.org/spec/latest/chapters/copies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan staging buffer uploads

**Goal:** static data ends up in the fastest (device-local) memory, uploads are batched,
and dynamic data takes the cheapest path the hardware offers.

## 1. Classic staging path
```cpp
// staging: CPU-visible, sequential write
VmaAllocationCreateInfo sa{}; sa.usage = VMA_MEMORY_USAGE_AUTO;
sa.flags = VMA_ALLOCATION_CREATE_HOST_ACCESS_SEQUENTIAL_WRITE_BIT | VMA_ALLOCATION_CREATE_MAPPED_BIT;
vmaCreateBuffer(vma, &stagingInfo /*TRANSFER_SRC*/, &sa, &staging, &stAlloc, &stInfo);
memcpy(stInfo.pMappedData, src, size);
// destination: device-local
VmaAllocationCreateInfo da{}; da.usage = VMA_MEMORY_USAGE_AUTO_PREFER_DEVICE;
vmaCreateBuffer(vma, &dstInfo /*VERTEX|INDEX|STORAGE|TRANSFER_DST*/, &da, &dst, &dAlloc, nullptr);
// record
VkBufferCopy r{0, 0, size}; vkCmdCopyBuffer(cmd, staging, dst, 1, &r);
// barrier: COPY/TRANSFER_WRITE -> VERTEX_INPUT/VERTEX_ATTRIBUTE_READ (or the consuming stage)
```

## 2. Textures
```cpp
transition(img, UNDEFINED -> TRANSFER_DST_OPTIMAL);
VkBufferImageCopy c{}; c.bufferOffset = off; c.imageSubresource = {VK_IMAGE_ASPECT_COLOR_BIT, mip, 0, 1};
c.imageExtent = {w >> mip, h >> mip, 1};          // bufferRowLength 0 = tightly packed
vkCmdCopyBufferToImage(cmd, staging, img, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, mipCount, copies);
transition(img, TRANSFER_DST_OPTIMAL -> SHADER_READ_ONLY_OPTIMAL);
```
Block-compressed formats: the buffer offset must be a multiple of the texel block size, and the copy extent a multiple of the
texel block extent unless the region reaches the edge of the image subresource. `optimalBufferCopyOffsetAlignment` is the optimal
buffer offset alignment. On a queue family without graphics or compute support, `bufferOffset` must be a multiple of 4.

## 3. Batch
One big staging ring (size it from your measured load), many regions, one command buffer, one submit per
batch; reclaim ring space when the batch's fence/timeline value completes. Per-asset
submits with `vkQueueWaitIdle` are the most common loading-time sink.

## 4. ReBAR / host-visible device-local
On desktop with Resizable BAR (and on integrated/UMA GPUs) there is a
`DEVICE_LOCAL | HOST_VISIBLE` type covering most of VRAM. For **per-frame dynamic data**
(uniforms, instance data) write directly there and skip the copy:
```cpp
a.flags = VMA_ALLOCATION_CREATE_HOST_ACCESS_SEQUENTIAL_WRITE_BIT |
          VMA_ALLOCATION_CREATE_HOST_ACCESS_ALLOW_TRANSFER_INSTEAD_BIT | VMA_ALLOCATION_CREATE_MAPPED_BIT;
vmaGetAllocationMemoryProperties(vma, alloc, &props);
if (!(props & VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)) { /* VMA fell back: use staging copy */ }
```
Per the VMA documentation, PC graphics cards expose only 256 MB of BAR by default unless ReBAR is enabled in the BIOS — keep it for small, hot buffers.

## Gotchas
- VMA's rule for uncached, write-combined memory: only sequential writes and no reads.
- Non-coherent memory (`HOST_COHERENT` absent) needs
  `vmaFlushAllocation` after writing.
- Forgetting the post-copy barrier is a synchronisation error even when one implementation happens to hide it.
- Staging buffers freed before the copy executes = use-after-free on the GPU; tie
  lifetime to the batch's completion.

## Verify
- [ ] Static meshes/textures live in DEVICE_LOCAL-only memory (VMA stats JSON confirms).
- [ ] Load-time submits are O(batches); no `vkQueueWaitIdle` in the asset loader.
- [ ] Validation clean; textures correct on at least two vendors.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (validusage.json for vkCmdCopyBufferToImage, chapters/copies.adoc, chapters/limits.adoc) and the VMA header vk_mem_alloc.h (main, Advanced data uploading).
Confirmed: VMA flags and functions used (HOST_ACCESS_SEQUENTIAL_WRITE_BIT, ALLOW_TRANSFER_INSTEAD_BIT, MAPPED_BIT, MEMORY_USAGE_AUTO and AUTO_PREFER_DEVICE, vmaGetAllocationMemoryProperties, vmaFlushAllocation); compressed-format offset and extent rules; optimalBufferCopyOffsetAlignment; 256 MB default BAR statement and write-combined rule. Removed the ring size and mobile-coherence claims.
Method: documentation only; no commands were run.
