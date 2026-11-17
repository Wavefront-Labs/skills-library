---
id: computing-software.computer-graphics-engineering.opengl.vulkan-immediate-submit-for-uploads
name: vulkan-immediate-submit-for-uploads
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-command-buffers, immediate-submit, one-time-submit, vkqueuesubmit2, queue-submission, upload-batching, transfer-queue]
level: practitioner
status: docs-checked
description: "Run one-off GPU work in Vulkan (uploads, mip generation, BLAS builds) with an immediate-submit helper, then graduate to batched async uploads with vkQueueSubmit2."
sources: ["https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#commandbuffers-submission", "https://docs.vulkan.org/guide/latest/extensions/VK_KHR_synchronization2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan immediate submit for uploads

**Goal:** a simple, correct path for one-off GPU work at load time, and a clear upgrade
path when it becomes a loading-time bottleneck.

## 1. The helper
```cpp
struct Immediate { VkCommandPool pool; VkCommandBuffer cmd; VkFence fence; } imm;
void immediateSubmit(std::function<void(VkCommandBuffer)>&& fn) {
    vkResetFences(dev, 1, &imm.fence);
    vkResetCommandBuffer(imm.cmd, 0);
    VkCommandBufferBeginInfo bi{VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO};
    bi.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;
    vkBeginCommandBuffer(imm.cmd, &bi);
    fn(imm.cmd);
    vkEndCommandBuffer(imm.cmd);
    VkCommandBufferSubmitInfo cbi{VK_STRUCTURE_TYPE_COMMAND_BUFFER_SUBMIT_INFO}; cbi.commandBuffer = imm.cmd;
    VkSubmitInfo2 si{VK_STRUCTURE_TYPE_SUBMIT_INFO_2}; si.commandBufferInfoCount = 1; si.pCommandBufferInfos = &cbi;
    vkQueueSubmit2(gfxQueue, 1, &si, imm.fence);
    vkWaitForFences(dev, 1, &imm.fence, VK_TRUE, 9'999'999'999);
}
```
Its pool is created with `RESET_COMMAND_BUFFER_BIT`. Uses: staging copies, layout
transitions for new textures, mip blits, acceleration-structure builds.

## 2. vkQueueSubmit2 (sync2) shape
`VkSubmitInfo2` takes arrays of `VkSemaphoreSubmitInfo` (semaphore, value for timeline,
**stageMask** per semaphore, `deviceIndex`) and `VkCommandBufferSubmitInfo`. `vkQueueSubmit2` takes an array of `VkSubmitInfo2`,
so several command buffers and several submits can go in **one** call; fewer calls means less per-submit overhead.

## 3. When immediate submit becomes the problem
It serialises CPU and GPU per upload. Loading 2,000 textures this way is slow. Upgrade:
1. Record **many** copies into one command buffer, submit once.
2. Move uploads to a dedicated transfer queue with a staging ring; signal a **timeline
   semaphore** value per batch; the render queue waits on that value before first use
   (requires queue-family ownership transfer if using `EXCLUSIVE` sharing).
3. Poll `vkGetSemaphoreCounterValue` to know which assets are resident, instead of waiting.

## Gotchas
- Calling immediate submit from multiple threads needs one helper (pool+fence) per thread
  or a mutex — pools are externally synchronised.
- Using it during the frame stalls rendering; restrict to load time or a loading thread
  with its own queue.
- Forgetting the barrier after the copy (`TRANSFER_WRITE` → `SHADER_READ`, layout to
  `SHADER_READ_ONLY_OPTIMAL`) is a synchronisation error even if one GPU happens to show correct output.

## Verify
- [ ] Level load profile: number of `vkQueueSubmit2` calls is O(batches), not O(assets).
- [ ] Validation clean (layouts and access masks) after uploads.
- [ ] Rendering never blocks on a fence from the upload path during gameplay.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (xml/vk.xml, validusage.json, chapters/cmdbuffers.adoc).
Confirmed: VkSubmitInfo2 members (pWaitSemaphoreInfos, pCommandBufferInfos, pSignalSemaphoreInfos), VkSemaphoreSubmitInfo members including stageMask and deviceIndex, VkCommandBufferSubmitInfo, vkGetSemaphoreCounterValue requires a timeline semaphore, the commandbuffers-submission section. Removed the vkguide attribution and unverified kernel-transition and GPU-specific claims.
Method: documentation only; no commands were run.
