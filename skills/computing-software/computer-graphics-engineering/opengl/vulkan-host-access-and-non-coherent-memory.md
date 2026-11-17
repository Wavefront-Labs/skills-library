---
id: computing-software.computer-graphics-engineering.opengl.vulkan-host-access-and-non-coherent-memory
name: vulkan-host-access-and-non-coherent-memory
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-synchronization, vkflushmappedmemoryranges, host-coherent, host-cached-readback]
level: advanced
status: docs-checked
description: "Synchronise CPU access to mapped Vulkan memory: flush/invalidate for non-coherent memory, nonCoherentAtomSize, host barriers and safe readback."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/memory.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator/blob/master/include/vk_mem_alloc.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host access and non-coherent memory

## Memory property combos
| Properties | Use | Rule |
|---|---|---|
| `HOST_VISIBLE` + `HOST_COHERENT` | uploads | no flush needed; writes visible at submit |
| `HOST_VISIBLE` + `HOST_CACHED` (not coherent) | readback | flush after CPU writes, invalidate before CPU reads |
| `HOST_VISIBLE` + `HOST_COHERENT` + `HOST_CACHED` | readback | no invalidate needed; still needs the HOST_READ memory barrier and a fence or semaphore wait |
| `DEVICE_LOCAL` + `HOST_VISIBLE` | device-local memory the host can map | as above, depending on the coherent bit |

## CPU writes -> GPU reads
```c
memcpy(mapped + off, data, size);
if (!(props & VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)) {
    VkMappedMemoryRange r = { VK_STRUCTURE_TYPE_MAPPED_MEMORY_RANGE, NULL, memory,
        alignDown(off, atom), alignUp(off + size, atom) - alignDown(off, atom) };   // atom = nonCoherentAtomSize
    vkFlushMappedMemoryRanges(device, 1, &r);
}
vkQueueSubmit2(...);    // host write ordering guarantee: available host writes become visible to the device
```
With VMA: `vmaFlushAllocation(allocator, alloc, off, size)` handles coherency and alignment
(no-op on coherent memory).

## GPU writes -> CPU reads
```c
// in the command buffer after the GPU write (e.g. copy to readback buffer):
VkMemoryBarrier2 b = { VK_STRUCTURE_TYPE_MEMORY_BARRIER_2 };
b.srcStageMask = VK_PIPELINE_STAGE_2_COPY_BIT;   b.srcAccessMask = VK_ACCESS_2_TRANSFER_WRITE_BIT;
b.dstStageMask = VK_PIPELINE_STAGE_2_HOST_BIT;   b.dstAccessMask = VK_ACCESS_2_HOST_READ_BIT;
// ... submit with fence; later:
vkWaitForFences(device, 1, &fence, VK_TRUE, UINT64_MAX);    // or timeline semaphore wait
if (!coherent) vkInvalidateMappedMemoryRanges(device, 1, &range);   // aligned to atom
read(mapped);
```
The fence wait alone is not enough: the spec requires a memory barrier whose second scope includes
`HOST_BIT` / `HOST_READ_BIT` (a memory domain operation) before the host reads device writes.

## Gotchas
- In a `VkMappedMemoryRange`, `offset` must be a multiple of `nonCoherentAtomSize`, and `size` must be a
  multiple of it, `VK_WHOLE_SIZE`, or reach the end of the memory object. The limit is at most 256.
- `vkMapMemory` requires that the `VkDeviceMemory` is not currently host mapped, so map once and keep
  the pointer.

## Verify
- [ ] Test on a platform that exposes non-coherent memory types, with validation on; readback values correct.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Host write ordering guarantee: queue submission defines a memory dependency covering host writes that are available to the host memory domain; non-coherent writes need `vkFlushMappedMemoryRanges` first; a memory barrier whose destination includes `HOST_READ_BIT` performs the memory domain operation for host reads (synchronization chapter).
- Confirmed: VkMappedMemoryRange rules: offset multiple of `nonCoherentAtomSize`; size a multiple of it, `VK_WHOLE_SIZE` or reaching the end of the memory (memory chapter); limits table: `nonCoherentAtomSize` at most 256; `vkMapMemory` memory must not be currently host mapped (VUID-vkMapMemory-memory-00678).
- Confirmed: VMA: `vmaFlushAllocation` rounds offset and size to `nonCoherentAtomSize` and is ignored for coherent or non-host-visible memory.
- Removed write-combined speed, suballocation corruption and platform remarks (no source found); fixed table cells that contained pipe characters.

Method: documentation only; no commands were run.
