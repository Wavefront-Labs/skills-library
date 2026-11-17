---
id: computing-software.computer-graphics-engineering.opengl.vulkan-multi-queue-submission-and-priorities
name: vulkan-multi-queue-submission-and-priorities
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, command-buffers, queue-priorities, dedicated-transfer-queue, async-compute-vulkan]
level: advanced
status: docs-checked
description: "Use multiple Vulkan queues: pick dedicated transfer/compute families, set queue priorities and global priority, and synchronise cross-queue work."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/devsandqueues.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_global_priority.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-queue submission and queue priorities

## Picking queue families
```c
// prefer families with ONLY the capability you want: they map to dedicated engines
int pickFamily(VkQueueFlags want, VkQueueFlags avoid) {
    for (uint32_t i = 0; i < count; ++i)
        if ((props[i].queueFlags & want) == want && !(props[i].queueFlags & avoid)) return i;
    return -1;
}
int gfx      = pickFamily(VK_QUEUE_GRAPHICS_BIT, 0);
int compute  = pickFamily(VK_QUEUE_COMPUTE_BIT, VK_QUEUE_GRAPHICS_BIT);                 // async compute
int transfer = pickFamily(VK_QUEUE_TRANSFER_BIT, VK_QUEUE_GRAPHICS_BIT | VK_QUEUE_COMPUTE_BIT); // DMA engine
```
Fall back to the graphics family if a dedicated one doesn't exist; a graphics or compute family supports transfer commands even if it
does not report `VK_QUEUE_TRANSFER_BIT`. Check `minImageTransferGranularity` on transfer families: image copy offsets and extents
must respect it.

## Priorities
```c
float prio[2] = { 1.0f, 0.5f };
VkDeviceQueueCreateInfo q = { VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO };
q.queueFamilyIndex = gfx; q.queueCount = 2; q.pQueuePriorities = prio;
```
Priorities are normalized floats (0.0 lowest, 1.0 highest). Within one device a higher-priority queue may be allotted more processing time
and may starve a lower-priority one; the spec gives no ordering guarantee among equal-priority queues.
`VK_KHR_global_priority` (core in Vulkan 1.4; `VkDeviceQueueGlobalPriorityCreateInfo` with `LOW`, `MEDIUM` (the default), `HIGH` or
`REALTIME`) requests a priority relative to other work on the system; a request above `MEDIUM` can fail with `VK_ERROR_NOT_PERMITTED`
(`_KHR` in the extension) if the caller lacks privileges.

## Cross-queue synchronisation
- Use semaphores (timeline semaphores are simplest) between queues; fences are only for CPU.
- Resources used on two families with `VK_SHARING_MODE_EXCLUSIVE` need a queue family ownership
  transfer (release barrier on source queue + acquire barrier on destination), or create them
  `CONCURRENT`.
- Data written on one family must be ownership-transferred before another family reads it.
  Only resources whose previous contents you will discard (e.g. a render target cleared on the
  new queue) may skip the transfer.

## Typical uses
| Queue | Work |
|---|---|
| Graphics | main frame |
| Async compute | SSAO, light culling, particle sim overlapping shadow passes |
| Transfer | streaming textures/meshes without stalling graphics |

## Gotchas
- Batch work into few `vkQueueSubmit2` calls per queue.
- Async compute only helps if the overlapped workloads stress different units; profile it.
- Queues from the same family are not guaranteed to run concurrently in hardware.

## Verify
- [ ] GPU trace shows transfer/compute queue work overlapping graphics; validation reports no ownership errors.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23); vk.xml marks `VK_KHR_global_priority` as promoted to Vulkan 1.4. Confirmed in `devsandqueues.adoc`: queue priorities are normalized floats where higher may get more processing time and may starve lower, with no ordering guarantee among equals (the old text said most desktop drivers ignore them, which no document states); global priority levels are LOW, MEDIUM (default), HIGH and REALTIME, and a request above the default can return `VK_ERROR_NOT_PERMITTED` without privileges (the old text listed only HIGH/REALTIME and claimed VR compositors use it); transfer support is implied by graphics or compute (the `TRANSFER_BIT` is optional to report); `minImageTransferGranularity` semantics. Removed the (8,8,1) example, the DCC claim and the submission-cost claim.

Method: documentation only; no commands were run.
