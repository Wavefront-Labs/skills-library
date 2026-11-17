---
id: computing-software.computer-graphics-engineering.opengl.vulkan-queue-family-ownership-transfer
name: vulkan-queue-family-ownership-transfer
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-synchronization, queue-ownership-transfer, vk-sharing-mode-exclusive, async-compute, transfer-queue]
level: advanced
status: docs-checked
description: "Move Vulkan resources between queue families safely: release/acquire barrier pairs, semaphores, when CONCURRENT sharing is simpler, and common mistakes."
sources: ["https://docs.vulkan.org/spec/latest/chapters/synchronization.html#synchronization-queue-transfers", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue family ownership transfers

**Goal:** use a resource created with `VK_SHARING_MODE_EXCLUSIVE` on a second queue family
(dedicated transfer queue upload, async compute) without undefined contents.

## 1. Release on the source queue
```cpp
VkBufferMemoryBarrier2 rel{VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER_2};
rel.srcStageMask = VK_PIPELINE_STAGE_2_COPY_BIT;  rel.srcAccessMask = VK_ACCESS_2_TRANSFER_WRITE_BIT;
rel.dstStageMask = VK_PIPELINE_STAGE_2_NONE;      rel.dstAccessMask = 0;   // ignored on release
rel.srcQueueFamilyIndex = transferFamily; rel.dstQueueFamilyIndex = graphicsFamily;
rel.buffer = buf; rel.size = VK_WHOLE_SIZE;
// record in the transfer command buffer, submit signalling semaphore S
```
## 2. Acquire on the destination queue
Same barrier (same family indices, same subresource range, same old/new layout for images)
recorded on the graphics queue, with `srcStageMask = NONE, srcAccessMask = 0` (source masks are
ignored on an acquire) and real
`dstStageMask/dstAccessMask` (e.g. `VERTEX_ATTRIBUTE_INPUT` / `VERTEX_ATTRIBUTE_READ`).
Submit waiting on semaphore S. The pair is one logical barrier split across queues; a layout
transition specified in both happens once, between them.

## 3. When to skip it
- `srcQueueFamilyIndex == dstQueueFamilyIndex` or `VK_QUEUE_FAMILY_IGNORED`: no transfer.
- If you do not care about the old contents (resource will be fully overwritten), skip the
  release and just use it on the new queue, with an `UNDEFINED` old layout on images.
- `VK_SHARING_MODE_CONCURRENT` with both families listed in `pQueueFamilyIndices` needs no
  ownership transfer; the spec requires explicit transfers only for `EXCLUSIVE` resources.

## Gotchas
- Missing semaphore between release and acquire = race even with correct barriers.
- A release without a matching acquire leaves the contents and image layout undefined for the
  second queue family; an acquire must match a previous release (same range).

## Verify
- [ ] Validation (with syncval) clean for upload-then-draw across queues.
- [ ] Uploaded meshes render correctly on first frame with the transfer queue path enabled.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: EXCLUSIVE resources must have ownership explicitly transferred; without a transfer the contents are undefined for reads on the second family; the transfer is skippable when contents are not needed (spec note).
- Confirmed: Release: destination access mask ignored (and destination stage mask ignored unless the maintenance8 flag is used); acquire: source access mask ignored (source stage likewise); acquire range must match the release exactly; an execution dependency such as a semaphore must order the two halves.
- Removed AMD DCC and DMA-engine remarks (no source found).

Method: documentation only; no commands were run.
