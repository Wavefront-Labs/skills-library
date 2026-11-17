---
id: computing-software.computer-graphics-engineering.opengl.vulkan-memory-heaps-and-type-selection
name: vulkan-memory-heaps-and-type-selection
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-memory, memory-types, memory-heaps, vma, rebar, device-local, host-visible]
level: advanced
status: docs-checked
description: "Choose Vulkan memory correctly: heaps vs types, memoryTypeBits filtering, DEVICE_LOCAL vs HOST_VISIBLE, ReBAR, coherency, budgets and VMA usage flags."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/memory.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory heaps and type selection

**Goal:** put each resource in the right memory type on discrete, integrated and mobile GPUs.

## 1. The model
`vkGetPhysicalDeviceMemoryProperties` gives **heaps** (pools with a size, for example VRAM or system RAM) and **types** (property flag combos that live in a heap).
Pick a type with:
```cpp
uint32_t findType(uint32_t bits, VkMemoryPropertyFlags want) {
    for (uint32_t i = 0; i < props.memoryTypeCount; ++i)
        if ((bits & (1u << i)) && (props.memoryTypes[i].propertyFlags & want) == want) return i;
    return UINT32_MAX;
}
// bits = VkMemoryRequirements::memoryTypeBits from vkGet*MemoryRequirements
```
The spec orders types so that one whose flags are a strict subset of another's comes first, so the first type containing the flags you require has the fewest extras; unrelated flag combinations have no defined order, so handle fallbacks.

## 2. Typical choices (discrete PC)
| Resource | Flags |
|---|---|
| Textures, render targets, static meshes | `DEVICE_LOCAL` |
| Staging upload | `HOST_VISIBLE | HOST_COHERENT` (system RAM) |
| Per-frame uniforms, dynamic vertices | `DEVICE_LOCAL | HOST_VISIBLE` (BAR / ReBAR) if present, else host memory |
| Readback | `HOST_VISIBLE | HOST_CACHED` |
A discrete GPU may or may not expose a `DEVICE_LOCAL | HOST_VISIBLE` type (BAR); with Resizable BAR enabled it can cover the whole of VRAM (VMA docs). On
unified-memory GPUs many types can be `DEVICE_LOCAL | HOST_VISIBLE`: check the flags and skip the staging copy where it makes sense.

## 3. VMA does this for you
```cpp
VmaAllocationCreateInfo ai{}; ai.usage = VMA_MEMORY_USAGE_AUTO;
ai.flags = VMA_ALLOCATION_CREATE_HOST_ACCESS_SEQUENTIAL_WRITE_BIT | VMA_ALLOCATION_CREATE_MAPPED_BIT;
vmaCreateBuffer(vma, &bci, &ai, &buf, &alloc, &info);   // info.pMappedData persistently mapped
```
`HOST_ACCESS_SEQUENTIAL_WRITE` lets VMA choose host-visible device-local (BAR/unified) memory; add
`HOST_ACCESS_ALLOW_TRANSFER_INSTEAD` and check the resulting flags to decide whether a staging
copy is needed.

## Gotchas
- `maxMemoryAllocationCount` is guaranteed to be at least 4096: suballocate, never one `vkAllocateMemory`
  per resource.
- Non-coherent memory needs `vkFlushMappedMemoryRanges` / `Invalidate` aligned to
  `nonCoherentAtomSize`.
- Write-combined (uncached) memory is very slow to read from the CPU; never read back from it.
- Track usage with `VK_EXT_memory_budget` (`vmaGetHeapBudgets`) and stay within the reported budget.

## Verify
- [ ] Log chosen type index and flags per allocation class on 3 GPUs (dGPU, iGPU, mobile).
- [ ] Budget stays below heap size under the heaviest scene.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23), `memory.adoc` and `limits.adoc`, and `vk_mem_alloc.h`. Confirmed: type ordering rule (strict-subset flag sets come first, no ordering between unrelated sets); at least one `HOST_VISIBLE | HOST_COHERENT` type and one `DEVICE_LOCAL` type must exist; `maxMemoryAllocationCount` minimum 4096; VMA names `VMA_MEMORY_USAGE_AUTO`, `VMA_ALLOCATION_CREATE_HOST_ACCESS_SEQUENTIAL_WRITE_BIT`, `..._HOST_ACCESS_ALLOW_TRANSFER_INSTEAD_BIT`, `..._MAPPED_BIT`, `vmaGetHeapBudgets`; VMA documents that a host-visible device-local type (BAR) may or may not exist and may cover all VRAM with ReBAR, and that sequential-write memory may be uncached and write-combined and slow to read. Removed the 256 MB BAR figure and the frame-time spike claim.

Method: documentation only; no commands were run.
