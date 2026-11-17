---
id: computing-software.computer-graphics-engineering.opengl.vulkan-dedicated-allocations-and-memory-requirements
name: vulkan-dedicated-allocations-and-memory-requirements
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-memory, dedicated-allocation, vkgetbuffermemoryrequirements, memory-requirements]
level: advanced
status: docs-checked
description: "Read Vulkan memory requirements (size, alignment, type bits), decide when to use dedicated allocations, and query requirements before resource creation."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/resources.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory requirements and dedicated allocations

## Requirements
```c
VkMemoryDedicatedRequirements ded = { VK_STRUCTURE_TYPE_MEMORY_DEDICATED_REQUIREMENTS };
VkMemoryRequirements2 req = { VK_STRUCTURE_TYPE_MEMORY_REQUIREMENTS_2, &ded };
VkImageMemoryRequirementsInfo2 info = { VK_STRUCTURE_TYPE_IMAGE_MEMORY_REQUIREMENTS_INFO_2, NULL, image };
vkGetImageMemoryRequirements2(device, &info, &req);
// req.memoryRequirements.size / .alignment / .memoryTypeBits
// ded.prefersDedicatedAllocation / ded.requiresDedicatedAllocation
```
- `size` can be larger than width*height*bytes-per-texel; always use the returned value.
- `alignment` is the required alignment of the resource's offset within the memory; suballocate respecting it.
- `memoryTypeBits`: bit i set = memory type i allowed. Intersect with your desired properties.
- `bufferImageGranularity` limit: linear (buffers, linear images) and optimal-tiled images
  placed in the same allocation must be separated by this granularity (a power of two; the
  spec requires implementations to report at most 131072 bytes). VMA handles it.

## Before creating the resource (1.3 / maintenance4)
`vkGetDeviceImageMemoryRequirements` / `vkGetDeviceBufferMemoryRequirements` take the create
info instead of the object: size pools or check budgets without creating throwaway resources.

## Dedicated allocations
```c
VkMemoryDedicatedAllocateInfo dai = { VK_STRUCTURE_TYPE_MEMORY_DEDICATED_ALLOCATE_INFO, NULL, image, VK_NULL_HANDLE };
VkMemoryAllocateInfo ai = { VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO, &dai, req.memoryRequirements.size, typeIndex };
vkAllocateMemory(device, &ai, NULL, &mem);
vkBindImageMemory(device, image, mem, 0);
```
Use when:
- `requiresDedicatedAllocation` is true (must); the spec says this can happen for external-memory handle types that need a dedicated allocation.
- `prefersDedicatedAllocation` is true: the implementation indicates a dedicated allocation may perform better (suballocating is still allowed).
- Very large resources relative to your block size, where suballocation wastes space (a heuristic, not a spec rule).
With VMA: `VMA_ALLOCATION_CREATE_DEDICATED_MEMORY_BIT`, or let VMA decide automatically (it reads
the dedicated requirements when `VK_KHR_dedicated_allocation`/1.1 is available).

## Gotchas
- `maxMemoryAllocationCount` (guaranteed minimum 4096): dedicating every texture exhausts it. Dedicate only
  render targets and huge resources.
- Allocate device memory at load time rather than in the frame loop, and keep the count well below the limit.
- Requirements depend on the whole create info (flags, usage, tiling, format), so don't cache them by dimensions alone.

## Verify
- [ ] Log of allocations shows dedicated memory only where required/preferred; allocation count well under the limit.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and `vk_mem_alloc.h` from the VulkanMemoryAllocator repository. Confirmed: `VkMemoryDedicatedRequirements` semantics (`prefers` = may perform better, `requires` can be true for external handle types); `vkGetDeviceImageMemoryRequirements`/`vkGetDeviceBufferMemoryRequirements` exist (core 1.3 via maintenance4); `maxMemoryAllocationCount` minimum 4096; `bufferImageGranularity` required maximum 131072; `VMA_ALLOCATION_CREATE_DEDICATED_MEMORY_BIT` and `VMA_DEDICATED_ALLOCATION` (needs VK_KHR_get_memory_requirements2 and VK_KHR_dedicated_allocation) exist. Removed the 64 KB / 4 KB alignment figures, the NVIDIA 64 KB granularity figure, vendor placement claims and the allocation-time claim, which no document covers.

Method: documentation only; no commands were run.
