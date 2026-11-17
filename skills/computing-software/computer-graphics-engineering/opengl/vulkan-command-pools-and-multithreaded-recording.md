---
id: computing-software.computer-graphics-engineering.opengl.vulkan-command-pools-and-multithreaded-recording
name: vulkan-command-pools-and-multithreaded-recording
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-command-buffers, command-buffers, command-pools, multithreaded-recording, secondary-command-buffers, vkresetcommandpool, render-pass-continue, job-system]
level: advanced
status: docs-checked
description: "Organise Vulkan command pools per frame and per thread, reset pools instead of buffers, and record in parallel with secondary buffers or per-thread primaries."
sources: ["https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan command pools and multithreaded recording

**Goal:** command recording that scales across CPU cores with no locks and minimal
allocation churn.

## 1. Pool layout: [frame in flight][thread]
Command pools are **externally synchronised** — one thread at a time per pool (and its
buffers). So:
```cpp
struct FrameCmd { VkCommandPool pool[MAX_THREADS]; std::vector<VkCommandBuffer> bufs[MAX_THREADS]; };
FrameCmd frames[FRAMES_IN_FLIGHT];
// start of frame, after waiting that frame's fence:
for (int t = 0; t < threads; ++t) vkResetCommandPool(dev, frames[fi].pool[t], 0);
```
- `vkResetCommandPool` returns every buffer of the pool to the initial state in one call; per-buffer
  `vkResetCommandBuffer` additionally requires `VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT`.
- Use `VK_COMMAND_POOL_CREATE_TRANSIENT_BIT` for short-lived per-frame buffers (a hint the implementation may use for allocation behaviour).
- Allocate buffers once and reuse; don't allocate/free each frame.

## 2. Option A: secondary command buffers inside one pass
```cpp
VkCommandBufferInheritanceRenderingInfo inh{VK_STRUCTURE_TYPE_COMMAND_BUFFER_INHERITANCE_RENDERING_INFO};
inh.colorAttachmentCount = 1; inh.pColorAttachmentFormats = &colorFmt; inh.depthAttachmentFormat = depthFmt;
inh.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;
VkCommandBufferInheritanceInfo ii{VK_STRUCTURE_TYPE_COMMAND_BUFFER_INHERITANCE_INFO, &inh};
VkCommandBufferBeginInfo bi{VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO};
bi.flags = VK_COMMAND_BUFFER_USAGE_RENDER_PASS_CONTINUE_BIT | VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;
bi.pInheritanceInfo = &ii;
// each worker records its slice of draws into its own secondary
// main thread: vkCmdBeginRendering(... flags = VK_RENDERING_CONTENTS_SECONDARY_COMMAND_BUFFERS_BIT)
vkCmdExecuteCommands(primary, n, secondaries);
```
The spec states a secondary command buffer inherits no state from the primary: re-bind pipeline, descriptor sets, viewport/scissor
(dynamic state) in each one. With dynamic rendering, `RENDER_PASS_CONTINUE_BIT` requires `VkCommandBufferInheritanceRenderingInfo` in the inheritance `pNext` chain.

## 3. Option B: per-thread primaries per pass
Each worker records a whole pass (shadow cascade, G-buffer chunk) into its own primary;
submit them in order in one `vkQueueSubmit2` with multiple command buffer infos. Simpler,
no inheritance rules, works when passes are independent.

## 4. Granularity
Choose job sizes by measurement: very small secondaries add `vkCmdExecuteCommands` overhead. Check each vendor's best-practice guide for secondary command buffer advice on your targets.

## Gotchas
- Recording into a buffer from a pool another thread is resetting = data race the
  validation layer may not catch. Pool per thread per frame, no sharing.
- Resetting a pool whose buffers are still executing on the GPU is invalid — only after the
  frame fence.
- Secondary buffers recorded with `ONE_TIME_SUBMIT` must be re-recorded every frame;
  cached secondaries need `SIMULTANEOUS_USE` if executed in two frames concurrently.

## Verify
- [ ] CPU profiler shows recording spread across worker threads, main thread mostly submitting.
- [ ] No per-frame `vkAllocateCommandBuffers`/`vkFreeCommandBuffers` in steady state.
- [ ] Validation clean with sync validation enabled.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/cmdbuffers.adoc, validusage.json, xml/vk.xml).
Confirmed: VkCommandBufferInheritanceRenderingInfo members (colorAttachmentCount, pColorAttachmentFormats, depthAttachmentFormat, rasterizationSamples); RENDER_PASS_CONTINUE_BIT rule with dynamic rendering; no state inherited by secondaries; vkResetCommandPool rule against pending buffers; RESET_COMMAND_BUFFER_BIT and TRANSIENT semantics. Removed the unverified job-size and driver-speed claims.
Method: documentation only; no commands were run.
