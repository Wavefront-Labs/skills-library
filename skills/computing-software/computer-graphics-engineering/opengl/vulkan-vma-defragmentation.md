---
id: computing-software.computer-graphics-engineering.opengl.vulkan-vma-defragmentation
name: vulkan-vma-defragmentation
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-memory, vma-defragmentation, memory-fragmentation, vma-statistics]
level: sme
status: docs-checked
description: "Defragment Vulkan memory with VMA's incremental defragmentation passes: moving allocations, recreating resources, copies and barriers, plus measuring waste."
sources: ["https://gpuopen-librariesandsdks.github.io/VulkanMemoryAllocator/html/defragmentation.html", "https://gpuopen-librariesandsdks.github.io/VulkanMemoryAllocator/html/statistics.html", "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMA defragmentation

Long-running apps that stream assets fragment their memory blocks: total free memory is high
but no block can fit a new large allocation, so VMA allocates new blocks (budget creep).

## Measure first
```c
VmaTotalStatistics stats; vmaCalculateStatistics(allocator, &stats);
// stats.total.statistics.blockBytes vs allocationBytes -> wasted fraction
char* json; vmaBuildStatsString(allocator, &json, VK_TRUE);   // detailed JSON map of blocks and allocations
vmaFreeStatsString(allocator, json);
```
The header documents `blockBytes - allocationBytes` as the memory allocated from Vulkan but not used by allocations. Defragment when that waste crosses a threshold you choose from measurements.

## Incremental API (current VMA header)
```c
VmaDefragmentationInfo di = {};
di.flags = VMA_DEFRAGMENTATION_FLAG_ALGORITHM_BALANCED_BIT;
di.maxBytesPerPass = 64ull << 20;          // spread work over frames
di.maxAllocationsPerPass = 64;
VmaDefragmentationContext ctx; vmaBeginDefragmentation(allocator, &di, &ctx);
for (;;) {
    VmaDefragmentationPassMoveInfo pass;
    if (vmaBeginDefragmentationPass(allocator, ctx, &pass) == VK_SUCCESS) break;   // VK_SUCCESS = no more moves; VK_INCOMPLETE = moves pending
    for (uint32_t i = 0; i < pass.moveCount; ++i) {
        VmaDefragmentationMove& m = pass.pMoves[i];
        VmaAllocationInfo ai; vmaGetAllocationInfo(allocator, m.srcAllocation, &ai);
        Resource* r = (Resource*)ai.pUserData;                  // set via vmaSetAllocationUserData at creation
        if (!r->movable) { m.operation = VMA_DEFRAGMENTATION_MOVE_OPERATION_IGNORE; continue; }
        r->newHandle = recreateResource(r);                     // same create info
        vmaBindBufferMemory(allocator, m.dstTmpAllocation, r->newHandle);   // or vmaBindImageMemory
        recordCopy(cmd, r->handle, r->newHandle);               // vkCmdCopyBuffer / vkCmdCopyImage + barriers
    }
    submitAndWait(cmd);          // or wait on a fence frames later
    for (each move) { destroyOld(r); r->handle = r->newHandle; updateDescriptors(r); }
    if (vmaEndDefragmentationPass(allocator, ctx, &pass) == VK_SUCCESS) break;   // VK_INCOMPLETE = run another pass
}
vmaEndDefragmentation(allocator, ctx, NULL);
```
VMA only decides *where* to move; you recreate resources, copy contents, and fix references.

## Rules
- Images need layout handling: transition the new image to `TRANSFER_DST_OPTIMAL`, copy, then to
  the original layout; the old image must be in a readable layout.
- Mark resources that are in use by in-flight frames or that you can't re-point as `IGNORE`, or
  `DESTROY` for allocations you no longer need.
- Descriptors (or bindless table slots / buffer device addresses) must be updated to the new handles
  after the copy completes and before the next use.
- Render targets that are rewritten every frame don't need copies: just recreate.

## Alternatives
- Avoid fragmentation: separate pools by lifetime (static level data vs streaming), fixed-size
  pools for streaming textures (slab per mip size), linear allocators for per-frame data.

## Verify
- [ ] Wasted bytes drop after defragmentation; no visual corruption and no validation errors on moved resources.

## Checked
Checked 2026-10-26 against the VMA header include/vk_mem_alloc.h (main; defragmentation and statistics documentation).
Confirmed: vmaBeginDefragmentation, vmaBeginDefragmentationPass, vmaEndDefragmentationPass, vmaEndDefragmentation; VK_SUCCESS and VK_INCOMPLETE meanings; VMA_DEFRAGMENTATION_FLAG_ALGORITHM_BALANCED_BIT; maxBytesPerPass and maxAllocationsPerPass; move operations COPY, IGNORE and DESTROY; dstTmpAllocation bound with vmaBindBufferMemory/vmaBindImageMemory; vmaCalculateStatistics, blockBytes and allocationBytes. Removed the VmaDumpVis tool mention and the numeric waste threshold.
Method: documentation only; no commands were run.
