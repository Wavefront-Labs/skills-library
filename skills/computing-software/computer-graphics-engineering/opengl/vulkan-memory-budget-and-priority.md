---
id: computing-software.computer-graphics-engineering.opengl.vulkan-memory-budget-and-priority
name: vulkan-memory-budget-and-priority
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-memory, memory-budget, vk-ext-memory-budget, memory-priority]
level: advanced
status: docs-checked
description: "Stay within VRAM using VK_EXT_memory_budget (heap budget/usage), react to pressure by streaming down, and set VK_EXT_memory_priority/pageable hints."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_memory_budget.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_memory_priority.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_pageable_device_local_memory.adoc", "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator/blob/master/include/vk_mem_alloc.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory budget and priority

Heap `size` is the physical size, not what you may use: other processes can use the same device
memory. Going over `heapBudget` may cause allocations to start failing or performance to degrade.

## Query budget
```c
VkPhysicalDeviceMemoryBudgetPropertiesEXT budget = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_MEMORY_BUDGET_PROPERTIES_EXT };
VkPhysicalDeviceMemoryProperties2 mp = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_MEMORY_PROPERTIES_2, &budget };
vkGetPhysicalDeviceMemoryProperties2(gpu, &mp);
for (uint32_t h = 0; h < mp.memoryProperties.memoryHeapCount; ++h)
    printf("heap %u: usage %llu / budget %llu\n", h, budget.heapUsage[h], budget.heapBudget[h]);
```
`heapUsage` = estimated usage of the current process, `heapBudget` = a guideline for how much total
memory from the heap the current process can use. Values are implementation-dependent and change with
system activity; the extension suggests querying at an interval (per frame, per few seconds). With VMA:
`vmaGetHeapBudgets` (enable `VMA_ALLOCATOR_CREATE_EXT_MEMORY_BUDGET_BIT`).

## Reacting to pressure
- Keep a margin below the budget. Near or above it: drop texture mip levels for distant objects,
  shrink streaming pools, lower render resolution or shadow map sizes.
- VMA: `VMA_ALLOCATION_CREATE_WITHIN_BUDGET_BIT` fails allocations that would exceed budget
  instead of overcommitting; handle the failure by evicting.
- The budget can change when other processes use the heap; treat it as dynamic.

## Priority hints
```c
VkMemoryPriorityAllocateInfoEXT prio = { VK_STRUCTURE_TYPE_MEMORY_PRIORITY_ALLOCATE_INFO_EXT };
prio.priority = 1.0f;          // range 0..1: higher for render targets and hot buffers, lower for streamed textures
allocInfo.pNext = &prio;
```
`VK_EXT_pageable_device_local_memory` (exposed when the OS pages device-local memory; enable the
`pageableDeviceLocalMemory` feature) adds `vkSetDeviceMemoryPriorityEXT` to change the priority of
existing allocations (e.g. when a texture becomes visible). VMA: set `VmaAllocationCreateInfo::priority` with `VMA_ALLOCATOR_CREATE_EXT_MEMORY_PRIORITY_BIT`.

## Gotchas
- Budgets are reported per heap: check every heap you allocate from, and don't assume a separate
  VRAM heap exists.

## Verify
- [ ] Debug overlay shows usage vs budget per heap; with a second VRAM-hungry app open, your app reduces quality instead of stuttering.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: VK_EXT_memory_budget: `heapBudget` is a guideline for the current process before allocations may fail or performance degrade; `heapUsage` is the current process's estimated usage; query per frame or every few seconds; designed to work with VK_EXT_memory_priority.
- Confirmed: VK_EXT_memory_priority: priority is 0..1 (VUID-VkMemoryPriorityAllocateInfoEXT-priority-02602); VK_EXT_pageable_device_local_memory adds `vkSetDeviceMemoryPriorityEXT` and a `pageableDeviceLocalMemory` feature.
- Confirmed: VMA header: `VMA_ALLOCATOR_CREATE_EXT_MEMORY_BUDGET_BIT`, `VMA_ALLOCATOR_CREATE_EXT_MEMORY_PRIORITY_BIT`, `vmaGetHeapBudgets`, and `VMA_ALLOCATION_CREATE_WITHIN_BUDGET_BIT` (returns `VK_ERROR_OUT_OF_DEVICE_MEMORY` if the budget would be exceeded) exist.
- Removed WDDM, ReBAR size and driver-internal allocation remarks (no source found).

Method: documentation only; no commands were run.
