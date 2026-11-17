---
id: computing-software.computer-graphics-engineering.opengl.vulkan-resizable-bar-host-visible-vram
name: vulkan-resizable-bar-host-visible-vram
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-memory, resizable-bar, device-local-host-visible, rebar]
level: advanced
status: docs-checked
description: "Use DEVICE_LOCAL|HOST_VISIBLE (ReBAR) Vulkan memory to write per-frame data straight into VRAM, with fallbacks when the BAR is only 256 MB."
sources: ["https://gpuopen-librariesandsdks.github.io/VulkanMemoryAllocator/html/usage_patterns.html", "https://docs.vulkan.org/spec/latest/appendices/VK_EXT_memory_budget.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resizable BAR / host-visible VRAM

Discrete GPUs may or may not expose a memory type that is both `DEVICE_LOCAL` and `HOST_VISIBLE`.
Per the VMA documentation, PC graphics cards have only 256 MB of BAR by default; with ReBAR enabled in the motherboard BIOS
the entire VRAM can be available for CPU mapping.

## Detect
```c
for (uint32_t i = 0; i < mp.memoryTypeCount; ++i) {
    VkMemoryPropertyFlags f = mp.memoryTypes[i].propertyFlags;
    if ((f & VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT) && (f & VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT)) {
        VkDeviceSize heap = mp.memoryHeaps[mp.memoryTypes[i].heapIndex].size;
        bool rebar = heap > 256ull * 1024 * 1024;   // heuristic: full BAR vs the default 256 MB window
    }
}
```

## What to put there
- Per-frame dynamic data written by the CPU and read by the GPU once or a few times:
  uniform/constant ring buffers, instance transforms, dynamic vertex data (UI, particles), indirect
  args written by the CPU. Writing directly avoids the staging copy and the transfer pass.
- **Not** large static assets: upload those once via staging into plain `DEVICE_LOCAL` memory;
  the copy is one-off and leaves the BAR heap free.
- Never read from it on the CPU: VMA's rule for uncached, write-combined memory is sequential writes only and no reads.

## Writing rules
- Write sequentially with `memcpy`; avoid read-modify-write and random access.
- Persistently map once.
- Size the ring for frames in flight; protect with the frame fence.

## With VMA
```c
VmaAllocationCreateInfo ci = {};
ci.usage = VMA_MEMORY_USAGE_AUTO;
ci.flags = VMA_ALLOCATION_CREATE_HOST_ACCESS_SEQUENTIAL_WRITE_BIT |
           VMA_ALLOCATION_CREATE_HOST_ACCESS_ALLOW_TRANSFER_INSTEAD_BIT |
           VMA_ALLOCATION_CREATE_MAPPED_BIT;
vmaCreateBuffer(allocator, &bufCI, &ci, &buf, &alloc, &info);
VkMemoryPropertyFlags props; vmaGetAllocationMemoryProperties(allocator, alloc, &props);
if (props & VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT) memcpy(info.pMappedData, src, n);   // direct
else { /* got non-mappable VRAM: write to staging, record vkCmdCopyBuffer */ }
```
`ALLOW_TRANSFER_INSTEAD` lets VMA pick ReBAR memory when available and fall back to
device-local + staging otherwise; your code handles both branches.

## Gotchas
- The BAR heap is small without ReBAR; don't fill it, and check the budget (`VK_EXT_memory_budget`).
- Integrated GPUs/UMA: every device-local type is host-visible; same code path applies.
- Measure: VMA notes that writes through PCI Express may have limited performance; keep staging for bulk loads.

## Verify
- [ ] Startup log reports ReBAR presence; GPU trace shows no per-frame copy pass for dynamic buffers when ReBAR is on.

## Checked
Checked 2026-10-26 against the VMA header vk_mem_alloc.h (main; usage patterns: advanced data uploading) and Vulkan-Docs xml/vk.xml.
Confirmed: 256 MB default BAR and ReBAR wording, the recommended flag pair HOST_ACCESS_SEQUENTIAL_WRITE_BIT with ALLOW_TRANSFER_INSTEAD_BIT, MAPPED_BIT, vmaGetAllocationMemoryProperties fallback pattern, write-combined sequential-write rule, VK_EXT_memory_budget exists. Removed AMD SAM naming, cache-line and throughput claims.
Method: documentation only; no commands were run.
