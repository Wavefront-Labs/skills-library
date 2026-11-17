---
id: computing-software.computer-graphics-engineering.opengl.vulkan-memory-aliasing-and-sparse-resources
name: vulkan-memory-aliasing-and-sparse-resources
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-memory, memory-aliasing, sparse-resources, transient-attachments, sparse-binding, lazily-allocated]
level: advanced
status: docs-checked
description: "Save Vulkan memory with aliasing of transient render targets, lazily allocated attachments, and sparse binding/residency for partially resident textures."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/sparsemem.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/resources.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/features.adoc", "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory aliasing and sparse resources

**Goal:** reuse memory between resources whose lifetimes do not overlap, and back huge
textures/buffers with memory only where needed.

## 1. Aliasing transient targets
Within a frame, a bloom chain, SSAO buffer and a post-process temp may never be live at the
same time. Bind them to the same memory:
```cpp
VkMemoryRequirements a, b; // from both images
// allocate max(size), alignment = max, memoryTypeBits = a.bits & b.bits
vkBindImageMemory(dev, imgA, mem, 0);
vkBindImageMemory(dev, imgB, mem, 0);
```
VMA: `vmaAllocateMemory` with merged requirements then `vmaBindImageMemory2` for each. A render
graph computes lifetimes and packs them automatically.
Rules when switching which resource is live: a barrier from the old resource's last use, and
the new resource's first use starts from `VK_IMAGE_LAYOUT_UNDEFINED` (contents are garbage) and
must be fully cleared or written. Set `VK_IMAGE_CREATE_ALIAS_BIT` only when aliases must
interpret each other's contents consistently: the spec requires identical creation parameters and identical memory binding for that.

## 2. Lazily allocated (tilers)
Depth or MSAA attachments used only inside a render pass: `VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT`
+ a memory type with `LAZILY_ALLOCATED`. A lazily allocated memory type may be backed lazily, so such attachments can stay without physical memory.

## 3. Sparse resources
Create with `VK_IMAGE_CREATE_SPARSE_BINDING_BIT | SPARSE_RESIDENCY_BIT` (check
`sparseResidencyImage2D` feature). Query tile shape with
`vkGetPhysicalDeviceSparseImageFormatProperties` (standard sparse block shapes are 64 KB, e.g. 128x128x1 for 32-bit texels). Bind pages
with `vkQueueBindSparse` on a queue with `VK_QUEUE_SPARSE_BINDING_BIT`, synchronised by
semaphores. The mip tail (small mips) is bound as a unit. Shaders can detect non-resident
reads with the SPIR-V `OpImageSparse*` instructions, which return a residency code (feature `shaderResourceResidency`).

## Gotchas
- Batch sparse binds into few `vkQueueBindSparse` calls and synchronise them with semaphores; software virtual texturing is the
  portable alternative.
- Aliasing hides bugs: a missing barrier shows as another pass's data bleeding in. Run
  synchronisation validation.
- Not all formats support sparse residency: check `vkGetPhysicalDeviceSparseImageFormatProperties` and the sparse residency features.

## Verify
- [ ] VRAM usage drops by the size of the aliased group; images look unchanged.
- [ ] Sparse texture shows fallback mip where pages are unbound and full detail where bound.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and `vk_mem_alloc.h`. Confirmed: all standard sparse image block shapes are 64 KB (sparsemem.adoc); the mip tail is bound as a region; `OpImageSparse*` instructions return a residency code and `shaderResourceResidency` is the feature (features.adoc, textures.adoc); aliasing rules and `ALIAS_BIT` semantics (resources.adoc); VMA's own documentation says a resource must be treated as uninitialised after aliasing and needs an image barrier from `VK_IMAGE_LAYOUT_UNDEFINED`, and `vmaAllocateMemory` and `vmaBindImageMemory2` exist. Removed the sparse bind timing claim, the MoltenVK claim, the GLSL `sparseTextureARB` name and the 'never get physical memory on mobile' claim.

Method: documentation only; no commands were run.
